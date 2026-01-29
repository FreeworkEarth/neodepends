#!/usr/bin/env python3
"""
Convenience script to run the Survey System from the project root.
This script ensures the src directory is in the Python path.
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run main
from main import main

if __name__ == "__main__":
    main()

