"""Configuration management for EchoLayerApp"""
from dataclasses import dataclass


@dataclass
class AudioConfig:
    """Audio configuration settings"""
    sample_rate: int = 48000
    channels: int = 2
    chunk_size: int = 1024
    device_index: int = None  # None for default device
    dtype: str = 'float32'


@dataclass
class UltrasonicLayerConfig:
    """Ultrasonic layer configuration"""
    frequency: int = 20000  # Hz - ultrasonic frequency
    amplitude: float = 0.1  # 0.0 to 1.0
    enabled: bool = False


@dataclass
class LoggingConfig:
    """Logging configuration"""
    log_dir: str = "logs"
    log_file_prefix: str = "latency_test"
    log_format: str = "csv"  # csv or json


@dataclass
class AppConfig:
    """Main application configuration"""
    audio: AudioConfig = None
    ultrasonic: UltrasonicLayerConfig = None
    logging: LoggingConfig = None
    
    def __post_init__(self):
        if self.audio is None:
            self.audio = AudioConfig()
        if self.ultrasonic is None:
            self.ultrasonic = UltrasonicLayerConfig()
        if self.logging is None:
            self.logging = LoggingConfig()
