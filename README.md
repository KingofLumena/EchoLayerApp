# EchoLayerApp 🔊

Acoustic optimization layer benchmark — measuring firmware-agnostic latency effects

## Overview

EchoLayerApp is a cross-platform audio latency benchmarking tool designed to measure latency shifts caused by ultrasonic signal layers. It features real-time latency logging using high-precision nanosecond timestamps, A/B testing capabilities, and a user-friendly Streamlit GUI.

## Features

- **🎯 A/B Testing**: Toggle between baseline (Mode A) and ultrasonic layer (Mode B) to compare latency impacts
- **⏱️ Precision Timing**: Real-time latency measurement using `time.monotonic_ns()` for nanosecond accuracy
- **🔊 Audio Processing**: Built on sounddevice for reliable cross-platform audio I/O
- **🌊 Ultrasonic Layers**: Configurable ultrasonic frequency overlay (18-22 kHz) for testing
- **📊 Live Statistics**: Real-time visualization of latency measurements and statistics
- **💾 Data Logging**: Save results to CSV or JSON files with timestamps and metadata
- **🖥️ Cross-Platform GUI**: Streamlit-based interface works on Windows, macOS, and Linux
- **🔧 Modular Design**: Extensible architecture for adding custom input layers

## Installation

### Prerequisites

- Python 3.8 or higher
- Working audio input/output devices

### Setup

1. Clone the repository:
```bash
git clone https://github.com/KingofLumena/EchoLayerApp.git
cd EchoLayerApp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Application

Run the Streamlit GUI:
```bash
streamlit run app.py
```

Or directly:
```bash
python -m streamlit run echolayer/gui/streamlit_app.py
```

### Running Tests

1. **Select Test Mode**:
   - Click "🔵 Test Mode A (No Ultrasonic)" for baseline measurements
   - Click "🟢 Test Mode B (With Ultrasonic)" to test with ultrasonic layer

2. **Configure Settings** (Optional):
   - Expand "⚙️ Audio Configuration" to adjust sample rate, channels, and device
   - Expand "🌊 Ultrasonic Layer Settings" to modify frequency and amplitude

3. **Run Test**:
   - Click "▶️ Start Test" to begin latency measurements
   - Watch live statistics update in real-time
   - Click "⏹️ Stop Test" when complete

4. **Save Results**:
   - Click "💾 Save Results" to export measurements
   - Files are saved to the `logs/` directory with timestamps

## Project Structure

```
EchoLayerApp/
├── app.py                          # Main entry point
├── requirements.txt                # Python dependencies
├── logs/                           # Test result logs (auto-generated)
├── echolayer/
│   ├── __init__.py
│   ├── config.py                   # Configuration dataclasses
│   ├── audio/
│   │   ├── __init__.py
│   │   └── processor.py            # Audio processing & latency measurement
│   ├── layers/
│   │   ├── __init__.py
│   │   └── ultrasonic.py           # Ultrasonic signal generation
│   ├── logging/
│   │   ├── __init__.py
│   │   └── logger.py               # Result logging (CSV/JSON)
│   └── gui/
│       ├── __init__.py
│       └── streamlit_app.py        # Streamlit GUI interface
└── tests/                          # Test files (if added)
```

## Architecture

### Core Components

1. **AudioProcessor** (`echolayer/audio/processor.py`)
   - Manages audio stream with sounddevice
   - Measures latency using `time.monotonic_ns()`
   - Applies optional ultrasonic layers
   - Collects and aggregates measurements

2. **UltrasonicLayer** (`echolayer/layers/ultrasonic.py`)
   - Generates ultrasonic sine waves (18-22 kHz)
   - Maintains phase continuity across chunks
   - Applies layers to audio signals

3. **LatencyLogger** (`echolayer/logging/logger.py`)
   - Saves measurements to CSV or JSON
   - Includes timestamps and metadata
   - Supports loading historical data

4. **EchoLayerGUI** (`echolayer/gui/streamlit_app.py`)
   - Streamlit-based user interface
   - Live statistics and visualization
   - Configuration controls
   - Test management

## Configuration

Configuration is managed through dataclasses in `config.py`:

- **AudioConfig**: Sample rate, channels, chunk size, device selection
- **UltrasonicLayerConfig**: Frequency, amplitude, enable/disable
- **LoggingConfig**: Log directory, file prefix, format (CSV/JSON)

## Extending the Application

### Adding New Input Layers

The modular design allows easy addition of new signal layers:

1. Create a new layer class in `echolayer/layers/`
2. Implement `generate()` and `apply_to_signal()` methods
3. Update `AudioProcessor` to support the new layer type
4. Add GUI controls in `streamlit_app.py`

Example:
```python
class CustomLayer:
    def apply_to_signal(self, audio_signal):
        # Your processing logic
        return modified_signal
```

## Technical Details

### Latency Measurement

Latency is measured as the time difference between:
- **Input timestamp**: When audio data is received (`time.monotonic_ns()`)
- **Output timestamp**: When processed audio is sent out (`time.monotonic_ns()`)

This provides the processing latency in nanoseconds, converted to milliseconds for display.

### Ultrasonic Layer

- Default frequency: 20 kHz (configurable 18-22 kHz)
- Amplitude: 0.1 (10%, configurable 0.01-0.5)
- Phase-continuous sine wave generation
- Stereo support with identical signal on both channels

## Requirements

- numpy>=1.21.0
- sounddevice>=0.4.6
- streamlit>=1.28.0
- pandas>=1.3.0

## License

See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## Troubleshooting

### No Audio Devices Found
- Ensure your audio devices are properly connected
- Check system audio settings
- Try selecting a specific device in Audio Configuration

### Permission Errors
- Ensure the application has permission to access your microphone
- Check system privacy settings

### High Latency Values
- Try reducing chunk size in Audio Configuration
- Close other audio applications
- Use a lower sample rate if needed

## Support

For issues and questions, please open an issue on GitHub.
