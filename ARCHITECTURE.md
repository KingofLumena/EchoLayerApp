# EchoLayerApp Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        EchoLayerApp                             │
│              Audio Latency Benchmarking System                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     User Interface (GUI)                         │
│                    echolayer/gui/                                │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Mode A/B    │  │    Config    │  │   Results    │         │
│  │   Toggle     │  │   Controls   │  │   Display    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────────┐
│                  Configuration Management                        │
│                    echolayer/config.py                           │
│                                                                  │
│  AudioConfig | UltrasonicLayerConfig | LoggingConfig           │
└─────────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────────┐
│                   Audio Processing Layer                         │
│                  echolayer/audio/processor.py                    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  AudioProcessor                                          │   │
│  │  • Stream management (sounddevice)                       │   │
│  │  • Latency measurement (time.monotonic_ns)              │   │
│  │  • Signal processing pipeline                            │   │
│  │  • Statistics calculation                                │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                ↕                                   ↕
┌──────────────────────────┐    ┌──────────────────────────────┐
│   Signal Layers          │    │   Logging System             │
│   echolayer/layers/      │    │   echolayer/logging/         │
│                          │    │                              │
│  ┌──────────────────┐   │    │  ┌──────────────────────┐   │
│  │ UltrasonicLayer  │   │    │  │  LatencyLogger       │   │
│  │ • 18-22 kHz gen  │   │    │  │  • CSV export        │   │
│  │ • Phase tracking │   │    │  │  • JSON export       │   │
│  │ • Stereo output  │   │    │  │  • Metadata          │   │
│  └──────────────────┘   │    │  └──────────────────────┘   │
│                          │    │                              │
│  [Extensible for more    │    └──────────────────────────────┘
│   layer types]           │                 ↓
└──────────────────────────┘         ┌─────────────┐
                                      │ logs/*.csv  │
                                      │ logs/*.json │
                                      └─────────────┘
```

## Data Flow

### Latency Measurement Flow

```
1. Audio Input
   ↓
2. Timestamp (time.monotonic_ns)  ← Input Timestamp
   ↓
3. Signal Processing
   ├─ Mode A: Pass-through
   └─ Mode B: + Ultrasonic Layer
   ↓
4. Audio Output
   ↓
5. Timestamp (time.monotonic_ns)  ← Output Timestamp
   ↓
6. Calculate Latency (Output - Input)
   ↓
7. Store Measurement
   ↓
8. Update Statistics & Display
```

### A/B Testing Workflow

```
┌──────────────┐
│  Mode A      │  Baseline (No Ultrasonic)
│  Baseline    │  ↓
└──────────────┘  Run Test → Collect Data → Save Results
                  
┌──────────────┐
│  Mode B      │  With Ultrasonic Layer (18-22 kHz)
│  Ultrasonic  │  ↓
└──────────────┘  Run Test → Collect Data → Save Results

                  ↓
            Compare Results
              ↓
     Analyze Latency Impact
```

## Component Interactions

```
app.py (Entry Point)
    ↓
EchoLayerGUI.run()
    ↓
    ├─→ render_ab_testing_controls()
    │   ├─→ processor.enable_ultrasonic_layer()
    │   └─→ processor.disable_ultrasonic_layer()
    │
    ├─→ render_test_controls()
    │   ├─→ processor.start_stream()
    │   │   └─→ _audio_callback()
    │   │       ├─→ time.monotonic_ns()
    │   │       ├─→ ultrasonic_layer.apply_to_signal()
    │   │       ├─→ time.monotonic_ns()
    │   │       └─→ store measurement
    │   └─→ processor.stop_stream()
    │
    ├─→ render_live_statistics()
    │   └─→ processor.get_statistics()
    │
    └─→ save_results()
        └─→ logger.save_measurements()
            ├─→ CSV format
            └─→ JSON format
```

## Module Responsibilities

### echolayer/config.py
- Define configuration dataclasses
- Manage application settings
- Provide defaults

### echolayer/audio/processor.py
- Audio stream management
- Latency measurement
- Signal processing
- Statistics calculation
- Device enumeration

### echolayer/layers/ultrasonic.py
- Generate ultrasonic signals
- Apply layers to audio
- Phase continuity management
- Multi-channel support

### echolayer/logging/logger.py
- Save measurements to files
- Load historical data
- Format conversion (CSV/JSON)
- Timestamp management

### echolayer/gui/streamlit_app.py
- User interface
- Control interactions
- Real-time visualization
- Configuration management

## Extension Points

The architecture supports easy extension:

1. **New Signal Layers**: Add classes in `echolayer/layers/`
2. **Custom Processing**: Extend `AudioProcessor`
3. **Additional Formats**: Extend `LatencyLogger`
4. **UI Enhancements**: Modify `streamlit_app.py`
5. **New Metrics**: Add to `LatencyMeasurement`

## Performance Characteristics

- **Latency Measurement**: Nanosecond precision (time.monotonic_ns)
- **Audio Processing**: Real-time with configurable chunk size
- **Memory Usage**: Measurements stored in-memory during test
- **File I/O**: Async write after test completion
- **GUI Updates**: 500ms refresh rate during testing

## Cross-Platform Support

- **Windows**: Full support via sounddevice
- **macOS**: Full support via sounddevice
- **Linux**: Full support (requires PortAudio)
- **GUI**: Browser-based (Streamlit) - platform agnostic
