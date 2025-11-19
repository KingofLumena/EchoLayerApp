# Quick Start Guide

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KingofLumena/EchoLayerApp.git
   cd EchoLayerApp
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   On Linux, you may also need to install PortAudio:
   ```bash
   sudo apt-get install portaudio19-dev
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```
   
   Or use the helper script:
   ```bash
   ./run.sh
   ```

## First Test

1. Open your browser to the URL shown (typically http://localhost:8501)

2. **Mode A - Baseline Test:**
   - Click "🔵 Test Mode A (No Ultrasonic)"
   - Click "▶️ Start Test"
   - Wait 10-30 seconds to collect data
   - Click "⏹️ Stop Test"
   - Review the statistics
   - Click "💾 Save Results"

3. **Mode B - Ultrasonic Test:**
   - Click "🟢 Test Mode B (With Ultrasonic)"
   - Click "▶️ Start Test"
   - Wait 10-30 seconds to collect data
   - Click "⏹️ Stop Test"
   - Review the statistics
   - Click "💾 Save Results"

4. **Compare Results:**
   - Check the `logs/` directory for saved CSV/JSON files
   - Compare mean latencies between Mode A and Mode B
   - Analyze the impact of the ultrasonic layer

## Configuration

Expand the configuration sections to customize:
- **Audio Configuration**: Sample rate, channels, chunk size, device selection
- **Ultrasonic Layer Settings**: Frequency (18-22 kHz), amplitude

## Examples

Run the examples script to see API usage:
```bash
python examples.py
```

## Testing

Run integration tests:
```bash
PYTHONPATH=. python tests/test_integration.py
```

## Troubleshooting

**No audio devices found:**
- Connect a microphone and/or speakers
- Check system audio settings
- Select a specific device in Audio Configuration

**Permission errors:**
- Grant microphone access in system privacy settings

**Import errors:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Install PortAudio if on Linux

## Results

Results are saved in `logs/` directory with timestamps:
- CSV format: Detailed measurements with headers
- JSON format: Includes measurements and statistics

## Next Steps

- Experiment with different ultrasonic frequencies (18-22 kHz)
- Try different sample rates and chunk sizes
- Compare results across different audio devices
- Analyze the latency impact of the ultrasonic layer
