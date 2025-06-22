#!/usr/bin/env python3
"""
Launcher script for the AI Book Publication Workflow Web Server
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.web_server import main

if __name__ == '__main__':
    main() 