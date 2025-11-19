"""Logging module for latency measurements"""
import os
import csv
import json
from datetime import datetime
from typing import List
from pathlib import Path
from ..audio.processor import LatencyMeasurement
from ..config import LoggingConfig


class LatencyLogger:
    """Logger for latency measurement results"""
    
    def __init__(self, config: LoggingConfig):
        """
        Initialize logger
        
        Args:
            config: Logging configuration
        """
        self.config = config
        self.log_dir = Path(config.log_dir)
        self.log_dir.mkdir(exist_ok=True, parents=True)
        
    def _generate_filename(self, extension: str) -> Path:
        """Generate timestamped filename"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.config.log_file_prefix}_{timestamp}.{extension}"
        return self.log_dir / filename
    
    def save_measurements_csv(self, measurements: List[LatencyMeasurement], 
                               test_name: str = "") -> str:
        """
        Save measurements to CSV file
        
        Args:
            measurements: List of latency measurements
            test_name: Optional test name/description
            
        Returns:
            Path to saved file
        """
        filepath = self._generate_filename("csv")
        
        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'input_timestamp_ns', 'output_timestamp_ns', 
                          'latency_ns', 'latency_ms', 'has_ultrasonic']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            # Add metadata row if test name provided
            if test_name:
                writer.writerow({'timestamp': f"Test: {test_name}"})
            
            for idx, measurement in enumerate(measurements):
                row = measurement.to_dict()
                row['timestamp'] = idx
                writer.writerow(row)
        
        return str(filepath)
    
    def save_measurements_json(self, measurements: List[LatencyMeasurement], 
                                test_name: str = "", 
                                statistics: dict = None) -> str:
        """
        Save measurements to JSON file
        
        Args:
            measurements: List of latency measurements
            test_name: Optional test name/description
            statistics: Optional statistics dictionary
            
        Returns:
            Path to saved file
        """
        filepath = self._generate_filename("json")
        
        data = {
            'test_name': test_name,
            'timestamp': datetime.now().isoformat(),
            'measurements': [m.to_dict() for m in measurements],
            'statistics': statistics or {}
        }
        
        with open(filepath, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=2)
        
        return str(filepath)
    
    def save_measurements(self, measurements: List[LatencyMeasurement],
                          test_name: str = "",
                          statistics: dict = None) -> str:
        """
        Save measurements using configured format
        
        Args:
            measurements: List of latency measurements
            test_name: Optional test name/description
            statistics: Optional statistics dictionary
            
        Returns:
            Path to saved file
        """
        if self.config.log_format == "json":
            return self.save_measurements_json(measurements, test_name, statistics)
        else:
            return self.save_measurements_csv(measurements, test_name)
    
    def load_measurements_csv(self, filepath: str) -> List[dict]:
        """
        Load measurements from CSV file
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            List of measurement dictionaries
        """
        measurements = []
        with open(filepath, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    # Skip metadata rows
                    int(row['timestamp'])
                    measurements.append(row)
                except (ValueError, KeyError):
                    continue
        return measurements
    
    def load_measurements_json(self, filepath: str) -> dict:
        """
        Load measurements from JSON file
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            Dictionary with measurements and metadata
        """
        with open(filepath, 'r') as jsonfile:
            return json.load(jsonfile)
