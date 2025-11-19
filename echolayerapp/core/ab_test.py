"""
A/B test framework for comparing audio configurations.
"""

import time
from typing import Dict, List, Optional, Callable
from .audio_engine import AudioEngine


class ABTest:
    """A/B testing framework for comparing audio latency."""
    
    def __init__(self, audio_engine: AudioEngine):
        """
        Initialize A/B test framework.
        
        Args:
            audio_engine: AudioEngine instance to use for tests
        """
        self.audio_engine = audio_engine
        self.test_results = {
            'A': [],
            'B': []
        }
        
    def run_test(self, config_a: Dict, config_b: Dict, 
                 iterations: int = 10) -> Dict:
        """
        Run A/B test comparing two configurations.
        
        Args:
            config_a: Configuration A (dict with 'base_freq', 'overlay_freq', etc.)
            config_b: Configuration B (dict with 'base_freq', 'overlay_freq', etc.)
            iterations: Number of test iterations per configuration
            
        Returns:
            Dictionary with test results and statistics
        """
        results = {
            'A': {'measurements': [], 'config': config_a},
            'B': {'measurements': [], 'config': config_b}
        }
        
        # Run test A
        for i in range(iterations):
            audio_a = self._generate_audio_from_config(config_a)
            measurement = self.audio_engine.play_audio(audio_a, blocking=True)
            results['A']['measurements'].append(measurement)
            time.sleep(0.1)  # Brief pause between iterations
        
        # Run test B
        for i in range(iterations):
            audio_b = self._generate_audio_from_config(config_b)
            measurement = self.audio_engine.play_audio(audio_b, blocking=True)
            results['B']['measurements'].append(measurement)
            time.sleep(0.1)  # Brief pause between iterations
        
        # Calculate statistics
        results['A']['stats'] = self._calculate_stats(results['A']['measurements'])
        results['B']['stats'] = self._calculate_stats(results['B']['measurements'])
        
        # Store results
        self.test_results = results
        
        return results
    
    def _generate_audio_from_config(self, config: Dict):
        """Generate audio based on configuration."""
        if 'overlay_freq' in config and config['overlay_freq'] > 0:
            return self.audio_engine.generate_ultrasonic_overlay(
                config.get('base_freq', 1000),
                config.get('overlay_freq', 20000),
                config.get('amplitude', 0.3)
            )
        else:
            return self.audio_engine.generate_tone(
                config.get('base_freq', 1000),
                config.get('amplitude', 0.5)
            )
    
    def _calculate_stats(self, measurements: List[Dict]) -> Dict:
        """Calculate statistics from measurements."""
        if not measurements:
            return {
                'count': 0,
                'mean_latency_ns': 0,
                'min_latency_ns': 0,
                'max_latency_ns': 0,
                'std_latency_ns': 0
            }
        
        latencies = [m.get('total_latency_ns', 0) for m in measurements if 'error' not in m]
        
        if not latencies:
            return {
                'count': 0,
                'mean_latency_ns': 0,
                'min_latency_ns': 0,
                'max_latency_ns': 0,
                'std_latency_ns': 0,
                'errors': len(measurements)
            }
        
        import numpy as np
        
        return {
            'count': len(latencies),
            'mean_latency_ns': float(np.mean(latencies)),
            'min_latency_ns': float(np.min(latencies)),
            'max_latency_ns': float(np.max(latencies)),
            'std_latency_ns': float(np.std(latencies)),
            'mean_latency_ms': float(np.mean(latencies)) / 1_000_000,
            'errors': len(measurements) - len(latencies)
        }
    
    def get_comparison(self) -> Dict:
        """
        Get comparison between A and B tests.
        
        Returns:
            Dictionary with comparison metrics
        """
        if not self.test_results or 'A' not in self.test_results:
            return {'error': 'No test results available'}
        
        stats_a = self.test_results['A'].get('stats', {})
        stats_b = self.test_results['B'].get('stats', {})
        
        mean_a = stats_a.get('mean_latency_ns', 0)
        mean_b = stats_b.get('mean_latency_ns', 0)
        
        if mean_a == 0:
            percent_diff = 0
        else:
            percent_diff = ((mean_b - mean_a) / mean_a) * 100
        
        return {
            'A_mean_latency_ms': stats_a.get('mean_latency_ms', 0),
            'B_mean_latency_ms': stats_b.get('mean_latency_ms', 0),
            'difference_ms': (mean_b - mean_a) / 1_000_000,
            'percent_difference': percent_diff,
            'winner': 'A' if mean_a < mean_b else 'B' if mean_b < mean_a else 'Tie'
        }
