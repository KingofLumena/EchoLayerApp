# Contributing to EchoLayerApp

Thank you for your interest in contributing to EchoLayerApp!

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/EchoLayerApp.git
   cd EchoLayerApp
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Project Structure

```
EchoLayerApp/
├── echolayer/              # Main package
│   ├── audio/             # Audio processing and latency measurement
│   ├── layers/            # Signal layer implementations
│   ├── logging/           # Result logging
│   ├── gui/               # Streamlit GUI
│   └── config.py          # Configuration management
├── tests/                 # Test files
├── logs/                  # Output logs (gitignored)
├── app.py                 # Main entry point
└── examples.py            # Usage examples
```

## Adding New Input Layers

The modular design makes it easy to add new signal layers:

1. **Create a new layer class** in `echolayer/layers/`:

   ```python
   # echolayer/layers/mysignal.py
   import numpy as np
   
   class MySignalLayer:
       def __init__(self, sample_rate: int, **kwargs):
           self.sample_rate = sample_rate
           # Your initialization
       
       def generate(self, num_samples: int, channels: int = 2) -> np.ndarray:
           """Generate your signal"""
           # Your signal generation logic
           return signal
       
       def apply_to_signal(self, audio_signal: np.ndarray) -> np.ndarray:
           """Apply your layer to existing audio"""
           num_samples, channels = audio_signal.shape
           my_signal = self.generate(num_samples, channels)
           return audio_signal + my_signal
   ```

2. **Update AudioProcessor** to support your layer:

   ```python
   # In echolayer/audio/processor.py
   def enable_mysignal_layer(self, **kwargs):
       from ..layers.mysignal import MySignalLayer
       self.mysignal_layer = MySignalLayer(
           sample_rate=self.config.sample_rate,
           **kwargs
       )
   ```

3. **Add configuration** in `echolayer/config.py`:

   ```python
   @dataclass
   class MySignalConfig:
       param1: int = 100
       param2: float = 0.5
       enabled: bool = False
   ```

4. **Add GUI controls** in `echolayer/gui/streamlit_app.py`:

   ```python
   def render_mysignal_config(self):
       with st.expander("🎵 My Signal Settings"):
           config = st.session_state.config.mysignal
           config.param1 = st.slider("Parameter 1", ...)
   ```

## Testing

Run tests before submitting:

```bash
# Integration tests
PYTHONPATH=. python tests/test_integration.py

# Test examples
python examples.py

# Test GUI (launches in browser)
streamlit run app.py
```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints for function parameters and returns
- Add docstrings to classes and functions
- Keep functions focused and modular

## Example Layer Ideas

- **Low-frequency layers**: Sub-bass frequencies
- **Pink noise layers**: 1/f noise patterns
- **Chirp signals**: Frequency sweeps
- **Amplitude modulation**: AM signals
- **Phase modulation**: PM signals
- **Multi-tone layers**: Multiple simultaneous frequencies
- **Noise patterns**: Various noise types (white, brown, etc.)

## Submitting Changes

1. Test your changes thoroughly
2. Update documentation if needed
3. Commit with clear messages:
   ```bash
   git commit -m "Add MySignal layer for testing XYZ"
   ```
4. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Create a Pull Request on GitHub

## Questions?

Open an issue on GitHub for:
- Bug reports
- Feature requests
- Questions about implementation
- Ideas for new layers

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
