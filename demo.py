#!/usr/bin/env python3
"""
Demo script for EchoLayerApp.
Demonstrates core functionality without requiring audio hardware.
"""

import sys
from echolayerapp.core.audio_engine import AudioEngine
from echolayerapp.core.ab_test import ABTest
from echolayerapp.utils.logger import LatencyLogger
from echolayerapp.utils.config import Config

def main():
    print("=" * 60)
    print("EchoLayerApp Demo")
    print("=" * 60)
    
    # Initialize components
    print("\n1. Initializing components...")
    config = Config()
    engine = AudioEngine(duration=0.1)  # Short duration for demo
    logger = LatencyLogger()
    print("   ✓ AudioEngine initialized")
    print("   ✓ Logger initialized")
    print("   ✓ Config loaded")
    
    # Generate audio samples
    print("\n2. Generating audio samples...")
    tone_1khz = engine.generate_tone(1000, 0.5)
    print(f"   ✓ Generated 1 kHz tone: {len(tone_1khz)} samples")
    
    overlay = engine.generate_ultrasonic_overlay(1000, 20000, 0.3)
    print(f"   ✓ Generated 1 kHz + 20 kHz overlay: {len(overlay)} samples")
    
    # Demonstrate A/B test configuration
    print("\n3. Setting up A/B test...")
    ab_test = ABTest(engine)
    config_a = {'base_freq': 1000, 'overlay_freq': 0}
    config_b = {'base_freq': 1000, 'overlay_freq': 20000}
    print(f"   Config A: Base={config_a['base_freq']} Hz, Overlay={config_a['overlay_freq']} Hz")
    print(f"   Config B: Base={config_b['base_freq']} Hz, Overlay={config_b['overlay_freq']} Hz")
    
    # Generate test audio
    audio_a = ab_test._generate_audio_from_config(config_a)
    audio_b = ab_test._generate_audio_from_config(config_b)
    print(f"   ✓ Test audio generated")
    
    # Demonstrate statistics calculation
    print("\n4. Demonstrating statistics...")
    mock_measurements = [
        {'total_latency_ns': 1000000, 'timestamp_ns': 0},
        {'total_latency_ns': 1200000, 'timestamp_ns': 1},
        {'total_latency_ns': 900000, 'timestamp_ns': 2},
        {'total_latency_ns': 1100000, 'timestamp_ns': 3},
        {'total_latency_ns': 950000, 'timestamp_ns': 4},
    ]
    
    stats = ab_test._calculate_stats(mock_measurements)
    print(f"   Measurements: {stats['count']}")
    print(f"   Mean latency: {stats['mean_latency_ms']:.2f} ms")
    print(f"   Min latency: {stats['min_latency_ns'] / 1_000_000:.2f} ms")
    print(f"   Max latency: {stats['max_latency_ns'] / 1_000_000:.2f} ms")
    print(f"   Std deviation: {stats['std_latency_ns'] / 1_000_000:.2f} ms")
    
    # Demonstrate logging
    print("\n5. Logging results...")
    log_file = logger.log_measurements(mock_measurements, "demo_measurements.json")
    print(f"   ✓ Results logged to: {log_file}")
    
    # Show configuration
    print("\n6. Configuration settings...")
    print(f"   Sample rate: {config.get('audio.sample_rate')} Hz")
    print(f"   Duration: {config.get('audio.duration')} s")
    print(f"   Log directory: {config.get('logging.log_dir')}")
    
    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("  • Run 'python run.py info' to see audio devices")
    print("  • Run 'python run.py test' to perform latency tests")
    print("  • Run 'python run.py ab-test' to compare configurations")
    print("  • Run 'python run.py --gui' to launch the GUI")
    print("\nNote: Audio playback requires working audio hardware.")
    print("=" * 60)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)
