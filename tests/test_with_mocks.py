"""
Tests for EelbrainPlotly2DViz using mocked MNE datasets.
This avoids downloading large datasets during testing.
"""

import pytest
from unittest.mock import patch
from src.eelbrain_plotly_viz import EelbrainPlotly2DViz, create_sample_brain_data

# Handle different import paths for different environments
try:
    from .mock_utils import mock_get_mne_sample, skip_if_ci
except ImportError:
    try:
        from tests.mock_utils import mock_get_mne_sample, skip_if_ci
    except ImportError:
        from mock_utils import mock_get_mne_sample, skip_if_ci


class TestEelbrainPlotly2DVizWithMock:
    """Test class using mocked MNE datasets."""

    @patch("eelbrain.datasets.get_mne_sample", side_effect=mock_get_mne_sample)
    def test_viz_creation_with_mocked_data(self, mock_get_sample):
        """Test creating visualization with mocked MNE data."""
        viz = EelbrainPlotly2DViz()

        # Verify that the visualization was created successfully
        assert viz.glass_brain_data is not None
        assert viz.glass_brain_data.shape[0] > 0  # Should have brain sources
        assert len(viz.time_values) > 0  # Should have time points
        assert viz.source_coords is not None
        assert viz.source_coords.shape[0] > 0  # Should have coordinates

        # Verify the mock was called
        mock_get_sample.assert_called_once()

    @patch("eelbrain.datasets.get_mne_sample", side_effect=mock_get_mne_sample)
    def test_viz_with_different_display_modes(self, mock_get_sample):
        """Test different display modes with mocked data."""
        display_modes = ["lyr", "ortho", "x", "y", "z"]

        for mode in display_modes:
            viz = EelbrainPlotly2DViz(display_mode=mode)
            assert viz.display_mode == mode
            assert viz.glass_brain_data is not None
            assert len(viz.brain_views) > 0

    @patch("eelbrain.datasets.get_mne_sample", side_effect=mock_get_mne_sample)
    def test_viz_with_different_layout_modes(self, mock_get_sample):
        """Test different layout modes with mocked data."""
        layout_modes = ["vertical", "horizontal"]

        for mode in layout_modes:
            viz = EelbrainPlotly2DViz(layout_mode=mode)
            assert viz.layout_mode == mode
            assert viz.glass_brain_data is not None

    @patch("eelbrain.datasets.get_mne_sample", side_effect=mock_get_mne_sample)
    def test_viz_with_custom_colormap(self, mock_get_sample):
        """Test custom colormap with mocked data."""
        custom_cmap = [[0, "blue"], [0.5, "white"], [1, "red"]]
        viz = EelbrainPlotly2DViz(cmap=custom_cmap)

        assert viz.cmap == custom_cmap
        assert viz.glass_brain_data is not None

    @patch("eelbrain.datasets.get_mne_sample", side_effect=mock_get_mne_sample)
    def test_viz_with_show_max_only(self, mock_get_sample):
        """Test show_max_only option with mocked data."""
        viz = EelbrainPlotly2DViz(show_max_only=True)

        assert viz.show_max_only is True
        assert viz.glass_brain_data is not None

    @patch("eelbrain.datasets.get_mne_sample", side_effect=mock_get_mne_sample)
    def test_dash_app_creation(self, mock_get_sample):
        """Test that Dash app is created properly with mocked data."""
        viz = EelbrainPlotly2DViz()

        # Check that the app was created
        assert viz.app is not None
        assert hasattr(viz.app, "layout")
        assert hasattr(viz.app, "callback_map")

    def test_basic_imports_work(self):
        """Test that basic imports work without any dataset dependencies."""
        # Test sample data creation (no network required)
        sample_data = create_sample_brain_data(n_sources=50, n_times=25)
        assert len(sample_data) == 6  # Should return dict with 6 keys
        assert "data" in sample_data  # Should have brain data
        assert "coords" in sample_data  # Should have coordinates

    def test_alias_import_works(self):
        """Test that the BrainPlotly2DViz alias works."""
        from src.eelbrain_plotly_viz import BrainPlotly2DViz, EelbrainPlotly2DViz

        # The alias should be the same as the original class
        assert BrainPlotly2DViz is EelbrainPlotly2DViz


class TestSkippedInCI:
    """Tests that are skipped in CI but can run locally with real data."""

    @skip_if_ci()
    def test_real_dataset_loading(self):
        """Test with real MNE dataset (skipped in CI)."""
        viz = EelbrainPlotly2DViz()

        # If this runs (not in CI), verify real data
        assert viz.glass_brain_data is not None
        assert viz.glass_brain_data.shape[0] > 1000  # Real dataset has more sources
        assert len(viz.time_values) > 50  # Real dataset has more time points


if __name__ == "__main__":
    # Run specific tests
    import sys

    print("🧪 Running mocked tests...")

    # Test basic functionality
    test_instance = TestEelbrainPlotly2DVizWithMock()

    try:
        # Run a simple test
        with patch("eelbrain.datasets.get_mne_sample", side_effect=mock_get_mne_sample):
            viz = EelbrainPlotly2DViz()
            print(f"✅ Mock test passed: {viz.glass_brain_data.shape[0]} sources")
    except Exception as e:
        print(f"❌ Mock test failed: {e}")
        sys.exit(1)

    print("🎉 All mock tests completed successfully!")
