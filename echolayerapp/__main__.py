#!/usr/bin/env python3
"""
Main entry point for EchoLayerApp.
Provides access to both CLI and GUI interfaces.
"""

import sys
import argparse


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='EchoLayerApp - Ultrasonic overlay latency benchmark tool',
        epilog='Use --gui for graphical interface or provide commands for CLI mode'
    )
    
    parser.add_argument('--gui', action='store_true',
                       help='Launch graphical user interface')
    parser.add_argument('--version', action='version',
                       version='EchoLayerApp 1.0.0')
    
    # Parse known args to allow CLI subcommands
    args, remaining = parser.parse_known_args()
    
    if args.gui:
        # Launch GUI
        try:
            from echolayerapp.interfaces.gui import main as gui_main
            gui_main()
        except ImportError as e:
            print(f"Error launching GUI: {e}", file=sys.stderr)
            print("Make sure tkinter is installed.", file=sys.stderr)
            sys.exit(1)
    else:
        # Launch CLI
        # Restore sys.argv for CLI parser
        sys.argv = [sys.argv[0]] + remaining
        from echolayerapp.interfaces.cli import main as cli_main
        cli_main()


if __name__ == '__main__':
    main()
