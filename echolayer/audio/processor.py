"""Audio processing with latency measurement"""
import sounddevice as sd
import numpy as np
import time
from typing import Optional, Callable, List, Tuple
from ..config import AudioConfig
from ..layers.ultrasonic import UltrasonicLayer


class LatencyMeasurement:
    """Container for latency measurement data"""
    
    def __init__(self):
        self.input_timestamp: int = 0
        self.output_timestamp: int = 0
        self.latency_ns: int = 0
        self.has_ultrasonic: bool = False
    
    @property
    def latency_ms(self) -> float:
        """Get latency in milliseconds"""
        return self.latency_ns / 1_000_000
        
    def calculate_latency(self) -> int:
        """Calculate latency in nanoseconds"""
        self.latency_ns = self.output_timestamp - self.input_timestamp
        return self.latency_ns
    
    def to_dict(self) -> dict:
        """Convert to dictionary for logging"""
        return {
            'input_timestamp_ns': self.input_timestamp,
            'output_timestamp_ns': self.output_timestamp,
            'latency_ns': self.latency_ns,
            'latency_ms': self.latency_ns / 1_000_000,
            'has_ultrasonic': self.has_ultrasonic
        }


class AudioProcessor:
    """Process audio with optional ultrasonic layers and measure latency"""
    
    def __init__(self, config: AudioConfig):
        """
        Initialize audio processor
        
        Args:
            config: Audio configuration
        """
        self.config = config
        self.ultrasonic_layer: Optional[UltrasonicLayer] = None
        self.measurements: List[LatencyMeasurement] = []
        self.callback_func: Optional[Callable] = None
        self.stream: Optional[sd.Stream] = None
        self.is_running = False
        
    def enable_ultrasonic_layer(self, frequency: int = 20000, amplitude: float = 0.1):
        """
        Enable ultrasonic layer
        
        Args:
            frequency: Ultrasonic frequency in Hz
            amplitude: Signal amplitude
        """
        self.ultrasonic_layer = UltrasonicLayer(
            sample_rate=self.config.sample_rate,
            frequency=frequency,
            amplitude=amplitude
        )
        
    def disable_ultrasonic_layer(self):
        """Disable ultrasonic layer"""
        self.ultrasonic_layer = None
    
    def is_ultrasonic_enabled(self) -> bool:
        """Check if ultrasonic layer is enabled"""
        return self.ultrasonic_layer is not None
    
    def _audio_callback(self, indata, outdata, frames, time_info, status):
        """
        Audio callback function for processing
        
        Args:
            indata: Input audio data
            outdata: Output audio data buffer
            frames: Number of frames
            time_info: Timing information
            status: Status flags
        """
        if status:
            print(f"Audio callback status: {status}")
        
        # Create measurement
        measurement = LatencyMeasurement()
        measurement.input_timestamp = time.monotonic_ns()
        measurement.has_ultrasonic = self.is_ultrasonic_enabled()
        
        # Process audio - pass through with optional ultrasonic layer
        if self.ultrasonic_layer:
            outdata[:] = self.ultrasonic_layer.apply_to_signal(indata)
        else:
            outdata[:] = indata
        
        measurement.output_timestamp = time.monotonic_ns()
        measurement.calculate_latency()
        
        # Store measurement
        self.measurements.append(measurement)
        
        # Call custom callback if set
        if self.callback_func:
            self.callback_func(measurement)
    
    def start_stream(self, callback: Optional[Callable] = None):
        """
        Start audio stream
        
        Args:
            callback: Optional callback function for measurement updates
        """
        if self.is_running:
            return
        
        self.callback_func = callback
        self.measurements.clear()
        
        # Reset ultrasonic phase if enabled
        if self.ultrasonic_layer:
            self.ultrasonic_layer.reset_phase()
        
        self.stream = sd.Stream(
            samplerate=self.config.sample_rate,
            channels=self.config.channels,
            dtype=self.config.dtype,
            blocksize=self.config.chunk_size,
            device=self.config.device_index,
            callback=self._audio_callback
        )
        
        self.stream.start()
        self.is_running = True
    
    def stop_stream(self):
        """Stop audio stream"""
        if self.stream and self.is_running:
            self.stream.stop()
            self.stream.close()
            self.is_running = False
            self.stream = None
    
    def get_measurements(self) -> List[LatencyMeasurement]:
        """Get all latency measurements"""
        return self.measurements.copy()
    
    def get_statistics(self) -> dict:
        """
        Calculate statistics from measurements
        
        Returns:
            Dictionary with latency statistics
        """
        if not self.measurements:
            return {
                'count': 0,
                'mean_ms': 0.0,
                'min_ms': 0.0,
                'max_ms': 0.0,
                'std_ms': 0.0
            }
        
        latencies_ms = [m.latency_ns / 1_000_000 for m in self.measurements]
        
        return {
            'count': len(latencies_ms),
            'mean_ms': np.mean(latencies_ms),
            'min_ms': np.min(latencies_ms),
            'max_ms': np.max(latencies_ms),
            'std_ms': np.std(latencies_ms)
        }
    
    def list_audio_devices(self) -> List[dict]:
        """
        List available audio devices
        
        Returns:
            List of audio device information
        """
        return sd.query_devices()
