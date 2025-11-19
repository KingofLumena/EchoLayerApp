"""Streamlit GUI for EchoLayerApp"""
import streamlit as st
import pandas as pd
import time
from typing import Optional
from ..config import AppConfig, AudioConfig, UltrasonicLayerConfig, LoggingConfig
from ..audio.processor import AudioProcessor
from ..logging.logger import LatencyLogger


class EchoLayerGUI:
    """Streamlit GUI for audio latency benchmarking"""
    
    def __init__(self):
        """Initialize GUI"""
        self.initialize_session_state()
        
    def initialize_session_state(self):
        """Initialize Streamlit session state"""
        if 'config' not in st.session_state:
            st.session_state.config = AppConfig()
        
        if 'processor' not in st.session_state:
            st.session_state.processor = AudioProcessor(st.session_state.config.audio)
        
        if 'logger' not in st.session_state:
            st.session_state.logger = LatencyLogger(st.session_state.config.logging)
        
        if 'is_testing' not in st.session_state:
            st.session_state.is_testing = False
        
        if 'measurements_display' not in st.session_state:
            st.session_state.measurements_display = []
    
    def render_header(self):
        """Render page header"""
        st.title("🔊 EchoLayerApp")
        st.markdown("### Audio Latency Benchmarking with Ultrasonic Layers")
        st.markdown("---")
    
    def render_ab_testing_controls(self):
        """Render A/B testing toggle controls"""
        st.subheader("A/B Testing Controls")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Mode A: Baseline")
            st.info("Clean audio pass-through without ultrasonic layer")
            
            if st.button("🔵 Test Mode A (No Ultrasonic)", 
                        key="test_a",
                        disabled=st.session_state.is_testing,
                        use_container_width=True):
                st.session_state.processor.disable_ultrasonic_layer()
                st.success("✓ Mode A selected: Ultrasonic layer disabled")
        
        with col2:
            st.markdown("#### Mode B: With Ultrasonic Layer")
            st.info("Audio with ultrasonic frequency overlay")
            
            if st.button("🟢 Test Mode B (With Ultrasonic)",
                        key="test_b",
                        disabled=st.session_state.is_testing,
                        use_container_width=True):
                config = st.session_state.config.ultrasonic
                st.session_state.processor.enable_ultrasonic_layer(
                    frequency=config.frequency,
                    amplitude=config.amplitude
                )
                st.success("✓ Mode B selected: Ultrasonic layer enabled")
        
        # Display current mode
        current_mode = "B (Ultrasonic ON)" if st.session_state.processor.is_ultrasonic_enabled() else "A (Baseline)"
        st.metric("Current Test Mode", current_mode)
    
    def render_audio_config(self):
        """Render audio configuration"""
        with st.expander("⚙️ Audio Configuration", expanded=False):
            config = st.session_state.config.audio
            
            config.sample_rate = st.selectbox(
                "Sample Rate (Hz)",
                options=[44100, 48000, 96000],
                index=1,
                key="sample_rate"
            )
            
            config.channels = st.slider(
                "Channels",
                min_value=1,
                max_value=2,
                value=2,
                key="channels"
            )
            
            config.chunk_size = st.slider(
                "Chunk Size (samples)",
                min_value=256,
                max_value=2048,
                value=1024,
                step=256,
                key="chunk_size"
            )
            
            # List available devices
            try:
                devices = st.session_state.processor.list_audio_devices()
                device_names = [f"{i}: {d['name']}" for i, d in enumerate(devices)]
                selected = st.selectbox(
                    "Audio Device",
                    options=["Default"] + device_names,
                    key="audio_device"
                )
                if selected != "Default":
                    config.device_index = int(selected.split(":")[0])
                else:
                    config.device_index = None
            except Exception as e:
                st.warning(f"Could not list audio devices: {e}")
    
    def render_ultrasonic_config(self):
        """Render ultrasonic layer configuration"""
        with st.expander("🌊 Ultrasonic Layer Settings", expanded=False):
            config = st.session_state.config.ultrasonic
            
            config.frequency = st.slider(
                "Ultrasonic Frequency (Hz)",
                min_value=18000,
                max_value=22000,
                value=20000,
                step=500,
                help="Frequency above human hearing range",
                key="ultrasonic_freq"
            )
            
            config.amplitude = st.slider(
                "Amplitude",
                min_value=0.01,
                max_value=0.5,
                value=0.1,
                step=0.01,
                help="Signal strength of ultrasonic layer",
                key="ultrasonic_amp"
            )
    
    def render_test_controls(self):
        """Render test start/stop controls"""
        st.subheader("Latency Test Control")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("▶️ Start Test", 
                        disabled=st.session_state.is_testing,
                        use_container_width=True,
                        type="primary"):
                self.start_test()
        
        with col2:
            if st.button("⏹️ Stop Test", 
                        disabled=not st.session_state.is_testing,
                        use_container_width=True):
                self.stop_test()
        
        with col3:
            if st.button("💾 Save Results",
                        disabled=st.session_state.is_testing or not st.session_state.processor.measurements,
                        use_container_width=True):
                self.save_results()
    
    def start_test(self):
        """Start latency test"""
        try:
            # Recreate processor with current config
            st.session_state.processor = AudioProcessor(st.session_state.config.audio)
            
            # Apply ultrasonic settings if needed
            if st.session_state.config.ultrasonic.enabled:
                config = st.session_state.config.ultrasonic
                st.session_state.processor.enable_ultrasonic_layer(
                    frequency=config.frequency,
                    amplitude=config.amplitude
                )
            
            st.session_state.processor.start_stream()
            st.session_state.is_testing = True
            st.success("✓ Test started! Audio stream is running...")
            st.rerun()
        except Exception as e:
            st.error(f"Error starting test: {e}")
    
    def stop_test(self):
        """Stop latency test"""
        try:
            st.session_state.processor.stop_stream()
            st.session_state.is_testing = False
            st.success("✓ Test stopped")
            st.rerun()
        except Exception as e:
            st.error(f"Error stopping test: {e}")
    
    def save_results(self):
        """Save test results to file"""
        try:
            measurements = st.session_state.processor.get_measurements()
            statistics = st.session_state.processor.get_statistics()
            
            mode = "with_ultrasonic" if st.session_state.processor.is_ultrasonic_enabled() else "baseline"
            test_name = f"latency_test_{mode}"
            
            filepath = st.session_state.logger.save_measurements(
                measurements,
                test_name=test_name,
                statistics=statistics
            )
            
            st.success(f"✓ Results saved to: {filepath}")
        except Exception as e:
            st.error(f"Error saving results: {e}")
    
    def render_live_statistics(self):
        """Render live statistics display"""
        st.subheader("📊 Live Statistics")
        
        if st.session_state.is_testing:
            stats = st.session_state.processor.get_statistics()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Sample Count", stats['count'])
            
            with col2:
                st.metric("Mean Latency", f"{stats['mean_ms']:.3f} ms")
            
            with col3:
                st.metric("Min Latency", f"{stats['min_ms']:.3f} ms")
            
            with col4:
                st.metric("Max Latency", f"{stats['max_ms']:.3f} ms")
            
            # Display recent measurements
            if stats['count'] > 0:
                measurements = st.session_state.processor.get_measurements()
                recent = measurements[-100:]  # Last 100 measurements
                
                df = pd.DataFrame([
                    {
                        'Sample': i,
                        'Latency (ms)': m.latency_ms,
                        'Ultrasonic': 'Yes' if m.has_ultrasonic else 'No'
                    }
                    for i, m in enumerate(recent)
                ])
                
                st.line_chart(df.set_index('Sample')['Latency (ms)'])
        else:
            st.info("Start a test to see live statistics")
    
    def render_results_summary(self):
        """Render results summary"""
        if not st.session_state.is_testing and st.session_state.processor.measurements:
            st.subheader("📈 Test Results Summary")
            
            stats = st.session_state.processor.get_statistics()
            measurements = st.session_state.processor.get_measurements()
            
            # Summary metrics
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Total Samples", stats['count'])
            
            with col2:
                st.metric("Mean Latency", f"{stats['mean_ms']:.3f} ms")
            
            with col3:
                st.metric("Std Deviation", f"{stats['std_ms']:.3f} ms")
            
            with col4:
                st.metric("Min Latency", f"{stats['min_ms']:.3f} ms")
            
            with col5:
                st.metric("Max Latency", f"{stats['max_ms']:.3f} ms")
            
            # Full data table
            with st.expander("View All Measurements"):
                df = pd.DataFrame([
                    {
                        'Sample': i,
                        'Latency (ms)': m.latency_ms,
                        'Latency (ns)': m.latency_ns,
                        'Ultrasonic': 'Yes' if m.has_ultrasonic else 'No'
                    }
                    for i, m in enumerate(measurements)
                ])
                st.dataframe(df, use_container_width=True)
    
    def run(self):
        """Run the GUI application"""
        st.set_page_config(
            page_title="EchoLayerApp",
            page_icon="🔊",
            layout="wide"
        )
        
        self.render_header()
        self.render_ab_testing_controls()
        
        st.markdown("---")
        
        self.render_audio_config()
        self.render_ultrasonic_config()
        
        st.markdown("---")
        
        self.render_test_controls()
        
        st.markdown("---")
        
        self.render_live_statistics()
        
        st.markdown("---")
        
        self.render_results_summary()
        
        # Auto-refresh when testing
        if st.session_state.is_testing:
            time.sleep(0.5)
            st.rerun()


def main():
    """Main entry point for Streamlit app"""
    gui = EchoLayerGUI()
    gui.run()


if __name__ == "__main__":
    main()
