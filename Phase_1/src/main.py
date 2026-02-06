#!/usr/bin/env python3
"""
Todo Application - Main Entry Point

This is the main entry point for the command-line todo application.
The application allows users to manage tasks through a console interface.
"""
import sys
from cli.cli_interface import CLIInterface


def main():
    """Main entry point for the todo application."""
    try:
        cli = CLIInterface()
        cli.run()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()