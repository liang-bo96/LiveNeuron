"""
Basic tests for eelbrain_plotly_viz package.
"""

import pytest


def test_package_import():
    """Test that the package can be imported."""
    import eelbrain_plotly_viz

    assert hasattr(eelbrain_plotly_viz, "EelbrainPlotly2DViz")
    assert hasattr(eelbrain_plotly_viz, "BrainPlotly2DViz")  # Alias
    assert hasattr(eelbrain_plotly_viz, "create_sample_brain_data")


def test_sample_data_creation():
    """Test sample data creation."""
    from eelbrain_plotly_viz.sample_data import create_sample_brain_data

    # Test vector data
    data_dict = create_sample_brain_data(
        n_sources=50, n_times=20, has_vector_data=True, random_seed=42
    )

    assert "data" in data_dict
    assert "coords" in data_dict
    assert "times" in data_dict
    assert "has_vector_data" in data_dict
    assert data_dict["has_vector_data"] is True
    assert data_dict["data"].shape == (50, 20, 3)
    assert data_dict["coords"].shape == (50, 3)
    assert data_dict["times"].shape == (20,)


def test_scalar_data_creation():
    """Test scalar data creation."""
    from eelbrain_plotly_viz.sample_data import create_sample_brain_data

    # Test scalar data
    data_dict = create_sample_brain_data(
        n_sources=30, n_times=15, has_vector_data=False, random_seed=123
    )

    assert data_dict["has_vector_data"] is False
    assert data_dict["data"].shape == (30, 15)
    assert data_dict["coords"].shape == (30, 3)
    assert data_dict["times"].shape == (15,)


def test_viz_creation_with_sample_data():
    """Test creating visualization with default sample data."""
    from eelbrain_plotly_viz import EelbrainPlotly2DViz

    # This should work without errors
    viz = EelbrainPlotly2DViz()

    assert viz.glass_brain_data is not None
    assert viz.source_coords is not None
    assert viz.time_values is not None
    assert hasattr(viz, "region_of_brain")
    assert hasattr(viz, "cmap")
    assert hasattr(viz, "show_max_only")
    assert hasattr(viz, "arrow_threshold")


def test_viz_creation_with_options():
    """Test creating visualization with different options."""
    from eelbrain_plotly_viz import EelbrainPlotly2DViz

    # Test with different parameters
    viz = EelbrainPlotly2DViz(
        y=None, region=None, cmap="Viridis", show_max_only=True, arrow_threshold="auto"
    )

    assert viz.glass_brain_data is not None
    assert viz.source_coords is not None
    assert viz.time_values is not None
    assert viz.cmap == "Viridis"
    assert viz.show_max_only is True
    assert viz.arrow_threshold == "auto"


def test_alias_import():
    """Test that the BrainPlotly2DViz alias works."""
    from eelbrain_plotly_viz import BrainPlotly2DViz, EelbrainPlotly2DViz

    # The alias should be the same as the original class
    assert BrainPlotly2DViz is EelbrainPlotly2DViz

    # Should be able to create instance with alias
    viz = BrainPlotly2DViz()
    assert viz.glass_brain_data is not None


def test_brain_projections():
    """Test brain projection creation."""
    from eelbrain_plotly_viz import EelbrainPlotly2DViz

    # Test with ortho display mode (3 orthogonal views)
    viz = EelbrainPlotly2DViz(display_mode="ortho")
    projections = viz._create_2d_brain_projections_plotly(time_idx=5)

    assert isinstance(projections, dict)
    assert "axial" in projections
    assert "sagittal" in projections
    assert "coronal" in projections

    # Check that each projection is a plotly figure
    for view_name, fig in projections.items():
        assert hasattr(fig, "data")
        assert hasattr(fig, "layout")

    # Test with default display mode (lyr - hemisphere views)
    viz_default = EelbrainPlotly2DViz()
    projections_default = viz_default.create_2d_brain_projections_plotly(time_idx=5)

    assert isinstance(projections_default, dict)
    assert "left_hemisphere" in projections_default
    assert "coronal" in projections_default
    assert "right_hemisphere" in projections_default


def test_butterfly_plot():
    """Test butterfly plot creation."""
    from eelbrain_plotly_viz import EelbrainPlotly2DViz

    viz = EelbrainPlotly2DViz()
    butterfly_fig = viz._create_butterfly_plot()

    assert hasattr(butterfly_fig, "data")
    assert hasattr(butterfly_fig, "layout")
    assert len(butterfly_fig.data) > 0  # Should have at least mean and max traces


def test_custom_colormap():
    """Test custom colormap functionality."""
    from eelbrain_plotly_viz import EelbrainPlotly2DViz

    # Test custom colormap
    custom_cmap = [[0, "yellow"], [0.5, "orange"], [1, "red"]]

    viz = EelbrainPlotly2DViz(cmap=custom_cmap)
    assert viz.cmap == custom_cmap


def test_different_arrow_thresholds():
    """Test different arrow threshold settings."""
    from eelbrain_plotly_viz import EelbrainPlotly2DViz

    # Test None threshold
    viz1 = EelbrainPlotly2DViz(arrow_threshold=None)
    assert viz1.arrow_threshold is None

    # Test auto threshold
    viz2 = EelbrainPlotly2DViz(arrow_threshold="auto")
    assert viz2.arrow_threshold == "auto"

    # Test numeric threshold
    viz3 = EelbrainPlotly2DViz(arrow_threshold=0.5)
    assert viz3.arrow_threshold == 0.5


def test_show_max_only_option():
    """Test show_max_only parameter."""
    from eelbrain_plotly_viz import EelbrainPlotly2DViz

    # Test with show_max_only=True
    viz1 = EelbrainPlotly2DViz(show_max_only=True)
    butterfly_fig1 = viz1._create_butterfly_plot()

    # Test with show_max_only=False
    viz2 = EelbrainPlotly2DViz(show_max_only=False)
    butterfly_fig2 = viz2._create_butterfly_plot()

    # Both should create valid figures
    assert hasattr(butterfly_fig1, "data")
    assert hasattr(butterfly_fig2, "data")

    # The number of traces might be different
    # (show_max_only=True should have fewer traces)
    assert len(butterfly_fig1.data) > 0
    assert len(butterfly_fig2.data) > 0


@pytest.mark.skipif(True, reason="eelbrain dependency not always available")
def test_eelbrain_integration():
    """Test integration with eelbrain (if available)."""
    try:
        from eelbrain import datasets
        from eelbrain_plotly_viz import EelbrainPlotly2DViz

        # Load eelbrain data
        data_ds = datasets.get_mne_sample(src="vol", ori="vector")
        y = data_ds["src"]

        # Create visualization with eelbrain data
        viz = EelbrainPlotly2DViz(y=y)

        assert viz.glass_brain_data is not None
        assert viz.source_coords is not None
        assert viz.time_values is not None

    except ImportError:
        pytest.skip("eelbrain not available")


def test_app_creation():
    """Test that the Dash app is created properly."""
    from eelbrain_plotly_viz import EelbrainPlotly2DViz

    viz = EelbrainPlotly2DViz()

    # Check that the app exists and has the expected attributes
    assert hasattr(viz, "app")
    assert hasattr(viz.app, "layout")
    assert hasattr(viz.app, "callback_map")
