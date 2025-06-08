#!/usr/bin/env python3
"""
Standalone runner for the LeetCode AI Assistant
This version can be run from within the screengpt directory without import issues.
"""

import sys
import os

# Add the parent directory to the Python path so we can import screengpt as a package
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Now we can import the package
from screengpt import main

if __name__ == "__main__":
    main() 