"""Ultrasonic layer generator for audio benchmarking"""
import numpy as np
from typing import Tuple


class UltrasonicLayer:
    """Generate and apply ultrasonic layers to audio signals"""
    
    def __init__(self, sample_rate: int, frequency: int = 20000, amplitude: float = 0.1):
        """
        Initialize ultrasonic layer generator
        
        Args:
            sample_rate: Audio sample rate in Hz
            frequency: Ultrasonic frequency in Hz (default 20kHz)
            amplitude: Signal amplitude 0.0-1.0
        """
        self.sample_rate = sample_rate
        self.frequency = frequency
        self.amplitude = amplitude
        self.phase = 0.0
        
    def generate(self, num_samples: int, channels: int = 2) -> np.ndarray:
        """
        Generate ultrasonic signal
        
        Args:
            num_samples: Number of samples to generate
            channels: Number of audio channels
            
        Returns:
            numpy array of ultrasonic signal
        """
        # Generate time array
        t = np.arange(num_samples) / self.sample_rate
        
        # Generate sine wave with continuous phase
        phase_increment = 2 * np.pi * self.frequency * num_samples / self.sample_rate
        signal = self.amplitude * np.sin(2 * np.pi * self.frequency * t + self.phase)
        
        # Update phase for continuity
        self.phase = (self.phase + phase_increment) % (2 * np.pi)
        
        # Expand to multiple channels if needed
        if channels > 1:
            signal = np.tile(signal.reshape(-1, 1), (1, channels))
        
        return signal.astype(np.float32)
    
    def apply_to_signal(self, audio_signal: np.ndarray) -> np.ndarray:
        """
        Apply ultrasonic layer to existing audio signal
        
        Args:
            audio_signal: Input audio signal
            
        Returns:
            Audio signal with ultrasonic layer added
        """
        if len(audio_signal.shape) == 1:
            channels = 1
            num_samples = len(audio_signal)
        else:
            num_samples, channels = audio_signal.shape
            
        ultrasonic = self.generate(num_samples, channels)
        return audio_signal + ultrasonic
    
    def reset_phase(self):
        """Reset the phase to zero"""
        self.phase = 0.0
