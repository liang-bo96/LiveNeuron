"""
Integration tests for eelbrain_plotly_viz package.
"""

import pytest
import tempfile
from eelbrain_plotly_viz import EelbrainPlotly2DViz


def test_export_functionality():
    """Test image export functionality."""
    viz = EelbrainPlotly2DViz()

    with tempfile.TemporaryDirectory() as temp_dir:
        # Test export (this will check if the method exists and can be called)
        result = viz.export_images(output_dir=temp_dir, time_idx=0)

        # Verify the result structure
        assert isinstance(result, dict)
        assert "status" in result
        # Don't require success since this depends on kaleido being available


def test_jupyter_mode():
    """Test Jupyter mode configuration."""
    viz = EelbrainPlotly2DViz()

    # Test that Jupyter mode can be enabled
    viz.is_jupyter_mode = True
    assert viz.is_jupyter_mode is True

    # Test that layout can be rebuilt for Jupyter
    try:
        viz._setup_layout()
        # If no exception, the layout setup worked
        assert True
    except Exception as e:
        pytest.fail(f"Jupyter layout setup failed: {e}")


def test_multiple_visualizations():
    """Test creating multiple visualization instances."""
    viz1 = EelbrainPlotly2DViz(cmap="Hot")
    viz2 = EelbrainPlotly2DViz(cmap="Viridis")

    # Verify they are independent instances
    assert viz1 is not viz2
    assert viz1.cmap != viz2.cmap
    assert viz1.app is not viz2.app


def test_error_handling():
    """Test error handling in various scenarios."""
    viz = EelbrainPlotly2DViz()

    # Test brain projections with invalid time index
    try:
        brain_plots = viz.create_2d_brain_projections_plotly(time_idx=99999)
        # Should handle gracefully and return valid figures
        assert isinstance(brain_plots, dict)
        assert "axial" in brain_plots
    except Exception as e:
        pytest.fail(f"Brain projection error handling failed: {e}")

    # Test butterfly plot with invalid time index
    try:
        butterfly_fig = viz.create_butterfly_plot(selected_time_idx=99999)
        # Should handle gracefully
        assert butterfly_fig is not None
    except Exception as e:
        pytest.fail(f"Butterfly plot error handling failed: {e}")


def test_callback_functionality():
    """Test that callbacks are properly set up."""
    viz = EelbrainPlotly2DViz()

    # Check that the app has callbacks
    assert viz.app is not None
    assert hasattr(viz.app, "callback_map")

    # The callback_map should have entries if callbacks are registered
    # This is a basic check that setup_callbacks worked
    callback_count = len(viz.app.callback_map) if viz.app.callback_map else 0
    assert callback_count > 0, "No callbacks were registered"


def test_data_consistency():
    """Test data consistency across different components."""
    viz = EelbrainPlotly2DViz()

    # Verify data attributes are consistent
    if viz.time_values is not None and viz.butterfly_data is not None:
        # Time dimension should match
        assert len(viz.time_values) == viz.butterfly_data.shape[1]

    if viz.source_coords is not None and viz.butterfly_data is not None:
        # Source dimension should match
        assert len(viz.source_coords) == viz.butterfly_data.shape[0]

    # Test that creating figures doesn't modify the underlying data
    if viz.butterfly_data is not None:
        original_data = viz.butterfly_data.copy()
        _ = viz.create_butterfly_plot(0)
        assert (viz.butterfly_data == original_data).all()
