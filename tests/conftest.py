"""
Pytest configuration and fixtures for eelbrain_plotly_viz tests.
"""

import pytest
from unittest.mock import patch

# Handle different import paths for different environments
try:
    from .mock_utils import mock_get_mne_sample
except ImportError:
    try:
        from tests.mock_utils import mock_get_mne_sample
    except ImportError:
        from mock_utils import mock_get_mne_sample


@pytest.fixture
def mock_mne_dataset():
    """Fixture that patches MNE dataset loading with mock data."""
    with patch(
        "eelbrain.datasets.get_mne_sample", side_effect=mock_get_mne_sample
    ) as mock:
        yield mock


@pytest.fixture
def viz_with_mock_data(mock_mne_dataset):
    """Fixture that provides a EelbrainPlotly2DViz instance with mocked data."""
    from src.eelbrain_plotly_viz import EelbrainPlotly2DViz

    return EelbrainPlotly2DViz()


# Configure pytest markers
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "network: marks tests as requiring network access"
    )
    config.addinivalue_line(
        "markers", "mne_dataset: marks tests as requiring MNE dataset download"
    )
