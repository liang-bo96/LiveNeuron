"""
Test configuration and common fixtures.

This file is automatically loaded by pytest and ensures the src directory
is in the Python path for both development and CI environments.
"""

import sys
import os

# Add src directory to Python path for development/CI environments
# This allows imports like 'from eelbrain_plotly_viz import ...' to work
project_root = os.path.dirname(os.path.dirname(__file__))
src_path = os.path.join(project_root, "src")

if src_path not in sys.path:
    sys.path.insert(0, src_path)
