# EchoLayerApp Usage Guide

## Quick Start

### Installation
```bash
# Clone and install dependencies
git clone https://github.com/KingofLumena/EchoLayerApp.git
cd EchoLayerApp
pip install -r requirements.txt

# System requirements
# Linux: sudo apt-get install portaudio19-dev python3-tk
# Windows: No additional requirements (included with Python)
# macOS: brew install portaudio
```

### First Run
```bash
# Check audio devices
python run.py info

# Run demo (no audio hardware required)
python demo.py

# Launch GUI
python run.py --gui
```

## Command-Line Interface (CLI)

### Available Commands

#### 1. Device Information
```bash
python run.py info
```
Shows available audio input/output devices on your system.

#### 2. Play Test Tone
```bash
# Basic tone
python run.py play --frequency 1000

# Tone with ultrasonic overlay
python run.py play --frequency 1000 --overlay 20000 --amplitude 0.3
```

**Options:**
- `--frequency FREQ`: Base frequency in Hz (default: 1000)
- `--overlay FREQ`: Overlay frequency in Hz (0 to disable, default: 0)
- `--amplitude AMP`: Amplitude 0.0-1.0 (default: 0.3)

#### 3. Latency Test
```bash
python run.py test --frequency 1000 --overlay 20000 --iterations 10
```

Runs multiple iterations and measures latency for each. Results include:
- Per-iteration latency in milliseconds
- Statistical summary (mean, median, min, max, std dev)
- Automatic logging to JSON file

**Options:**
- `--frequency FREQ`: Base frequency in Hz (default: 1000)
- `--overlay FREQ`: Overlay frequency in Hz (default: 20000)
- `--iterations N`: Number of test iterations (default: 10)
- `--output FILE`: Custom output filename

**Example:**
```bash
# Test with 20 iterations
python run.py test --frequency 1000 --overlay 20000 --iterations 20 --output my_test.json
```

#### 4. A/B Comparison Test
```bash
python run.py ab-test \
  --freq-a 1000 --overlay-a 0 \
  --freq-b 1000 --overlay-b 20000 \
  --iterations 10
```

Compares two different audio configurations to measure the latency impact of ultrasonic overlays.

**Options:**
- `--freq-a FREQ`: Test A base frequency (default: 1000)
- `--overlay-a FREQ`: Test A overlay frequency (default: 0)
- `--freq-b FREQ`: Test B base frequency (default: 1000)
- `--overlay-b FREQ`: Test B overlay frequency (default: 20000)
- `--iterations N`: Iterations per test (default: 10)
- `--output FILE`: Custom output filename

**Example Use Cases:**
```bash
# Compare baseline vs 20kHz overlay
python run.py ab-test --freq-a 1000 --overlay-a 0 --freq-b 1000 --overlay-b 20000

# Compare different overlay frequencies
python run.py ab-test --freq-a 1000 --overlay-a 18000 --freq-b 1000 --overlay-b 22000

# Test with more iterations for accuracy
python run.py ab-test --iterations 50 --output detailed_comparison.json
```

## Graphical User Interface (GUI)

### Launch GUI
```bash
python run.py --gui
```

### GUI Features

#### Tab 1: Single Test
- Configure base frequency and overlay frequency
- Set number of iterations
- Run test and view real-time results
- Play test tones to hear the difference
- Statistics displayed automatically

#### Tab 2: A/B Test
- Configure two test scenarios (A and B)
- Set iterations for each test
- Compare results side-by-side
- View which configuration has lower latency
- Percentage difference calculation

#### Tab 3: Results
- Browse log files
- View audio device information
- Open log directory in file explorer
- Refresh device list

### GUI Tips
- Use "Play Tone" in Single Test tab to preview audio
- Results appear in real-time during testing
- All tests are automatically logged
- Use threading to avoid blocking the UI

## Output Files

All results are saved in the `logs/` directory:

### JSON Format
```json
{
  "timestamp": "2025-11-19T12:30:00.123456",
  "measurements": [
    {
      "total_latency_ns": 1234567,
      "schedule_latency_ns": 456789,
      "playback_duration_ns": 777778,
      "timestamp_ns": 123456789
    }
  ]
}
```

### CSV Format
```csv
total_latency_ns,schedule_latency_ns,playback_duration_ns,timestamp_ns
1234567,456789,777778,123456789
1245678,467890,777788,234567890
```

## Configuration

Create a `config.json` file based on `config.example.json`:

```json
{
  "audio": {
    "sample_rate": 44100,
    "duration": 1.0,
    "amplitude": 0.3
  },
  "test": {
    "iterations": 10,
    "base_frequency": 1000,
    "ultrasonic_frequency": 20000
  },
  "logging": {
    "log_dir": "logs",
    "format": "json"
  },
  "gui": {
    "window_title": "EchoLayerApp - Latency Benchmark",
    "window_size": "800x600"
  }
}
```

## Advanced Usage

### Python API
```python
from echolayerapp import AudioEngine, ABTest, LatencyLogger

# Initialize components
engine = AudioEngine(sample_rate=44100, duration=1.0)
logger = LatencyLogger(log_dir="my_logs")

# Generate audio
tone = engine.generate_tone(1000, amplitude=0.5)
overlay = engine.generate_ultrasonic_overlay(1000, 20000, amplitude=0.3)

# Measure latency
measurement = engine.play_audio(tone, blocking=True)
print(f"Latency: {measurement['total_latency_ns'] / 1_000_000:.2f} ms")

# Run A/B test
ab_test = ABTest(engine)
config_a = {'base_freq': 1000, 'overlay_freq': 0}
config_b = {'base_freq': 1000, 'overlay_freq': 20000}
results = ab_test.run_test(config_a, config_b, iterations=10)

# Log results
logger.log_ab_test_results(results)
```

### Custom Analysis
```python
import json

# Load results
with open('logs/ab_test_results_20231119_123456.json', 'r') as f:
    data = json.load(f)

# Analyze
stats_a = data['results']['A']['stats']
stats_b = data['results']['B']['stats']

print(f"Configuration A: {stats_a['mean_latency_ms']:.2f} ms")
print(f"Configuration B: {stats_b['mean_latency_ms']:.2f} ms")
```

## Troubleshooting

### No Audio Output
- Check device with `python run.py info`
- Verify speakers/headphones are connected
- Try different output devices in system settings
- On Linux, check PulseAudio/ALSA configuration

### "PortAudio library not found"
- **Linux**: `sudo apt-get install portaudio19-dev`
- **macOS**: `brew install portaudio`
- **Windows**: Reinstall sounddevice: `pip install --upgrade sounddevice`

### GUI Won't Launch
- Ensure Tkinter is installed: `python -m tkinter`
- **Linux**: `sudo apt-get install python3-tk`
- Try running from terminal to see error messages

### High Latency Measurements
- Close other audio applications
- Increase audio buffer size in system settings
- Use lower sample rate (edit config.json)
- Check CPU usage during tests

### Inconsistent Results
- Increase number of iterations (--iterations 50)
- Close background applications
- Run tests multiple times and average results
- Check for thermal throttling on laptop

## Best Practices

1. **Baseline First**: Always run a baseline test (no overlay) before testing with overlays
2. **Multiple Iterations**: Use at least 10 iterations, 50+ for critical measurements
3. **Consistent Environment**: Keep system load similar across tests
4. **Document Setup**: Note hardware, OS version, and audio configuration
5. **Log Everything**: Use custom output names to track different configurations
6. **Regular Calibration**: Run known-good tests periodically to verify system

## Example Workflows

### Workflow 1: Basic Latency Measurement
```bash
# 1. Check devices
python run.py info

# 2. Run baseline
python run.py test --frequency 1000 --overlay 0 --iterations 20 --output baseline.json

# 3. Run with overlay
python run.py test --frequency 1000 --overlay 20000 --iterations 20 --output overlay_20khz.json

# 4. Compare results manually or use A/B test
```

### Workflow 2: Overlay Frequency Sweep
```bash
# Test different overlay frequencies
for freq in 18000 19000 20000 21000 22000; do
  python run.py test --frequency 1000 --overlay $freq --iterations 20 --output overlay_${freq}hz.json
done
```

### Workflow 3: Statistical Analysis
```bash
# Run comprehensive A/B test
python run.py ab-test --iterations 100 --output comprehensive_test.json

# Results automatically include statistical measures
```

## Performance Tips

- **Sample Rate**: Lower sample rates (22050 Hz) reduce CPU load
- **Duration**: Shorter durations (0.5s) speed up testing
- **Iterations**: Balance between accuracy and time
- **Amplitude**: Lower amplitudes (0.2-0.3) are safer for testing

## Safety Notes

⚠️ **Always start with low amplitude settings (0.2-0.3)**
⚠️ **Ultrasonic frequencies may not be audible but can still affect speakers**
⚠️ **Keep volume at reasonable levels during testing**
⚠️ **Stop immediately if you hear distortion or clipping**
