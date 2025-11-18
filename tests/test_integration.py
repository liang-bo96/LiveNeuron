"""
Integration tests for eelbrain_plotly_viz package.
"""

import pytest
import tempfile
from eelbrain_plotly_viz import EelbrainPlotly2DViz


def test_export_functionality():
    """Test image export functionality."""
    # Check for required dependencies upfront
    pytest.importorskip("kaleido", reason="kaleido required for image export testing")

    viz = EelbrainPlotly2DViz()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Test export functionality
        result = viz.export_images(output_dir=temp_dir, time_idx=5, format="png")

        # Check that export function runs without error
        assert isinstance(result, dict)
        assert "status" in result


def test_jupyter_mode():
    """Test Jupyter mode functionality."""
    viz = EelbrainPlotly2DViz()

    # Test setting Jupyter mode
    viz.is_jupyter_mode = True
    viz._setup_layout()  # Rebuild layout with Jupyter styles

    # Should still have a valid layout
    assert hasattr(viz.app, "layout")
    assert viz.is_jupyter_mode is True


def test_multiple_visualizations():
    """Test creating multiple visualizations doesn't interfere."""
    viz1 = EelbrainPlotly2DViz(cmap="Hot", show_max_only=False)
    viz2 = EelbrainPlotly2DViz(cmap="Viridis", show_max_only=True)

    # Each should maintain its own settings
    assert viz1.cmap == "Hot"
    assert viz2.cmap == "Viridis"
    assert viz1.show_max_only is False
    assert viz2.show_max_only is True

    # Both should create independent plots
    fig1 = viz1._create_butterfly_plot()
    fig2 = viz2._create_butterfly_plot()

    assert fig1 is not fig2
    assert hasattr(fig1, "data")
    assert hasattr(fig2, "data")


def test_error_handling():
    """Test error handling in various scenarios."""
    viz = EelbrainPlotly2DViz()

    # Test with invalid time index
    brain_plots = viz._create_2d_brain_projections_plotly(time_idx=999999)

    # Should still return a valid dictionary (with error handling)
    assert isinstance(brain_plots, dict)
    assert len(brain_plots) == 3

    # Test with None data (edge case)
    viz_empty = EelbrainPlotly2DViz()
    viz_empty.glass_brain_data = None
    viz_empty.source_coords = None
    viz_empty.time_values = None

    # Should handle gracefully
    brain_plots_empty = viz_empty._create_2d_brain_projections_plotly()
    assert isinstance(brain_plots_empty, dict)


def test_callback_functionality():
    """Test that Dash callbacks are properly set up."""
    viz = EelbrainPlotly2DViz()

    # Check that the app has callbacks registered
    assert hasattr(viz.app, "callback_map")
    assert len(viz.app.callback_map) > 0  # Should have some callbacks

    # Test that layout components exist
    assert viz.app.layout is not None


def test_data_consistency():
    """Test data consistency across different methods."""
    viz = EelbrainPlotly2DViz()

    # All data arrays should have consistent shapes
    n_sources, n_space, n_times = viz.glass_brain_data.shape

    assert viz.source_coords.shape[0] == n_sources
    assert viz.butterfly_data.shape[0] == n_sources
    assert viz.butterfly_data.shape[1] == n_times
    assert len(viz.time_values) == n_times

    # Test that projections use consistent data
    brain_plots = viz._create_2d_brain_projections_plotly(time_idx=5)

    for view_name, fig in brain_plots.items():
        assert hasattr(fig, "data")
        # Should have at least a heatmap trace
        assert len(fig.data) > 0
