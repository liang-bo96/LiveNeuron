"""
Test utilities for mocking MNE dataset dependencies.
This allows tests to run without downloading large datasets.
"""

import numpy as np
from unittest.mock import MagicMock
import pytest


class MockNDVar:
    """Mock NDVar that mimics eelbrain's NDVar structure."""

    def __init__(self, data, coords, times):
        self.data = data
        self.coords = coords
        self.times = times
        self.has_case = True  # Simulate having a case dimension initially

        # Create mock source dimension
        self.source = MagicMock()
        self.source.coordinates = coords

        # Create mock time dimension
        self.time = MagicMock()
        self.time.times = times

    def mean(self, dimension):
        """Mock the mean method to simulate averaging over cases."""
        if dimension == "case":
            # Return a new MockNDVar without case dimension
            mock_result = MockNDVar(self.data, self.coords, self.times)
            mock_result.has_case = False
            return mock_result
        return self

    def get_data(self, dimensions):
        """Mock get_data method to return data in specified dimension order."""
        if dimensions == ("source", "space", "time"):
            return self.data
        return self.data


def create_mock_mne_dataset():
    """Create a mock MNE dataset that mimics the structure of get_mne_sample."""
    # Create realistic brain coordinates (distributed in 3D space)
    n_sources = 200
    n_times = 76
    np.random.seed(42)  # For reproducible tests

    # Generate coordinates in a brain-like distribution
    coords = np.random.randn(n_sources, 3) * 0.05  # Scale to brain size
    coords[:, 2] = np.abs(coords[:, 2])  # Keep Z positive (above brain stem)

    # Create time values matching the expected range
    time_values = np.linspace(-0.1, 0.4, n_times)

    # Create realistic brain activity data (sources x space x time)
    brain_data = np.random.randn(n_sources, 3, n_times) * 0.1

    # Add some realistic temporal patterns
    for i in range(n_sources):
        # Add some temporal correlation
        brain_data[i, :, :] = np.cumsum(brain_data[i, :, :], axis=1) * 0.1

    # Create mock NDVar
    mock_ndvar = MockNDVar(brain_data, coords, time_values)

    # Create the mock dataset structure that matches what get_mne_sample returns
    mock_dataset = {
        "src": mock_ndvar,  # This is what the code accesses as data_ds["src"]
    }

    return mock_dataset


def mock_get_mne_sample(*args, **kwargs):
    """Mock function to replace datasets.get_mne_sample."""
    return create_mock_mne_dataset()


def skip_if_ci():
    """Skip test if running in CI environment."""
    import os

    skip_conditions = [
        os.getenv("CI", "").lower() in ("true", "1", "yes"),
        os.getenv("GITHUB_ACTIONS", "").lower() in ("true", "1", "yes"),
        os.getenv("SKIP_MNE_DATASET", "").lower() in ("true", "1", "yes"),
    ]

    return pytest.mark.skipif(
        any(skip_conditions), reason="Skipping MNE dataset test in CI environment"
    )


def mock_mne_dataset():
    """Pytest fixture to mock MNE dataset loading."""

    def decorator(func):
        """Decorator that patches get_mne_sample with mock data."""
        import functools
        from unittest.mock import patch

        @functools.wraps(func)
        @patch("eelbrain.datasets.get_mne_sample", side_effect=mock_get_mne_sample)
        def wrapper(mock_get_sample, *args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator
