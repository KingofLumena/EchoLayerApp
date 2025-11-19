"""
Audio engine module for EchoLayerApp.
Handles audio generation, playback, and latency measurement.
"""

import numpy as np
import sounddevice as sd
import time
from typing import Dict, Optional, Tuple


class AudioEngine:
    """Core audio engine for ultrasonic overlay benchmarking."""
    
    def __init__(self, sample_rate: int = 44100, duration: float = 1.0):
        """
        Initialize the audio engine.
        
        Args:
            sample_rate: Sample rate in Hz (default 44100)
            duration: Duration of audio samples in seconds (default 1.0)
        """
        self.sample_rate = sample_rate
        self.duration = duration
        self.latency_measurements = []
        
    def generate_tone(self, frequency: float, amplitude: float = 0.5) -> np.ndarray:
        """
        Generate a sine wave tone.
        
        Args:
            frequency: Frequency in Hz
            amplitude: Amplitude (0.0 to 1.0)
            
        Returns:
            numpy array of audio samples
        """
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), False)
        tone = amplitude * np.sin(2 * np.pi * frequency * t)
        return tone.astype(np.float32)
    
    def generate_ultrasonic_overlay(self, base_freq: float, 
                                   overlay_freq: float,
                                   amplitude: float = 0.3) -> np.ndarray:
        """
        Generate audio with ultrasonic overlay.
        
        Args:
            base_freq: Base frequency in Hz
            overlay_freq: Overlay frequency in Hz (typically ultrasonic range)
            amplitude: Amplitude (0.0 to 1.0)
            
        Returns:
            numpy array of mixed audio samples
        """
        base_tone = self.generate_tone(base_freq, amplitude)
        overlay_tone = self.generate_tone(overlay_freq, amplitude * 0.5)
        mixed = base_tone + overlay_tone
        # Normalize to prevent clipping
        mixed = mixed / np.max(np.abs(mixed))
        return mixed.astype(np.float32)
    
    def play_audio(self, audio_data: np.ndarray, blocking: bool = True) -> Dict[str, float]:
        """
        Play audio and measure latency.
        
        Args:
            audio_data: Audio samples to play
            blocking: Whether to wait for playback to complete
            
        Returns:
            Dictionary with latency measurements in nanoseconds
        """
        # Measure scheduling latency
        schedule_start = time.monotonic_ns()
        
        try:
            # Start playback
            sd.play(audio_data, self.sample_rate)
            schedule_end = time.monotonic_ns()
            
            if blocking:
                playback_start = time.monotonic_ns()
                sd.wait()  # Wait for playback to complete
                playback_end = time.monotonic_ns()
            else:
                playback_start = schedule_end
                playback_end = schedule_end
            
            measurements = {
                'schedule_latency_ns': schedule_end - schedule_start,
                'playback_duration_ns': playback_end - playback_start,
                'total_latency_ns': playback_end - schedule_start,
                'timestamp_ns': schedule_start
            }
            
            self.latency_measurements.append(measurements)
            return measurements
            
        except Exception as e:
            return {
                'error': str(e),
                'schedule_latency_ns': 0,
                'playback_duration_ns': 0,
                'total_latency_ns': 0,
                'timestamp_ns': time.monotonic_ns()
            }
    
    def stop_audio(self):
        """Stop any currently playing audio."""
        sd.stop()
    
    def get_device_info(self) -> Dict:
        """
        Get information about available audio devices.
        
        Returns:
            Dictionary with device information
        """
        try:
            devices = sd.query_devices()
            default_device = sd.default.device
            return {
                'devices': devices,
                'default_input': default_device[0] if isinstance(default_device, tuple) else default_device,
                'default_output': default_device[1] if isinstance(default_device, tuple) else default_device
            }
        except Exception as e:
            return {'error': str(e)}
    
    def clear_measurements(self):
        """Clear all latency measurements."""
        self.latency_measurements = []
    
    def get_measurements(self) -> list:
        """
        Get all latency measurements.
        
        Returns:
            List of measurement dictionaries
        """
        return self.latency_measurements
