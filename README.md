# EchoLayerApp

Acoustic optimization layer benchmark — measuring firmware-agnostic latency effects

## Overview

EchoLayerApp is a Python application designed to benchmark latency effects of ultrasonic overlays in audio playback. It provides both command-line and graphical interfaces for running tests, measuring latency with nanosecond precision, and comparing different audio configurations through A/B testing.

## Features

- **Audio Playback**: Generate and play audio tones with optional ultrasonic overlays using sounddevice
- **High-Precision Latency Measurement**: Uses `time.monotonic_ns()` for nanosecond-accurate timing
- **A/B Testing Framework**: Compare latency between different audio configurations
- **Dual Interface**: Both CLI and GUI (Tkinter) interfaces
- **Comprehensive Logging**: Export results to JSON and CSV formats
- **Cross-Platform**: Runs on Windows and Linux (macOS supported)
- **Modular Architecture**: Separated audio engine, test framework, and interface layers

## Installation

### Prerequisites

- Python 3.7 or higher
- PortAudio library (required by sounddevice)

#### Installing PortAudio

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install portaudio19-dev python3-tk
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install portaudio-devel python3-tkinter
```

**Windows:**
PortAudio binaries are included with the sounddevice package. Tkinter is included with Python.

**macOS:**
```bash
brew install portaudio
```

### Install EchoLayerApp

1. Clone the repository:
```bash
git clone https://github.com/KingofLumena/EchoLayerApp.git
cd EchoLayerApp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Install as package:
```bash
pip install -e .
```

## Usage

### Graphical User Interface (GUI)

Launch the GUI with:
```bash
python run.py --gui
# or if installed as package:
echolayerapp --gui
```

The GUI provides three tabs:
- **Single Test**: Run latency tests with customizable parameters
- **A/B Test**: Compare two audio configurations side-by-side
- **Results**: View log files and audio device information

### Command-Line Interface (CLI)

#### Show Audio Device Information
```bash
python run.py info
```

#### Play a Test Tone
```bash
python run.py play --frequency 1000 --overlay 20000 --amplitude 0.3
```

#### Run a Latency Test
```bash
python run.py test --frequency 1000 --overlay 20000 --iterations 10
```

#### Run an A/B Test
```bash
python run.py ab-test \
  --freq-a 1000 --overlay-a 0 \
  --freq-b 1000 --overlay-b 20000 \
  --iterations 10
```

### CLI Command Reference

**Commands:**
- `info` - Display audio device information
- `play` - Play a test tone
- `test` - Run a latency benchmark test
- `ab-test` - Run an A/B comparison test

**Common Options:**
- `--frequency FREQ` - Base frequency in Hz (default: 1000)
- `--overlay FREQ` - Overlay frequency in Hz (0 to disable, default: 20000)
- `--amplitude AMP` - Amplitude 0.0-1.0 (default: 0.3)
- `--iterations N` - Number of test iterations (default: 10)
- `--output FILE` - Custom output log filename

## Project Structure

```
EchoLayerApp/
├── echolayerapp/
│   ├── __init__.py           # Package initialization
│   ├── __main__.py           # Main entry point
│   ├── core/                 # Core functionality
│   │   ├── audio_engine.py   # Audio generation and playback
│   │   └── ab_test.py        # A/B testing framework
│   ├── interfaces/           # User interfaces
│   │   ├── cli.py            # Command-line interface
│   │   └── gui.py            # Graphical interface (Tkinter)
│   └── utils/                # Utility modules
│       ├── config.py         # Configuration management
│       └── logger.py         # Logging utilities
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup script
├── run.py                    # Convenience runner script
└── README.md                 # This file
```

## Output Files

All test results are saved to the `logs/` directory by default:

- **JSON format**: Detailed measurement data with timestamps
- **CSV format**: Tabular data for spreadsheet analysis
- **Log files**: Text-based activity logs

## Technical Details

### Latency Measurement

The application measures three types of latency:
1. **Schedule Latency**: Time to schedule audio playback
2. **Playback Duration**: Total time for audio to play
3. **Total Latency**: Combined scheduling and playback time

All measurements use `time.monotonic_ns()` for nanosecond precision and monotonic timing.

### Audio Generation

- **Base Tones**: Pure sine waves at specified frequencies
- **Ultrasonic Overlays**: Mixed tones combining base frequency with ultrasonic range (>20kHz)
- **Sample Rate**: 44.1 kHz (configurable)
- **Amplitude Normalization**: Automatic prevention of clipping

### A/B Testing

The A/B test framework:
- Runs multiple iterations of each configuration
- Calculates statistical measures (mean, median, min, max, std dev)
- Determines percentage difference between configurations
- Identifies the lower-latency configuration

## Cross-Platform Compatibility

The application is designed to run on:
- **Linux**: Tested on Ubuntu and Fedora
- **Windows**: Windows 10/11
- **macOS**: Big Sur and later

Note: Tkinter is included with most Python installations. On Linux, you may need to install it separately (python3-tk package).

## Troubleshooting

### "No module named 'sounddevice'"
Install dependencies: `pip install -r requirements.txt`

### "PortAudio library not found"
Install PortAudio for your platform (see Installation section)

### GUI doesn't launch
Ensure Tkinter is installed: `python -m tkinter` (should open a test window)

### No audio output
- Check audio device settings with `python run.py info`
- Verify speakers/headphones are connected and unmuted
- Try different output devices in system settings

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.
