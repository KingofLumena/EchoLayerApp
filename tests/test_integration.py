"""Integration tests for EchoLayerApp"""
import time
import numpy as np
from echolayer.config import AppConfig, AudioConfig, UltrasonicLayerConfig
from echolayer.audio.processor import AudioProcessor, LatencyMeasurement
from echolayer.layers.ultrasonic import UltrasonicLayer
from echolayer.logging.logger import LatencyLogger


def test_ultrasonic_layer():
    """Test ultrasonic layer generation"""
    print("Testing UltrasonicLayer...")
    
    layer = UltrasonicLayer(sample_rate=48000, frequency=20000, amplitude=0.1)
    signal = layer.generate(num_samples=1024, channels=2)
    
    assert signal.shape == (1024, 2), f"Expected shape (1024, 2), got {signal.shape}"
    assert signal.dtype == np.float32, f"Expected dtype float32, got {signal.dtype}"
    assert -0.11 <= signal.min() <= -0.09, f"Min value out of range: {signal.min()}"
    assert 0.09 <= signal.max() <= 0.11, f"Max value out of range: {signal.max()}"
    
    # Test apply to signal
    audio = np.random.randn(1024, 2).astype(np.float32) * 0.01
    result = layer.apply_to_signal(audio)
    assert result.shape == audio.shape, "Output shape mismatch"
    
    print("✓ UltrasonicLayer tests passed")


def test_configuration():
    """Test configuration management"""
    print("\nTesting Configuration...")
    
    config = AppConfig()
    assert config.audio.sample_rate == 48000
    assert config.audio.channels == 2
    assert config.ultrasonic.frequency == 20000
    assert config.logging.log_dir == "logs"
    
    # Test custom config
    custom = AppConfig(
        audio=AudioConfig(sample_rate=44100, channels=1)
    )
    assert custom.audio.sample_rate == 44100
    assert custom.audio.channels == 1
    
    print("✓ Configuration tests passed")


def test_latency_measurement():
    """Test latency measurement structure"""
    print("\nTesting LatencyMeasurement...")
    
    m = LatencyMeasurement()
    m.input_timestamp = 1000000000
    m.output_timestamp = 1000050000
    m.has_ultrasonic = True
    latency = m.calculate_latency()
    
    assert latency == 50000, f"Expected latency 50000, got {latency}"
    assert m.latency_ns == 50000
    
    data = m.to_dict()
    assert data['latency_ns'] == 50000
    assert data['latency_ms'] == 0.05
    assert data['has_ultrasonic'] == True
    
    print("✓ LatencyMeasurement tests passed")


def test_audio_processor_basic():
    """Test basic AudioProcessor functionality without stream"""
    print("\nTesting AudioProcessor (basic)...")
    
    config = AudioConfig()
    processor = AudioProcessor(config)
    
    # Test ultrasonic enable/disable
    assert not processor.is_ultrasonic_enabled()
    
    processor.enable_ultrasonic_layer(frequency=20000, amplitude=0.1)
    assert processor.is_ultrasonic_enabled()
    
    processor.disable_ultrasonic_layer()
    assert not processor.is_ultrasonic_enabled()
    
    # Test statistics with no measurements
    stats = processor.get_statistics()
    assert stats['count'] == 0
    
    print("✓ AudioProcessor basic tests passed")


def test_logger():
    """Test logger functionality"""
    print("\nTesting LatencyLogger...")
    
    from echolayer.config import LoggingConfig
    
    config = LoggingConfig(log_dir="logs")
    logger = LatencyLogger(config)
    
    # Create test measurements
    measurements = []
    for i in range(10):
        m = LatencyMeasurement()
        m.input_timestamp = i * 1_000_000
        m.output_timestamp = (i * 1_000_000) + 50_000
        m.has_ultrasonic = i % 2 == 0
        m.calculate_latency()
        measurements.append(m)
    
    # Test CSV save
    csv_file = logger.save_measurements_csv(measurements, "integration_test")
    assert csv_file.endswith('.csv')
    
    # Test JSON save
    config.log_format = "json"
    stats = {'mean_ms': 0.05, 'count': 10}
    json_file = logger.save_measurements_json(measurements, "integration_test", stats)
    assert json_file.endswith('.json')
    
    # Test loading
    loaded_csv = logger.load_measurements_csv(csv_file)
    assert len(loaded_csv) == 10
    
    loaded_json = logger.load_measurements_json(json_file)
    assert len(loaded_json['measurements']) == 10
    assert loaded_json['statistics']['mean_ms'] == 0.05
    
    print("✓ LatencyLogger tests passed")


def test_integration_workflow():
    """Test integrated workflow"""
    print("\nTesting integrated workflow...")
    
    # 1. Create configuration
    config = AppConfig(
        audio=AudioConfig(sample_rate=48000, channels=2),
        ultrasonic=UltrasonicLayerConfig(frequency=20000, amplitude=0.1)
    )
    
    # 2. Create processor and logger
    processor = AudioProcessor(config.audio)
    logger = LatencyLogger(config.logging)
    
    # 3. Test A/B workflow simulation (without actual audio stream)
    # Mode A: Baseline
    processor.disable_ultrasonic_layer()
    assert not processor.is_ultrasonic_enabled()
    
    # Mode B: With ultrasonic
    processor.enable_ultrasonic_layer(
        frequency=config.ultrasonic.frequency,
        amplitude=config.ultrasonic.amplitude
    )
    assert processor.is_ultrasonic_enabled()
    
    # 4. Simulate measurements
    for i in range(5):
        m = LatencyMeasurement()
        m.input_timestamp = i * 1_000_000
        m.output_timestamp = (i * 1_000_000) + 50_000 + i * 100
        m.has_ultrasonic = processor.is_ultrasonic_enabled()
        m.calculate_latency()
        processor.measurements.append(m)
    
    # 5. Get statistics
    stats = processor.get_statistics()
    assert stats['count'] == 5
    assert stats['mean_ms'] > 0
    
    # 6. Save results
    filepath = logger.save_measurements(
        processor.get_measurements(),
        test_name="integration_test_workflow",
        statistics=stats
    )
    assert filepath is not None
    
    print("✓ Integration workflow tests passed")


def run_all_tests():
    """Run all integration tests"""
    print("=" * 60)
    print("EchoLayerApp Integration Tests")
    print("=" * 60)
    
    try:
        test_ultrasonic_layer()
        test_configuration()
        test_latency_measurement()
        test_audio_processor_basic()
        test_logger()
        test_integration_workflow()
        
        print("\n" + "=" * 60)
        print("✓ All integration tests passed!")
        print("=" * 60)
        return True
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
