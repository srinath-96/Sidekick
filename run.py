#!/usr/bin/env python3
"""
Simple runner script for the LeetCode AI Assistant
"""

if __name__ == "__main__":
    try:
        # Try importing from the package (when run from parent directory)
        from screengpt import main
    except ModuleNotFoundError:
        # Fall back to relative import (when run from within screengpt directory)
        from main import main
    
    main() 