"""
Graphical user interface for EchoLayerApp using Tkinter.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from ..core.audio_engine import AudioEngine
from ..core.ab_test import ABTest
from ..utils.logger import LatencyLogger
from ..utils.config import Config


class GUI:
    """Tkinter-based GUI for EchoLayerApp."""
    
    def __init__(self, root):
        """
        Initialize the GUI.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.config = Config()
        
        # Initialize components
        self.audio_engine = AudioEngine(
            sample_rate=self.config.get('audio.sample_rate'),
            duration=self.config.get('audio.duration')
        )
        self.logger = LatencyLogger(
            log_dir=self.config.get('logging.log_dir')
        )
        
        # Setup UI
        self.root.title(self.config.get('gui.window_title'))
        self.root.geometry(self.config.get('gui.window_size'))
        
        self._create_widgets()
        self._layout_widgets()
    
    def _create_widgets(self):
        """Create GUI widgets."""
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        
        # Tab 1: Single Test
        self.tab_single = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_single, text='Single Test')
        self._create_single_test_tab()
        
        # Tab 2: A/B Test
        self.tab_ab = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ab, text='A/B Test')
        self._create_ab_test_tab()
        
        # Tab 3: Results
        self.tab_results = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_results, text='Results')
        self._create_results_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                                    relief=tk.SUNKEN, anchor=tk.W)
    
    def _create_single_test_tab(self):
        """Create single test tab widgets."""
        # Configuration frame
        config_frame = ttk.LabelFrame(self.tab_single, text="Test Configuration", padding=10)
        
        ttk.Label(config_frame, text="Base Frequency (Hz):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.single_freq_var = tk.StringVar(value="1000")
        ttk.Entry(config_frame, textvariable=self.single_freq_var, width=15).grid(row=0, column=1, pady=5)
        
        ttk.Label(config_frame, text="Overlay Frequency (Hz):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.single_overlay_var = tk.StringVar(value="20000")
        ttk.Entry(config_frame, textvariable=self.single_overlay_var, width=15).grid(row=1, column=1, pady=5)
        
        ttk.Label(config_frame, text="Iterations:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.single_iterations_var = tk.StringVar(value="10")
        ttk.Entry(config_frame, textvariable=self.single_iterations_var, width=15).grid(row=2, column=1, pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(self.tab_single, padding=10)
        ttk.Button(button_frame, text="Run Test", command=self._run_single_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Play Tone", command=self._play_test_tone).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self._clear_single_results).pack(side=tk.LEFT, padx=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(self.tab_single, text="Results", padding=10)
        self.single_results_text = scrolledtext.ScrolledText(results_frame, height=15, width=70)
        self.single_results_text.pack(fill=tk.BOTH, expand=True)
        
        # Layout
        config_frame.pack(fill=tk.X, padx=10, pady=10)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def _create_ab_test_tab(self):
        """Create A/B test tab widgets."""
        # Configuration frame
        config_frame = ttk.LabelFrame(self.tab_ab, text="A/B Test Configuration", padding=10)
        
        # Test A
        ttk.Label(config_frame, text="Test A", font=('', 10, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)
        ttk.Label(config_frame, text="Base Frequency (Hz):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.ab_freq_a_var = tk.StringVar(value="1000")
        ttk.Entry(config_frame, textvariable=self.ab_freq_a_var, width=15).grid(row=1, column=1, pady=5)
        
        ttk.Label(config_frame, text="Overlay Frequency (Hz):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.ab_overlay_a_var = tk.StringVar(value="0")
        ttk.Entry(config_frame, textvariable=self.ab_overlay_a_var, width=15).grid(row=2, column=1, pady=5)
        
        # Test B
        ttk.Label(config_frame, text="Test B", font=('', 10, 'bold')).grid(row=3, column=0, columnspan=2, pady=(15, 5))
        ttk.Label(config_frame, text="Base Frequency (Hz):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.ab_freq_b_var = tk.StringVar(value="1000")
        ttk.Entry(config_frame, textvariable=self.ab_freq_b_var, width=15).grid(row=4, column=1, pady=5)
        
        ttk.Label(config_frame, text="Overlay Frequency (Hz):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.ab_overlay_b_var = tk.StringVar(value="20000")
        ttk.Entry(config_frame, textvariable=self.ab_overlay_b_var, width=15).grid(row=5, column=1, pady=5)
        
        # Iterations
        ttk.Label(config_frame, text="Iterations per test:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.ab_iterations_var = tk.StringVar(value="10")
        ttk.Entry(config_frame, textvariable=self.ab_iterations_var, width=15).grid(row=6, column=1, pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(self.tab_ab, padding=10)
        ttk.Button(button_frame, text="Run A/B Test", command=self._run_ab_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self._clear_ab_results).pack(side=tk.LEFT, padx=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(self.tab_ab, text="Results", padding=10)
        self.ab_results_text = scrolledtext.ScrolledText(results_frame, height=15, width=70)
        self.ab_results_text.pack(fill=tk.BOTH, expand=True)
        
        # Layout
        config_frame.pack(fill=tk.X, padx=10, pady=10)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def _create_results_tab(self):
        """Create results tab widgets."""
        # Info frame
        info_frame = ttk.LabelFrame(self.tab_results, text="Log Files", padding=10)
        
        ttk.Button(info_frame, text="Refresh Log List", 
                  command=self._refresh_log_list).pack(pady=5)
        
        self.log_list = tk.Listbox(info_frame, height=10)
        self.log_list.pack(fill=tk.BOTH, expand=True, pady=5)
        
        ttk.Button(info_frame, text="Open Log Directory", 
                  command=self._open_log_directory).pack(pady=5)
        
        # Device info frame
        device_frame = ttk.LabelFrame(self.tab_results, text="Device Information", padding=10)
        self.device_info_text = scrolledtext.ScrolledText(device_frame, height=8, width=70)
        self.device_info_text.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(device_frame, text="Refresh Device Info", 
                  command=self._show_device_info).pack(pady=5)
        
        # Layout
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        device_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initial load
        self._refresh_log_list()
        self._show_device_info()
    
    def _layout_widgets(self):
        """Layout main widgets."""
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def _run_single_test(self):
        """Run single latency test."""
        try:
            freq = float(self.single_freq_var.get())
            overlay = float(self.single_overlay_var.get())
            iterations = int(self.single_iterations_var.get())
            
            if iterations < 1:
                messagebox.showerror("Error", "Iterations must be at least 1")
                return
            
            # Run test in thread to avoid blocking UI
            thread = threading.Thread(
                target=self._single_test_worker,
                args=(freq, overlay, iterations)
            )
            thread.daemon = True
            thread.start()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
    
    def _single_test_worker(self, freq, overlay, iterations):
        """Worker function for single test."""
        self.status_var.set("Running test...")
        self.single_results_text.insert(tk.END, f"\n=== Running Test ===\n")
        self.single_results_text.insert(tk.END, f"Base: {freq} Hz, Overlay: {overlay} Hz\n")
        self.single_results_text.insert(tk.END, f"Iterations: {iterations}\n\n")
        
        self.audio_engine.clear_measurements()
        
        for i in range(iterations):
            if overlay > 0:
                audio = self.audio_engine.generate_ultrasonic_overlay(freq, overlay)
            else:
                audio = self.audio_engine.generate_tone(freq)
            
            measurement = self.audio_engine.play_audio(audio, blocking=True)
            
            if 'error' not in measurement:
                latency_ms = measurement['total_latency_ns'] / 1_000_000
                self.single_results_text.insert(tk.END, f"Iteration {i+1}: {latency_ms:.2f} ms\n")
                self.single_results_text.see(tk.END)
        
        # Calculate and display statistics
        measurements = self.audio_engine.get_measurements()
        self._display_statistics(self.single_results_text, measurements)
        
        # Log results
        filepath = self.logger.log_measurements(measurements)
        self.single_results_text.insert(tk.END, f"\nLogged to: {filepath}\n")
        self.single_results_text.see(tk.END)
        
        self.status_var.set("Test complete")
    
    def _run_ab_test(self):
        """Run A/B test."""
        try:
            freq_a = float(self.ab_freq_a_var.get())
            overlay_a = float(self.ab_overlay_a_var.get())
            freq_b = float(self.ab_freq_b_var.get())
            overlay_b = float(self.ab_overlay_b_var.get())
            iterations = int(self.ab_iterations_var.get())
            
            if iterations < 1:
                messagebox.showerror("Error", "Iterations must be at least 1")
                return
            
            # Run test in thread
            thread = threading.Thread(
                target=self._ab_test_worker,
                args=(freq_a, overlay_a, freq_b, overlay_b, iterations)
            )
            thread.daemon = True
            thread.start()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
    
    def _ab_test_worker(self, freq_a, overlay_a, freq_b, overlay_b, iterations):
        """Worker function for A/B test."""
        self.status_var.set("Running A/B test...")
        self.ab_results_text.insert(tk.END, f"\n=== Running A/B Test ===\n")
        self.ab_results_text.insert(tk.END, f"Test A: {freq_a} Hz (overlay: {overlay_a} Hz)\n")
        self.ab_results_text.insert(tk.END, f"Test B: {freq_b} Hz (overlay: {overlay_b} Hz)\n")
        self.ab_results_text.insert(tk.END, f"Iterations: {iterations}\n\n")
        
        ab_test = ABTest(self.audio_engine)
        
        config_a = {'base_freq': freq_a, 'overlay_freq': overlay_a}
        config_b = {'base_freq': freq_b, 'overlay_freq': overlay_b}
        
        results = ab_test.run_test(config_a, config_b, iterations)
        
        # Display results
        self.ab_results_text.insert(tk.END, "=== Results ===\n\n")
        self.ab_results_text.insert(tk.END, f"Test A - Mean Latency: {results['A']['stats']['mean_latency_ms']:.2f} ms\n")
        self.ab_results_text.insert(tk.END, f"Test B - Mean Latency: {results['B']['stats']['mean_latency_ms']:.2f} ms\n\n")
        
        comparison = ab_test.get_comparison()
        self.ab_results_text.insert(tk.END, f"Difference: {comparison['difference_ms']:.2f} ms ")
        self.ab_results_text.insert(tk.END, f"({comparison['percent_difference']:.1f}%)\n")
        self.ab_results_text.insert(tk.END, f"Winner: {comparison['winner']}\n")
        
        # Log results
        filepath = self.logger.log_ab_test_results(results)
        self.ab_results_text.insert(tk.END, f"\nLogged to: {filepath}\n")
        self.ab_results_text.see(tk.END)
        
        self.status_var.set("A/B test complete")
    
    def _play_test_tone(self):
        """Play a test tone."""
        try:
            freq = float(self.single_freq_var.get())
            overlay = float(self.single_overlay_var.get())
            
            self.status_var.set("Playing tone...")
            
            if overlay > 0:
                audio = self.audio_engine.generate_ultrasonic_overlay(freq, overlay)
            else:
                audio = self.audio_engine.generate_tone(freq)
            
            measurement = self.audio_engine.play_audio(audio, blocking=True)
            
            if 'error' in measurement:
                messagebox.showerror("Error", f"Playback error: {measurement['error']}")
            else:
                self.status_var.set("Playback complete")
                
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
    
    def _clear_single_results(self):
        """Clear single test results."""
        self.single_results_text.delete(1.0, tk.END)
        self.status_var.set("Results cleared")
    
    def _clear_ab_results(self):
        """Clear A/B test results."""
        self.ab_results_text.delete(1.0, tk.END)
        self.status_var.set("Results cleared")
    
    def _display_statistics(self, text_widget, measurements):
        """Display statistics in text widget."""
        if not measurements:
            return
        
        latencies = [m['total_latency_ns'] / 1_000_000 
                    for m in measurements if 'error' not in m]
        
        if not latencies:
            return
        
        import statistics
        
        text_widget.insert(tk.END, "\n=== Statistics ===\n")
        text_widget.insert(tk.END, f"Count: {len(latencies)}\n")
        text_widget.insert(tk.END, f"Mean: {statistics.mean(latencies):.2f} ms\n")
        text_widget.insert(tk.END, f"Median: {statistics.median(latencies):.2f} ms\n")
        text_widget.insert(tk.END, f"Min: {min(latencies):.2f} ms\n")
        text_widget.insert(tk.END, f"Max: {max(latencies):.2f} ms\n")
        if len(latencies) > 1:
            text_widget.insert(tk.END, f"Std Dev: {statistics.stdev(latencies):.2f} ms\n")
    
    def _refresh_log_list(self):
        """Refresh the log file list."""
        self.log_list.delete(0, tk.END)
        log_files = self.logger.get_log_files()
        
        for log_file in log_files:
            import os
            basename = os.path.basename(log_file)
            self.log_list.insert(tk.END, basename)
    
    def _open_log_directory(self):
        """Open the log directory in file explorer."""
        import os
        import subprocess
        import platform
        
        log_dir = self.logger.log_dir
        
        if not os.path.exists(log_dir):
            messagebox.showinfo("Info", f"Log directory does not exist: {log_dir}")
            return
        
        try:
            if platform.system() == 'Windows':
                os.startfile(log_dir)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.Popen(['open', log_dir])
            else:  # Linux
                subprocess.Popen(['xdg-open', log_dir])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open directory: {e}")
    
    def _show_device_info(self):
        """Show audio device information."""
        self.device_info_text.delete(1.0, tk.END)
        
        info = self.audio_engine.get_device_info()
        
        if 'error' in info:
            self.device_info_text.insert(tk.END, f"Error: {info['error']}\n")
            return
        
        self.device_info_text.insert(tk.END, "=== Audio Device Information ===\n\n")
        self.device_info_text.insert(tk.END, f"Default Input: {info.get('default_input', 'N/A')}\n")
        self.device_info_text.insert(tk.END, f"Default Output: {info.get('default_output', 'N/A')}\n\n")
        self.device_info_text.insert(tk.END, "Available Devices:\n")
        
        devices = info.get('devices', [])
        if isinstance(devices, dict):
            for idx, device in devices.items():
                self.device_info_text.insert(tk.END, f"  [{idx}] {device}\n")
        else:
            for idx, device in enumerate(devices):
                self.device_info_text.insert(tk.END, f"  [{idx}] {device}\n")


def main():
    """Main entry point for GUI."""
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
