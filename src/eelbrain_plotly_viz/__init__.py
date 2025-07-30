"""
Eelbrain Plotly Visualization Package

Interactive 2D brain visualization using Plotly and Dash.
Supports both Eelbrain NDVar data format and standalone numpy arrays.
"""

__version__ = "1.0.0"
__author__ = "Eelbrain Team"

from .viz_2d import BrainPlotly2DViz
from .sample_data import create_sample_brain_data

__all__ = [
    "BrainPlotly2DViz",
    "create_sample_brain_data",
] 