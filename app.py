"""Main entry point for EchoLayerApp"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from echolayer.gui.streamlit_app import main

if __name__ == "__main__":
    main()
