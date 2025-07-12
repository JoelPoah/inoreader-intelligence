#!/usr/bin/env python3
"""
CLI wrapper for Inoreader Intelligence
"""

import sys
import os
from pathlib import Path

# Add src to path  
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Set up environment
os.environ['PATH'] = f"/home/joel/.local/bin:{os.environ.get('PATH', '')}"
os.environ['PYTHONPATH'] = f"{Path(__file__).parent}/src"

from inoreader_intelligence.cli import main

if __name__ == "__main__":
    main()