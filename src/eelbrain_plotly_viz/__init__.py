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

from .viz_2d import EelbrainPlotly2DViz
from .sample_data import create_sample_brain_data
from .layout_builder_helper import (
    # Layout strategy classes and registry
    LayoutBuilder,
    VerticalLayout,
    HorizontalLayout,
    LAYOUTS,
    register_layout,
    get_layout_builder,
)

# Create alias for backward compatibility
BrainPlotly2DViz = EelbrainPlotly2DViz

__all__ = [
    # Main class
    "EelbrainPlotly2DViz",
    "BrainPlotly2DViz",  # Alias for compatibility
    # Sample data
    "create_sample_brain_data",
    # Layout strategy pattern (Open/Closed Principle)
    "LayoutBuilder",  # Abstract base class for custom layouts
    "VerticalLayout",  # Built-in vertical layout
    "HorizontalLayout",  # Built-in horizontal layout
    "LAYOUTS",  # Layout registry dictionary
    "register_layout",  # Function to register custom layouts
    "get_layout_builder",  # Function to retrieve layout builders
]
