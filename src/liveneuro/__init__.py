"""
LiveNeuro - Interactive 2D Brain Visualization Package

Public API for the LiveNeuro 2D brain visualization package.

Typical usage:

    from liveneuro import LiveNeuro
    viz = LiveNeuro(...)
"""

from ._liveneuro import LiveNeuro
from ._sample_data import create_sample_brain_data
from ._layout_helper import LayoutBuilder, register_layout, get_layout_builder

__version__ = "1.0.0"
__author__ = "LiveNeuro Team"


__all__ = [
    "LiveNeuro",
    "create_sample_brain_data",
    "LayoutBuilder",
    "register_layout",
    "get_layout_builder",
]
