#!/usr/bin/env python3
'''
run.py: Entry point for the Snoopy Simulation
'''

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

# Import the main simulation
from src.main import main

if __name__ == "__main__":
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Run the simulation
    main()