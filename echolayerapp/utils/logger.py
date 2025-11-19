"""
Logging utilities for EchoLayerApp.
Handles latency measurements and results logging.
"""

import json
import csv
import os
from datetime import datetime
from typing import Dict, List, Optional


class LatencyLogger:
    """Logger for latency measurements and test results."""
    
    def __init__(self, log_dir: str = "logs"):
        """
        Initialize the latency logger.
        
        Args:
            log_dir: Directory for log files (default "logs")
        """
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
    def log_measurements(self, measurements: List[Dict], 
                        filename: Optional[str] = None,
                        format: str = 'json') -> str:
        """
        Log latency measurements to file.
        
        Args:
            measurements: List of measurement dictionaries
            filename: Output filename (auto-generated if None)
            format: Output format ('json' or 'csv')
            
        Returns:
            Path to the log file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ext = 'json' if format == 'json' else 'csv'
            filename = f"latency_measurements_{timestamp}.{ext}"
        
        filepath = os.path.join(self.log_dir, filename)
        
        if format == 'json':
            self._log_json(measurements, filepath)
        elif format == 'csv':
            self._log_csv(measurements, filepath)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        return filepath
    
    def _log_json(self, measurements: List[Dict], filepath: str):
        """Log measurements in JSON format."""
        with open(filepath, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'measurements': measurements
            }, f, indent=2)
    
    def _log_csv(self, measurements: List[Dict], filepath: str):
        """Log measurements in CSV format."""
        if not measurements:
            return
        
        # Get all keys from measurements
        fieldnames = set()
        for m in measurements:
            fieldnames.update(m.keys())
        fieldnames = sorted(fieldnames)
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(measurements)
    
    def log_ab_test_results(self, test_results: Dict, 
                           filename: Optional[str] = None) -> str:
        """
        Log A/B test results to JSON file.
        
        Args:
            test_results: A/B test results dictionary
            filename: Output filename (auto-generated if None)
            
        Returns:
            Path to the log file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ab_test_results_{timestamp}.json"
        
        filepath = os.path.join(self.log_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'results': test_results
            }, f, indent=2)
        
        return filepath
    
    def log_text(self, message: str, filename: str = "echolayer.log"):
        """
        Append text message to log file.
        
        Args:
            message: Message to log
            filename: Log filename
        """
        filepath = os.path.join(self.log_dir, filename)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(filepath, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")
    
    def get_log_files(self) -> List[str]:
        """
        Get list of log files in the log directory.
        
        Returns:
            List of log file paths
        """
        if not os.path.exists(self.log_dir):
            return []
        
        files = [os.path.join(self.log_dir, f) 
                for f in os.listdir(self.log_dir) 
                if os.path.isfile(os.path.join(self.log_dir, f))]
        return sorted(files, key=os.path.getmtime, reverse=True)
