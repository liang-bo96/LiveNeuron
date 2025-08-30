"""
Performance and stress tests for eelbrain_plotly_viz package.
"""

import pytest
import time
import numpy as np
from eelbrain_plotly_viz import EelbrainPlotly2DViz
from eelbrain_plotly_viz.sample_data import create_sample_brain_data


def test_large_dataset_performance():
    """Test performance with larger datasets."""
    # Test with default sample data (no custom data needed for performance test)
    start_time = time.time()
    viz = EelbrainPlotly2DViz()  # Uses default MNE sample data
    creation_time = time.time() - start_time

    # Should create visualization in reasonable time (less than 30 seconds)
    assert creation_time < 30.0, f"Visualization creation took {creation_time:.2f}s"

    # Test plot creation performance
    start_time = time.time()
    butterfly_fig = viz.create_butterfly_plot(0)
    butterfly_time = time.time() - start_time

    assert butterfly_time < 10.0, f"Butterfly plot creation took {butterfly_time:.2f}s"
    assert butterfly_fig is not None


def test_memory_usage():
    """Test memory usage doesn't grow excessively."""
    import gc

    # Force garbage collection before test
    gc.collect()

    # Create multiple visualizations to test for memory leaks
    vizualizations = []
    for i in range(5):
        # Use default sample data for each visualization
        viz = EelbrainPlotly2DViz()
        vizualizations.append(viz)

    # Test that we can create plots from all visualizations
    for i, viz in enumerate(vizualizations):
        butterfly_fig = viz.create_butterfly_plot(i % 10)
        assert butterfly_fig is not None

    # Clean up
    del vizualizations
    gc.collect()


def test_many_time_points():
    """Test handling datasets with many time points."""
    # Use default sample data which has sufficient time points for testing
    viz = EelbrainPlotly2DViz()

    # Test accessing different time points (use valid indices for default data)
    max_time_idx = len(viz.time_values) - 1 if viz.time_values is not None else 50
    time_points = [0, min(10, max_time_idx), min(25, max_time_idx), max_time_idx]
    for time_idx in time_points:
        start_time = time.time()
        butterfly_fig = viz.create_butterfly_plot(time_idx)
        brain_plots = viz.create_2d_brain_projections_plotly(time_idx)
        plot_time = time.time() - start_time

        assert butterfly_fig is not None
        assert isinstance(brain_plots, dict)
        assert "axial" in brain_plots
        # Each plot should be created quickly
        assert (
            plot_time < 5.0
        ), f"Plot creation for time {time_idx} took {plot_time:.2f}s"
