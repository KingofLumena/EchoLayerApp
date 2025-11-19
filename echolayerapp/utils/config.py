"""
Configuration management for EchoLayerApp.
"""

import json
import os
from typing import Dict, Any


class Config:
    """Configuration manager for EchoLayerApp."""
    
    DEFAULT_CONFIG = {
        'audio': {
            'sample_rate': 44100,
            'duration': 1.0,
            'amplitude': 0.3
        },
        'test': {
            'iterations': 10,
            'base_frequency': 1000,
            'ultrasonic_frequency': 20000
        },
        'logging': {
            'log_dir': 'logs',
            'format': 'json'
        },
        'gui': {
            'window_title': 'EchoLayerApp - Latency Benchmark',
            'window_size': '800x600'
        }
    }
    
    def __init__(self, config_file: str = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to JSON config file (optional)
        """
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_file and os.path.exists(config_file):
            self.load_from_file(config_file)
    
    def load_from_file(self, filepath: str):
        """Load configuration from JSON file."""
        with open(filepath, 'r') as f:
            user_config = json.load(f)
            self._merge_config(user_config)
    
    def _merge_config(self, user_config: Dict):
        """Merge user config with defaults."""
        for key, value in user_config.items():
            if key in self.config and isinstance(value, dict):
                self.config[key].update(value)
            else:
                self.config[key] = value
    
    def save_to_file(self, filepath: str):
        """Save current configuration to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'audio.sample_rate')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        Set configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
