"""
Command-line interface for EchoLayerApp.
"""

import argparse
import sys
from ..core.audio_engine import AudioEngine
from ..core.ab_test import ABTest
from ..utils.logger import LatencyLogger
from ..utils.config import Config


class CLI:
    """Command-line interface for EchoLayerApp."""
    
    def __init__(self):
        """Initialize CLI."""
        self.config = Config()
        self.audio_engine = AudioEngine(
            sample_rate=self.config.get('audio.sample_rate'),
            duration=self.config.get('audio.duration')
        )
        self.logger = LatencyLogger(
            log_dir=self.config.get('logging.log_dir')
        )
    
    def run(self):
        """Run the CLI."""
        parser = self._create_parser()
        args = parser.parse_args()
        
        if args.command == 'info':
            self._show_device_info()
        elif args.command == 'play':
            self._play_tone(args)
        elif args.command == 'test':
            self._run_single_test(args)
        elif args.command == 'ab-test':
            self._run_ab_test(args)
        else:
            parser.print_help()
    
    def _create_parser(self):
        """Create argument parser."""
        parser = argparse.ArgumentParser(
            description='EchoLayerApp - Ultrasonic overlay latency benchmark tool'
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Info command
        subparsers.add_parser('info', help='Show audio device information')
        
        # Play command
        play_parser = subparsers.add_parser('play', help='Play a test tone')
        play_parser.add_argument('--frequency', type=float, default=1000,
                                help='Frequency in Hz (default: 1000)')
        play_parser.add_argument('--overlay', type=float, default=0,
                                help='Overlay frequency in Hz (default: 0, disabled)')
        play_parser.add_argument('--amplitude', type=float, default=0.3,
                                help='Amplitude 0.0-1.0 (default: 0.3)')
        
        # Test command
        test_parser = subparsers.add_parser('test', help='Run latency test')
        test_parser.add_argument('--frequency', type=float, default=1000,
                                help='Base frequency in Hz (default: 1000)')
        test_parser.add_argument('--overlay', type=float, default=20000,
                                help='Overlay frequency in Hz (default: 20000)')
        test_parser.add_argument('--iterations', type=int, default=10,
                                help='Number of iterations (default: 10)')
        test_parser.add_argument('--output', type=str, default=None,
                                help='Output log file name')
        
        # A/B test command
        ab_parser = subparsers.add_parser('ab-test', help='Run A/B comparison test')
        ab_parser.add_argument('--freq-a', type=float, default=1000,
                              help='Test A base frequency (default: 1000)')
        ab_parser.add_argument('--overlay-a', type=float, default=0,
                              help='Test A overlay frequency (default: 0)')
        ab_parser.add_argument('--freq-b', type=float, default=1000,
                              help='Test B base frequency (default: 1000)')
        ab_parser.add_argument('--overlay-b', type=float, default=20000,
                              help='Test B overlay frequency (default: 20000)')
        ab_parser.add_argument('--iterations', type=int, default=10,
                              help='Iterations per test (default: 10)')
        ab_parser.add_argument('--output', type=str, default=None,
                              help='Output log file name')
        
        return parser
    
    def _show_device_info(self):
        """Show audio device information."""
        print("\n=== Audio Device Information ===\n")
        info = self.audio_engine.get_device_info()
        
        if 'error' in info:
            print(f"Error: {info['error']}")
            return
        
        print(f"Default Input Device: {info.get('default_input', 'N/A')}")
        print(f"Default Output Device: {info.get('default_output', 'N/A')}")
        print("\nAvailable Devices:")
        
        devices = info.get('devices', [])
        if isinstance(devices, dict):
            for idx, device in devices.items():
                print(f"  [{idx}] {device}")
        else:
            for idx, device in enumerate(devices):
                print(f"  [{idx}] {device}")
    
    def _play_tone(self, args):
        """Play a test tone."""
        print(f"\nPlaying tone: {args.frequency} Hz", end='')
        
        if args.overlay > 0:
            print(f" with {args.overlay} Hz overlay")
            audio = self.audio_engine.generate_ultrasonic_overlay(
                args.frequency, args.overlay, args.amplitude
            )
        else:
            print()
            audio = self.audio_engine.generate_tone(args.frequency, args.amplitude)
        
        measurement = self.audio_engine.play_audio(audio, blocking=True)
        
        if 'error' in measurement:
            print(f"Error: {measurement['error']}")
        else:
            print(f"Playback completed. Latency: {measurement['total_latency_ns'] / 1_000_000:.2f} ms")
    
    def _run_single_test(self, args):
        """Run a single latency test."""
        print(f"\n=== Running Latency Test ===")
        print(f"Base frequency: {args.frequency} Hz")
        print(f"Overlay frequency: {args.overlay} Hz")
        print(f"Iterations: {args.iterations}\n")
        
        self.audio_engine.clear_measurements()
        
        for i in range(args.iterations):
            print(f"Iteration {i+1}/{args.iterations}...", end=' ')
            
            if args.overlay > 0:
                audio = self.audio_engine.generate_ultrasonic_overlay(
                    args.frequency, args.overlay
                )
            else:
                audio = self.audio_engine.generate_tone(args.frequency)
            
            measurement = self.audio_engine.play_audio(audio, blocking=True)
            
            if 'error' in measurement:
                print(f"Error: {measurement['error']}")
            else:
                print(f"{measurement['total_latency_ns'] / 1_000_000:.2f} ms")
        
        # Log results
        measurements = self.audio_engine.get_measurements()
        filepath = self.logger.log_measurements(measurements, args.output)
        
        # Print statistics
        self._print_statistics(measurements)
        print(f"\nResults logged to: {filepath}")
    
    def _run_ab_test(self, args):
        """Run A/B comparison test."""
        print(f"\n=== Running A/B Test ===")
        print(f"Test A: {args.freq_a} Hz (overlay: {args.overlay_a} Hz)")
        print(f"Test B: {args.freq_b} Hz (overlay: {args.overlay_b} Hz)")
        print(f"Iterations: {args.iterations}\n")
        
        ab_test = ABTest(self.audio_engine)
        
        config_a = {
            'base_freq': args.freq_a,
            'overlay_freq': args.overlay_a
        }
        
        config_b = {
            'base_freq': args.freq_b,
            'overlay_freq': args.overlay_b
        }
        
        print("Running Test A...")
        print("Running Test B...")
        results = ab_test.run_test(config_a, config_b, args.iterations)
        
        # Print results
        print("\n=== Results ===\n")
        
        # Check for errors
        stats_a = results['A']['stats']
        stats_b = results['B']['stats']
        
        if stats_a.get('errors', 0) > 0 or stats_b.get('errors', 0) > 0:
            print("Warning: Some measurements failed (audio device may not be available)")
            if stats_a.get('errors', 0) > 0:
                print(f"  Test A: {stats_a['errors']} errors out of {args.iterations} iterations")
            if stats_b.get('errors', 0) > 0:
                print(f"  Test B: {stats_b['errors']} errors out of {args.iterations} iterations")
            print()
        
        print(f"Test A - Mean Latency: {stats_a['mean_latency_ms']:.2f} ms")
        print(f"Test B - Mean Latency: {stats_b['mean_latency_ms']:.2f} ms")
        
        comparison = ab_test.get_comparison()
        print(f"\nDifference: {comparison['difference_ms']:.2f} ms ({comparison['percent_difference']:.1f}%)")
        print(f"Winner: {comparison['winner']}")
        
        # Log results
        filepath = self.logger.log_ab_test_results(results, args.output)
        print(f"\nResults logged to: {filepath}")
    
    def _print_statistics(self, measurements):
        """Print statistics from measurements."""
        if not measurements:
            return
        
        latencies = [m['total_latency_ns'] / 1_000_000 
                    for m in measurements if 'error' not in m]
        
        if not latencies:
            print("\nNo valid measurements.")
            return
        
        import statistics
        
        print("\n=== Statistics ===")
        print(f"Count: {len(latencies)}")
        print(f"Mean: {statistics.mean(latencies):.2f} ms")
        print(f"Median: {statistics.median(latencies):.2f} ms")
        print(f"Min: {min(latencies):.2f} ms")
        print(f"Max: {max(latencies):.2f} ms")
        if len(latencies) > 1:
            print(f"Std Dev: {statistics.stdev(latencies):.2f} ms")


def main():
    """Main entry point for CLI."""
    cli = CLI()
    cli.run()


if __name__ == '__main__':
    main()
