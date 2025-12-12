"""
LiveNeuron - Interactive 2D Brain Visualization Package

Interactive 2D brain visualization using Plotly and Dash.
Supports Eelbrain NDVar data format with built-in MNE sample data.

The EelbrainPlotly2DViz class demonstrates the Single Responsibility Principle
by delegating to internal helper components:
- Data loading and normalization
- Figure construction
- Layout composition (Strategy pattern)
- Application control and interaction

Custom layouts can be created by inheriting from LayoutBuilder and registering
them via register_layout; see the documentation for a complete example.
"""

__version__ = "1.0.0"
__author__ = "LiveNeuron Team"

# Main visualization class
from ._viz_2d import EelbrainPlotly2DViz

# Sample data for testing (public function only, not internal classes)
from ._sample_data import create_sample_brain_data

# Layout extension API (for users who want to create custom layouts)
from ._layout_helper import (
    LayoutBuilder,
    register_layout,
    get_layout_builder,
)

__all__ = [
    # Main class
    "EelbrainPlotly2DViz",
    # Sample data
    "create_sample_brain_data",
    # Layout extension API (Open/Closed Principle)
    "LayoutBuilder",  # Abstract base class for custom layouts
    "register_layout",  # Function to register custom layouts
    "get_layout_builder",  # Function to retrieve layout builders
]
