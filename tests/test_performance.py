"""
Performance and stress tests for eelbrain_plotly_viz package.
"""

import pytest
import time
import numpy as np
import os
from unittest.mock import patch
from eelbrain_plotly_viz import EelbrainPlotly2DViz
from eelbrain_plotly_viz.sample_data import create_sample_brain_data

# Handle different import paths for different environments
try:
    from .mock_utils import mock_get_mne_sample, skip_if_ci
except ImportError:
    try:
        from tests.mock_utils import mock_get_mne_sample, skip_if_ci
    except ImportError:
        from mock_utils import mock_get_mne_sample, skip_if_ci

# Check if we should use mock data (for CI or offline testing)
USE_MOCK_DATA = (
    os.getenv("CI", "").lower() in ("true", "1", "yes")
    or os.getenv("SKIP_MNE_DATASET", "").lower() in ("true", "1", "yes")
    or os.getenv("USE_MOCK_DATA", "").lower() in ("true", "1", "yes")
)


def test_large_dataset_performance():
    """Test performance with larger datasets."""
    # Create a larger dataset
    data_dict = create_sample_brain_data(
        n_sources=500, n_times=100, has_vector_data=True, random_seed=42
    )

    start_time = time.time()
    if USE_MOCK_DATA:
        with patch("eelbrain.datasets.get_mne_sample", side_effect=mock_get_mne_sample):
            viz = EelbrainPlotly2DViz()
    else:
        viz = EelbrainPlotly2DViz()

    # Override with larger data
    viz.glass_brain_data = data_dict["data"].transpose(
        0, 2, 1
    )  # (sources, space, time)
    viz.source_coords = data_dict["coords"]
    viz.time_values = data_dict["times"]
    viz.butterfly_data = np.linalg.norm(viz.glass_brain_data, axis=1)

    # Test plotting functions
    butterfly_fig = viz.create_butterfly_plot()
    brain_plots = viz.create_2d_brain_projections_plotly(time_idx=10)

    end_time = time.time()
    execution_time = end_time - start_time

    # Should complete within reasonable time (adjust threshold as needed)
    assert execution_time < 30, f"Performance test took too long: {execution_time:.2f}s"
    assert butterfly_fig is not None
    assert len(brain_plots) == 3


def test_memory_usage():
    """Test memory usage doesn't explode with moderate datasets."""
    # Check for required dependencies upfront
    psutil = pytest.importorskip("psutil", reason="psutil required for memory testing")
    import os

    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB

    # Create multiple visualizations
    for i in range(5):
        if USE_MOCK_DATA:
            with patch(
                "eelbrain.datasets.get_mne_sample", side_effect=mock_get_mne_sample
            ):
                viz = EelbrainPlotly2DViz()
        else:
            viz = EelbrainPlotly2DViz()

        _ = viz.create_butterfly_plot()
        _ = viz.create_2d_brain_projections_plotly(time_idx=i)

    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = final_memory - initial_memory

    # Memory shouldn't increase dramatically (adjust threshold as needed)
    assert memory_increase < 1500, f"Memory usage increased by {memory_increase:.1f}MB"
