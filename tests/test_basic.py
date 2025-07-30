"""
Basic tests for eelbrain_plotly_viz package.
"""

import pytest
import numpy as np


def test_package_import():
    """Test that the package can be imported."""
    import eelbrain_plotly_viz
    assert hasattr(eelbrain_plotly_viz, 'BrainPlotly2DViz')
    assert hasattr(eelbrain_plotly_viz, 'create_sample_brain_data')


def test_sample_data_creation():
    """Test sample data creation."""
    from eelbrain_plotly_viz import create_sample_brain_data
    
    # Test vector data
    data_dict = create_sample_brain_data(
        n_sources=50,
        n_times=20,
        has_vector_data=True,
        random_seed=42
    )
    
    assert 'data' in data_dict
    assert 'coords' in data_dict
    assert 'times' in data_dict
    assert 'has_vector_data' in data_dict
    assert data_dict['has_vector_data'] is True
    assert data_dict['data'].shape == (50, 20, 3)
    assert data_dict['coords'].shape == (50, 3)
    assert data_dict['times'].shape == (20,)


def test_scalar_data_creation():
    """Test scalar data creation."""
    from eelbrain_plotly_viz import create_sample_brain_data
    
    # Test scalar data
    data_dict = create_sample_brain_data(
        n_sources=30,
        n_times=15,
        has_vector_data=False,
        random_seed=123
    )
    
    assert data_dict['has_vector_data'] is False
    assert data_dict['data'].shape == (30, 15)
    assert data_dict['coords'].shape == (30, 3)
    assert data_dict['times'].shape == (15,)


def test_viz_creation_with_sample_data():
    """Test creating visualization with sample data."""
    from eelbrain_plotly_viz import BrainPlotly2DViz
    
    # This should work without errors
    viz = BrainPlotly2DViz()
    
    assert viz.glass_brain_data is not None
    assert viz.source_coords is not None
    assert viz.time_values is not None
    assert hasattr(viz, 'has_vector_data')


def test_viz_creation_with_numpy_data():
    """Test creating visualization with numpy arrays."""
    from eelbrain_plotly_viz import BrainPlotly2DViz
    
    # Create test data
    data = np.random.rand(20, 10, 3)  # Vector data
    coords = np.random.rand(20, 3) * 0.1 - 0.05
    times = np.linspace(0, 1, 10)
    
    viz = BrainPlotly2DViz(y=data, coords=coords, times=times)
    
    assert viz.glass_brain_data is not None
    assert viz.source_coords is not None
    assert viz.time_values is not None
    assert viz.has_vector_data is True


def test_viz_creation_with_dict_data():
    """Test creating visualization with dictionary data."""
    from eelbrain_plotly_viz import BrainPlotly2DViz, create_sample_brain_data
    
    data_dict = create_sample_brain_data(n_sources=25, n_times=12)
    viz = BrainPlotly2DViz(y=data_dict)
    
    assert viz.glass_brain_data is not None
    assert viz.source_coords is not None
    assert viz.time_values is not None


def test_brain_projections():
    """Test brain projection creation."""
    from eelbrain_plotly_viz import BrainPlotly2DViz
    
    viz = BrainPlotly2DViz()
    projections = viz.create_2d_brain_projections_plotly(time_idx=5)
    
    assert isinstance(projections, dict)
    assert 'axial' in projections
    assert 'sagittal' in projections
    assert 'coronal' in projections
    
    # Check that each projection is a plotly figure
    for view_name, fig in projections.items():
        assert hasattr(fig, 'data')
        assert hasattr(fig, 'layout')


def test_butterfly_plot():
    """Test butterfly plot creation."""
    from eelbrain_plotly_viz import BrainPlotly2DViz
    
    viz = BrainPlotly2DViz()
    butterfly_fig = viz.create_butterfly_plot()
    
    assert hasattr(butterfly_fig, 'data')
    assert hasattr(butterfly_fig, 'layout')
    assert len(butterfly_fig.data) > 0  # Should have at least mean and max traces


def test_error_handling():
    """Test error handling for invalid inputs."""
    from eelbrain_plotly_viz import BrainPlotly2DViz
    
    # Test missing coords parameter
    with pytest.raises(ValueError, match="coords parameter is required"):
        data = np.random.rand(10, 5, 3)
        BrainPlotly2DViz(y=data)
    
    # Test missing times parameter
    with pytest.raises(ValueError, match="times parameter is required"):
        data = np.random.rand(10, 5, 3)
        coords = np.random.rand(10, 3)
        BrainPlotly2DViz(y=data, coords=coords)
    
    # Test invalid data dictionary
    with pytest.raises(ValueError, match="Missing required key"):
        invalid_dict = {'data': np.random.rand(10, 5)}  # Missing required keys
        BrainPlotly2DViz(y=invalid_dict) 