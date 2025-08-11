"""
LiveNeuron - Interactive 2D Brain Visualization Package

Interactive 2D brain visualization using Plotly and Dash.
Supports Eelbrain NDVar data format with built-in MNE sample data.
"""

__version__ = "1.0.0"
__author__ = "LiveNeuron Team"

from .viz_2d import EelbrainPlotly2DViz
from .sample_data import create_sample_brain_data

# Create alias for backward compatibility
BrainPlotly2DViz = EelbrainPlotly2DViz

__all__ = [
    "EelbrainPlotly2DViz",
    "BrainPlotly2DViz",  # Alias for compatibility
    "create_sample_brain_data",
]
