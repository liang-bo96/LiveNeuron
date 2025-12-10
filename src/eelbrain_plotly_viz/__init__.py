"""
LiveNeuron - Interactive 2D Brain Visualization Package

Interactive 2D brain visualization using Plotly and Dash.
Supports Eelbrain NDVar data format with built-in MNE sample data.

The EelbrainPlotly2DViz class demonstrates the Single Responsibility Principle
through mixin composition:
- DataLoaderMixin: Handles data ingestion and normalization
- PlotFactoryMixin: Constructs all visualization figures
- LayoutBuilderMixin: Arranges UI components (uses Strategy pattern)
- AppControllerMixin: Controls user interaction and application behavior

Custom layouts can be created by inheriting from LayoutBuilder and registering
them via register_layout; see the documentation for a complete example.
"""

__version__ = "1.0.0"
__author__ = "LiveNeuron Team"

from .viz_2d import EelbrainPlotly2DViz
from .sample_data import create_sample_brain_data

# Export mixins for extensibility
from .data_loader_mixin import DataLoaderMixin
from .plot_factory_mixin import PlotFactoryMixin
from .layout_builder_mixin import (
    LayoutBuilderMixin,
    # Layout strategy classes and registry
    LayoutBuilder,
    VerticalLayout,
    HorizontalLayout,
    LAYOUTS,
    register_layout,
    get_layout_builder,
)
from .app_controller_mixin import AppControllerMixin

# Create alias for backward compatibility
BrainPlotly2DViz = EelbrainPlotly2DViz

__all__ = [
    # Main class
    "EelbrainPlotly2DViz",
    "BrainPlotly2DViz",  # Alias for compatibility
    # Sample data
    "create_sample_brain_data",
    # Mixins for extensibility
    "DataLoaderMixin",
    "PlotFactoryMixin",
    "LayoutBuilderMixin",
    "AppControllerMixin",
    # Layout strategy pattern (Open/Closed Principle)
    "LayoutBuilder",  # Abstract base class for custom layouts
    "VerticalLayout",  # Built-in vertical layout
    "HorizontalLayout",  # Built-in horizontal layout
    "LAYOUTS",  # Layout registry dictionary
    "register_layout",  # Function to register custom layouts
    "get_layout_builder",  # Function to retrieve layout builders
]
