"""
Sample data generator for brain visualization.

Provides synthetic brain data for testing and demonstration purposes
without requiring eelbrain dependencies.
"""

import numpy as np
from typing import Tuple, Dict, Any, Optional


def create_sample_brain_data(
    n_sources: int = 200,
    n_times: int = 50,
    has_vector_data: bool = True,
    random_seed: int = 42
) -> Dict[str, Any]:
    """
    Create synthetic brain data for visualization testing.
    
    Parameters
    ----------
    n_sources : int, default 200
        Number of brain sources/vertices.
    n_times : int, default 50
        Number of time points.
    has_vector_data : bool, default True
        Whether to include vector (3D) data or just scalar data.
    random_seed : int, default 42
        Random seed for reproducible data.
        
    Returns
    -------
    data_dict : dict
        Dictionary containing:
        - 'data': numpy array of shape (n_sources, n_times, 3) for vector data
                 or (n_sources, n_times) for scalar data
        - 'coords': numpy array of shape (n_sources, 3) with source coordinates
        - 'times': numpy array of shape (n_times,) with time values
        - 'has_vector_data': bool indicating data type
    """
    np.random.seed(random_seed)
    
    # Create realistic brain-like coordinates
    # Simulate brain volume roughly within [-0.08, 0.08] meters
    coords = _create_brain_coordinates(n_sources)
    
    # Create time values (0 to 0.5 seconds)
    times = np.linspace(0, 0.5, n_times)
    
    if has_vector_data:
        # Create vector data (n_sources, n_times, 3)
        data = _create_vector_brain_activity(n_sources, n_times, coords, times)
    else:
        # Create scalar data (n_sources, n_times)
        data = _create_scalar_brain_activity(n_sources, n_times, coords, times)
    
    return {
        'data': data,
        'coords': coords,
        'times': times,
        'has_vector_data': has_vector_data,
        'n_sources': n_sources,
        'n_times': n_times
    }


def _create_brain_coordinates(n_sources: int) -> np.ndarray:
    """Create realistic brain-like 3D coordinates."""
    # Create coordinates that roughly follow brain shape
    coords = np.zeros((n_sources, 3))
    
    # Generate coordinates in layers (axial slices)
    n_layers = 8
    sources_per_layer = n_sources // n_layers
    
    for layer in range(n_layers):
        start_idx = layer * sources_per_layer
        end_idx = min((layer + 1) * sources_per_layer, n_sources)
        n_layer_sources = end_idx - start_idx
        
        # Z coordinate (superior-inferior): -0.04 to 0.06 meters
        z = -0.04 + (layer / (n_layers - 1)) * 0.10
        
        # Create roughly brain-shaped cross-section at this Z level
        # Use a combination of sphere and ellipsoid
        for i in range(n_layer_sources):
            # Random angle
            theta = np.random.uniform(0, 2 * np.pi)
            phi = np.random.uniform(0, np.pi)
            
            # Brain-like radial distance (smaller at top and bottom)
            brain_factor = 0.5 + 0.5 * np.cos(phi)  # Smaller at poles
            radius = np.random.uniform(0.02, 0.08) * brain_factor
            
            # Convert to Cartesian (roughly brain-shaped)
            x = radius * np.sin(phi) * np.cos(theta) * 0.8  # Slightly flattened
            y = radius * np.sin(phi) * np.sin(theta) * 1.2  # Elongated front-back
            
            coords[start_idx + i] = [x, y, z]
    
    return coords


def _create_scalar_brain_activity(
    n_sources: int, 
    n_times: int, 
    coords: np.ndarray, 
    times: np.ndarray
) -> np.ndarray:
    """Create realistic scalar brain activity patterns."""
    data = np.zeros((n_sources, n_times))
    
    # Create multiple activity patterns
    n_patterns = 3
    
    for pattern in range(n_patterns):
        # Random center of activity
        center = coords[np.random.randint(0, n_sources)]
        
        # Time course (Gaussian pulse)
        peak_time = 0.1 + pattern * 0.15
        time_width = 0.05
        time_course = np.exp(-0.5 * ((times - peak_time) / time_width) ** 2)
        
        # Spatial pattern (distance-based decay)
        for i, coord in enumerate(coords):
            distance = np.linalg.norm(coord - center)
            spatial_decay = np.exp(-distance / 0.03)  # 3cm decay
            
            # Add noise and scale
            amplitude = spatial_decay * np.random.uniform(0.5, 2.0)
            noise = np.random.normal(0, 0.1, n_times)
            
            data[i] += amplitude * time_course + noise
    
    # Add baseline noise
    data += np.random.normal(0, 0.05, (n_sources, n_times))
    
    return data


def _create_vector_brain_activity(
    n_sources: int, 
    n_times: int, 
    coords: np.ndarray, 
    times: np.ndarray
) -> np.ndarray:
    """Create realistic vector brain activity patterns."""
    data = np.zeros((n_sources, n_times, 3))
    
    # Create scalar activity first
    scalar_activity = _create_scalar_brain_activity(n_sources, n_times, coords, times)
    
    # Convert to vector activity with realistic orientations
    for i, coord in enumerate(coords):
        for t in range(n_times):
            magnitude = abs(scalar_activity[i, t])
            
            if magnitude > 0.1:  # Only create vectors for significant activity
                # Create somewhat realistic dipole orientations
                # Tend to point radially outward from brain center
                direction = coord / (np.linalg.norm(coord) + 1e-6)
                
                # Add some randomness to direction
                random_perturbation = np.random.normal(0, 0.3, 3)
                direction = direction + random_perturbation
                direction = direction / (np.linalg.norm(direction) + 1e-6)
                
                # Scale by magnitude
                data[i, t] = direction * magnitude
            else:
                # Small random vectors for noise
                data[i, t] = np.random.normal(0, 0.02, 3)
    
    return data


def create_sample_mne_like_data() -> Dict[str, Any]:
    """
    Create sample data that mimics MNE/Eelbrain structure.
    
    Returns data with realistic brain activity patterns including:
    - Multiple temporal activation patterns
    - Realistic spatial correlations
    - Both scalar and vector components
    """
    # Create a larger, more realistic dataset
    return create_sample_brain_data(
        n_sources=400,
        n_times=100,
        has_vector_data=True,
        random_seed=12345
    ) 