"""
Example usage of EchoLayerApp components
This demonstrates how to use the API programmatically
"""
import time
import numpy as np
from echolayer.config import AppConfig, AudioConfig, UltrasonicLayerConfig, LoggingConfig
from echolayer.audio.processor import AudioProcessor, LatencyMeasurement
from echolayer.layers.ultrasonic import UltrasonicLayer
from echolayer.logging.logger import LatencyLogger


def example_ultrasonic_generation():
    """Example: Generate ultrasonic signal"""
    print("=" * 60)
    print("Example 1: Ultrasonic Signal Generation")
    print("=" * 60)
    
    # Create ultrasonic layer generator
    layer = UltrasonicLayer(
        sample_rate=48000,
        frequency=20000,  # 20 kHz
        amplitude=0.1     # 10% amplitude
    )
    
    # Generate 1024 samples for stereo
    signal = layer.generate(num_samples=1024, channels=2)
    
    print(f"Generated signal shape: {signal.shape}")
    print(f"Signal dtype: {signal.dtype}")
    print(f"Signal range: [{signal.min():.4f}, {signal.max():.4f}]")
    print()


def example_apply_ultrasonic():
    """Example: Apply ultrasonic layer to audio"""
    print("=" * 60)
    print("Example 2: Apply Ultrasonic Layer to Audio")
    print("=" * 60)
    
    # Create a synthetic audio signal (white noise)
    audio = np.random.randn(1024, 2).astype(np.float32) * 0.01
    print(f"Original audio range: [{audio.min():.4f}, {audio.max():.4f}]")
    
    # Create and apply ultrasonic layer
    layer = UltrasonicLayer(sample_rate=48000, frequency=20000, amplitude=0.1)
    result = layer.apply_to_signal(audio)
    
    print(f"With ultrasonic range: [{result.min():.4f}, {result.max():.4f}]")
    print(f"Difference: {np.abs(result - audio).max():.4f}")
    print()


def example_configuration():
    """Example: Working with configuration"""
    print("=" * 60)
    print("Example 3: Configuration Management")
    print("=" * 60)
    
    # Create default configuration
    config = AppConfig()
    print("Default Configuration:")
    print(f"  Sample Rate: {config.audio.sample_rate} Hz")
    print(f"  Channels: {config.audio.channels}")
    print(f"  Chunk Size: {config.audio.chunk_size}")
    print(f"  Ultrasonic Frequency: {config.ultrasonic.frequency} Hz")
    print(f"  Ultrasonic Amplitude: {config.ultrasonic.amplitude}")
    print()
    
    # Create custom configuration
    custom_config = AppConfig(
        audio=AudioConfig(
            sample_rate=44100,
            channels=1,
            chunk_size=512
        ),
        ultrasonic=UltrasonicLayerConfig(
            frequency=19000,
            amplitude=0.05,
            enabled=True
        )
    )
    print("Custom Configuration:")
    print(f"  Sample Rate: {custom_config.audio.sample_rate} Hz")
    print(f"  Channels: {custom_config.audio.channels}")
    print(f"  Chunk Size: {custom_config.audio.chunk_size}")
    print(f"  Ultrasonic Frequency: {custom_config.ultrasonic.frequency} Hz")
    print()


def example_latency_measurement():
    """Example: Create and work with latency measurements"""
    print("=" * 60)
    print("Example 4: Latency Measurement")
    print("=" * 60)
    
    # Simulate latency measurements
    measurements = []
    for i in range(5):
        m = LatencyMeasurement()
        m.input_timestamp = i * 1_000_000  # 1ms intervals
        m.output_timestamp = (i * 1_000_000) + 50_000 + i * 1000  # 50µs + increasing
        m.has_ultrasonic = i % 2 == 0
        m.calculate_latency()
        measurements.append(m)
        
        print(f"Measurement {i+1}:")
        print(f"  Latency: {m.latency_ns} ns ({m.latency_ms:.3f} ms)")
        print(f"  Has Ultrasonic: {m.has_ultrasonic}")
    print()


def example_audio_processor():
    """Example: AudioProcessor without stream (simulated)"""
    print("=" * 60)
    print("Example 5: AudioProcessor (Simulated)")
    print("=" * 60)
    
    config = AudioConfig(sample_rate=48000, channels=2)
    processor = AudioProcessor(config)
    
    # Test Mode A: Baseline (no ultrasonic)
    print("Mode A: Baseline")
    processor.disable_ultrasonic_layer()
    print(f"  Ultrasonic enabled: {processor.is_ultrasonic_enabled()}")
    
    # Simulate some measurements
    for i in range(10):
        m = LatencyMeasurement()
        m.input_timestamp = i * 1_000_000
        m.output_timestamp = (i * 1_000_000) + 45_000
        m.has_ultrasonic = False
        m.calculate_latency()
        processor.measurements.append(m)
    
    stats_a = processor.get_statistics()
    print(f"  Mean Latency: {stats_a['mean_ms']:.3f} ms")
    print()
    
    # Test Mode B: With ultrasonic
    print("Mode B: With Ultrasonic Layer")
    processor.measurements.clear()
    processor.enable_ultrasonic_layer(frequency=20000, amplitude=0.1)
    print(f"  Ultrasonic enabled: {processor.is_ultrasonic_enabled()}")
    
    # Simulate measurements with slightly different latency
    for i in range(10):
        m = LatencyMeasurement()
        m.input_timestamp = i * 1_000_000
        m.output_timestamp = (i * 1_000_000) + 48_000
        m.has_ultrasonic = True
        m.calculate_latency()
        processor.measurements.append(m)
    
    stats_b = processor.get_statistics()
    print(f"  Mean Latency: {stats_b['mean_ms']:.3f} ms")
    print(f"  Difference: {stats_b['mean_ms'] - stats_a['mean_ms']:.3f} ms")
    print()


def example_logging():
    """Example: Save and load measurements"""
    print("=" * 60)
    print("Example 6: Logging Results")
    print("=" * 60)
    
    config = LoggingConfig(log_dir="logs")
    logger = LatencyLogger(config)
    
    # Create sample measurements
    measurements = []
    for i in range(20):
        m = LatencyMeasurement()
        m.input_timestamp = i * 1_000_000
        m.output_timestamp = (i * 1_000_000) + 50_000
        m.has_ultrasonic = i >= 10  # First 10 without, last 10 with
        m.calculate_latency()
        measurements.append(m)
    
    # Save to CSV
    csv_file = logger.save_measurements_csv(measurements, "example_test")
    print(f"Saved to CSV: {csv_file}")
    
    # Calculate statistics
    latencies = [m.latency_ns / 1_000_000 for m in measurements]
    stats = {
        'count': len(latencies),
        'mean_ms': np.mean(latencies),
        'min_ms': np.min(latencies),
        'max_ms': np.max(latencies),
        'std_ms': np.std(latencies)
    }
    
    # Save to JSON
    config.log_format = "json"
    json_file = logger.save_measurements_json(measurements, "example_test", stats)
    print(f"Saved to JSON: {json_file}")
    
    # Load back
    loaded = logger.load_measurements_json(json_file)
    print(f"Loaded {len(loaded['measurements'])} measurements")
    print(f"Test name: {loaded['test_name']}")
    print(f"Mean latency: {loaded['statistics']['mean_ms']:.3f} ms")
    print()


def example_ab_testing_workflow():
    """Example: Complete A/B testing workflow"""
    print("=" * 60)
    print("Example 7: A/B Testing Workflow")
    print("=" * 60)
    
    # Configuration
    config = AppConfig()
    processor = AudioProcessor(config.audio)
    logger = LatencyLogger(config.logging)
    
    print("A/B Testing: Baseline vs Ultrasonic Layer")
    print()
    
    # Phase 1: Test Mode A (Baseline)
    print("Phase 1: Testing Mode A (Baseline)")
    processor.disable_ultrasonic_layer()
    
    # Simulate measurements
    for i in range(15):
        m = LatencyMeasurement()
        m.input_timestamp = i * 1_000_000
        m.output_timestamp = (i * 1_000_000) + 45_000 + np.random.randint(-2000, 2000)
        m.has_ultrasonic = False
        m.calculate_latency()
        processor.measurements.append(m)
    
    stats_a = processor.get_statistics()
    print(f"  Samples: {stats_a['count']}")
    print(f"  Mean: {stats_a['mean_ms']:.3f} ms")
    print(f"  Min: {stats_a['min_ms']:.3f} ms")
    print(f"  Max: {stats_a['max_ms']:.3f} ms")
    print(f"  Std: {stats_a['std_ms']:.3f} ms")
    
    # Save Mode A results
    filepath_a = logger.save_measurements(
        processor.get_measurements(),
        test_name="mode_a_baseline",
        statistics=stats_a
    )
    print(f"  Saved to: {filepath_a}")
    print()
    
    # Phase 2: Test Mode B (With Ultrasonic)
    print("Phase 2: Testing Mode B (With Ultrasonic)")
    processor.measurements.clear()
    processor.enable_ultrasonic_layer(
        frequency=config.ultrasonic.frequency,
        amplitude=config.ultrasonic.amplitude
    )
    
    # Simulate measurements with slightly increased latency
    for i in range(15):
        m = LatencyMeasurement()
        m.input_timestamp = i * 1_000_000
        m.output_timestamp = (i * 1_000_000) + 48_000 + np.random.randint(-2000, 2000)
        m.has_ultrasonic = True
        m.calculate_latency()
        processor.measurements.append(m)
    
    stats_b = processor.get_statistics()
    print(f"  Samples: {stats_b['count']}")
    print(f"  Mean: {stats_b['mean_ms']:.3f} ms")
    print(f"  Min: {stats_b['min_ms']:.3f} ms")
    print(f"  Max: {stats_b['max_ms']:.3f} ms")
    print(f"  Std: {stats_b['std_ms']:.3f} ms")
    
    # Save Mode B results
    filepath_b = logger.save_measurements(
        processor.get_measurements(),
        test_name="mode_b_ultrasonic",
        statistics=stats_b
    )
    print(f"  Saved to: {filepath_b}")
    print()
    
    # Comparison
    print("Comparison:")
    print(f"  Mean latency difference: {stats_b['mean_ms'] - stats_a['mean_ms']:.3f} ms")
    print(f"  Percentage increase: {((stats_b['mean_ms'] / stats_a['mean_ms']) - 1) * 100:.2f}%")
    print()


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "EchoLayerApp - Example Usage" + " " * 20 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    example_ultrasonic_generation()
    example_apply_ultrasonic()
    example_configuration()
    example_latency_measurement()
    example_audio_processor()
    example_logging()
    example_ab_testing_workflow()
    
    print("=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)
    print()
    print("To run the GUI application:")
    print("  streamlit run app.py")
    print()


if __name__ == "__main__":
    main()
