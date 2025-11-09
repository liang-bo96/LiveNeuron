# LiveNeuron

[![Tests](https://github.com/liang-bo96/LiveNeuron/actions/workflows/test.yml/badge.svg)](https://github.com/liang-bo96/LiveNeuron/actions/workflows/test.yml)
[![Lint](https://github.com/liang-bo96/LiveNeuron/actions/workflows/lint.yml/badge.svg)](https://github.com/liang-bo96/LiveNeuron/actions/workflows/lint.yml)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Interactive 2D brain visualization using Plotly and Dash. A standalone Python package for creating web-based brain activity visualizations with performance-optimized arrow rendering.

## Features

- 🧠 **Multiple display modes** - 10+ anatomical view configurations (ortho, lyr, lzry, etc.)
- 📐 **Flexible layouts** - Vertical (traditional) or horizontal (compact) arrangements
- 🦋 **Interactive butterfly plots** with real-time hover and click navigation
- ⚡ **Optimized arrow rendering** using Plotly's quiver plots for vector data
- 🎯 **Smart arrow filtering** with auto-threshold and custom magnitude filtering
- 🎨 **Customizable colormaps** and arrow scaling for optimal visualization
- 🔧 **Flexible data input** - supports Eelbrain NDVar and MNE sample data
- 📊 **Export capabilities** for static images (PNG, JPG, SVG, PDF)
- 📱 **Jupyter notebook support** with inline and JupyterLab modes
- 🌈 **Unified view sizing** - consistent brain plot dimensions across all views
- 🎛️ **Real-time mode** - dynamic updates on hover for rapid exploration

## Installation

### Install from GitHub

```bash
# Basic installation
pip install git+https://github.com/liang-bo96/LiveNeuron.git

# With optional Eelbrain support
pip install "git+https://github.com/liang-bo96/LiveNeuron.git[eelbrain]"

# Development installation
pip install "git+https://github.com/liang-bo96/LiveNeuron.git[dev]"
```

### Local Development

```bash
git clone https://github.com/liang-bo96/LiveNeuron.git
cd LiveNeuron
pip install -e .
```

## Quick Start

### Basic Usage with Sample Data

```python
from eelbrain_plotly_viz import EelbrainPlotly2DViz

# Create visualization with sample data
viz = EelbrainPlotly2DViz()

# Run interactive dashboard
viz.run()  # The port is random, check the console output for the URL.
```

### Using Built-in MNE Sample Data with Custom Options

```python
from eelbrain_plotly_viz import EelbrainPlotly2DViz

# Create visualization with custom options
viz = EelbrainPlotly2DViz(
    y=None,                      # Use built-in sample data
    region=None,                 # Use full brain (or specify 'aparc+aseg' for parcellation)
    cmap='YlOrRd',              # Custom colormap (Yellow-Orange-Red)
    show_max_only=True,         # Show only mean and max in butterfly plot
    arrow_threshold='auto',     # Show only significant arrows (>10% of max)
    arrow_scale=1.0,            # Default arrow length (0.5=shorter, 2.0=longer)
    layout_mode='horizontal',   # Compact horizontal layout
    display_mode='lyr',         # Left + Coronal + Right hemisphere views
    realtime=True               # Enable real-time hover updates
)

viz.run()
```

### Using Eelbrain NDVar Data

```python
from eelbrain import datasets
from eelbrain_plotly_viz import EelbrainPlotly2DViz

# Load Eelbrain data
data_ds = datasets.get_mne_sample(src='vol', ori='vector')
y = data_ds['src']  # NDVar format

# Visualize
viz = EelbrainPlotly2DViz(y=y)
viz.run()
```

### Jupyter Notebook Usage

```python
from eelbrain_plotly_viz import EelbrainPlotly2DViz

# Create and display in notebook
viz = EelbrainPlotly2DViz()
viz.show_in_jupyter(width=1200, height=900)  # Interactive display in notebook
```

### Using Sample Data Generator

```python
from eelbrain_plotly_viz import create_sample_brain_data

# Create sample data (for testing or development)
data_dict = create_sample_brain_data(
    n_sources=200,
    n_times=100, 
    has_vector_data=True,
    random_seed=42
)

# Note: The sample data generator creates a dictionary with:
# - 'coords': (n_sources, 3) array of source coordinates
# - 'data': (n_sources, 3, n_times) or (n_sources, n_times) array
# - 'time_values': (n_times,) array of time points
# 
# To use this data, you need to convert it to Eelbrain NDVar format
# or use the built-in MNE sample data instead:
from eelbrain_plotly_viz import EelbrainPlotly2DViz

viz = EelbrainPlotly2DViz()  # Uses built-in MNE sample data
viz.run()
```

## Advanced Usage

### Display Modes

LiveNeuron supports multiple anatomical view configurations:

```python
# Orthogonal views (traditional 3-view)
viz = EelbrainPlotly2DViz(display_mode='ortho')  # Sagittal + Coronal + Axial

# Single views
viz = EelbrainPlotly2DViz(display_mode='x')  # Sagittal only
viz = EelbrainPlotly2DViz(display_mode='y')  # Coronal only
viz = EelbrainPlotly2DViz(display_mode='z')  # Axial only

# Dual views
viz = EelbrainPlotly2DViz(display_mode='xz')  # Sagittal + Axial
viz = EelbrainPlotly2DViz(display_mode='yx')  # Coronal + Sagittal
viz = EelbrainPlotly2DViz(display_mode='yz')  # Coronal + Axial

# Hemisphere views (best for lateralized activity)
viz = EelbrainPlotly2DViz(display_mode='l')   # Left hemisphere only
viz = EelbrainPlotly2DViz(display_mode='r')   # Right hemisphere only
viz = EelbrainPlotly2DViz(display_mode='lr')  # Both hemispheres

# Combined hemisphere views (recommended for comprehensive visualization)
viz = EelbrainPlotly2DViz(display_mode='lyr')   # Left + Coronal + Right (GlassBrain default)
viz = EelbrainPlotly2DViz(display_mode='lzr')   # Left + Axial + Right

# 4-view comprehensive modes
viz = EelbrainPlotly2DViz(display_mode='lyrz')  # Left + Coronal + Right + Axial
viz = EelbrainPlotly2DViz(display_mode='lzry')  # Left + Axial + Right + Coronal
```

### Layout Modes

```python
# Vertical layout (traditional, butterfly plot on top)
viz = EelbrainPlotly2DViz(
    layout_mode='vertical',
    display_mode='ortho'
)

# Horizontal layout (compact, butterfly plot on left)
viz = EelbrainPlotly2DViz(
    layout_mode='horizontal',
    display_mode='lyr'
)
```

### Custom Visualization Options

```python
# Custom colormap (list format)
custom_cmap = [
    [0, 'rgba(255,255,255,0.8)'],  # White with 80% transparency (low activity)
    [0.5, 'rgba(255,165,0,0.9)'],  # Orange with 90% transparency
    [1, 'rgba(255,0,0,1.0)']       # Red with full opacity (high activity)
]

viz = EelbrainPlotly2DViz(
    y=None,                       # Use built-in data
    region='aparc+aseg',         # Apply parcellation
    cmap=custom_cmap,            # Custom colormap
    show_max_only=False,         # Show individual traces in butterfly plot
    arrow_threshold=0.1,         # Custom arrow threshold (magnitude > 0.1)
    arrow_scale=0.5,             # Shorter arrows for dense data
    layout_mode='horizontal',    # Compact layout
    display_mode='lyrz',         # 4-view comprehensive mode
    realtime=False               # Click-to-update mode (default)
)
```

### Export Static Images

```python
# Export all views as PNG images
result = viz.export_images(
    output_dir="./my_brain_plots",
    time_idx=30,
    format="png"
)

if result["status"] == "success":
    print("Exported files:")
    for plot_type, filepath in result["files"].items():
        print(f"  {plot_type}: {filepath}")
```

### Custom Server Configuration

```python
# Run on custom port with different modes
viz.run(port=8888, debug=True)                    # External browser
viz.run(mode='inline', width=1200, height=900)    # Jupyter inline
viz.run(mode='jupyterlab', width=1400, height=1000)  # JupyterLab tab
```

## Data Formats

### Vector Data
For data with direction and magnitude (e.g., current dipoles):
- **Eelbrain**: NDVar with dimensions `([case,] time, source, space)`
- **MNE Sample**: Built-in volumetric source data with 3D vectors

### Scalar Data  
For data with magnitude only (e.g., power, activation):
- **Eelbrain**: NDVar with dimensions `([case,] time, source)`

### Built-in Sample Data
LiveNeuron includes MNE sample data for immediate testing:
- Volumetric source space with 1589 sources
- Vector data (3D current dipoles)
- 76 time points from -100ms to 400ms
- Optional brain region filtering via parcellation

## Performance Features

### Optimized Arrow Rendering
- **Plotly quiver plots**: Fast vector field visualization using `ff.create_quiver`
- **Smart deduplication**: Automatic handling of overlapping 2D projections
- **Magnitude-based filtering**: Show only significant arrows with auto-threshold
- **Batch rendering**: Efficient creation of hundreds of arrows simultaneously
- **Fallback support**: Annotation-based rendering when quiver plots fail

### Visualization Optimizations
- **Unified view sizing**: Pre-calculated axis ranges for consistent brain plot dimensions
- **Global colormap**: Fixed color scale across all time points for intuitive comparison
- **Binned statistics**: Efficient heatmap generation using `scipy.stats.binned_statistic_2d`
- **Fixed axis ranges**: Prevents size changes during time navigation
- **Optimized layouts**: Zero-margin brain plots for maximum space utilization

### Memory Efficiency
- Efficient data handling for large datasets
- Vectorized NumPy operations for coordinate transformations
- Optimized for real-time interaction with cursor-based time selection

## Visualization Components

### Brain Projections
- **Multiple anatomical views**: 10+ display mode configurations (ortho, lyr, lyrz, etc.)
- **Hemisphere views**: Specialized left/right lateral projections with Y-axis flipping for left hemisphere
- **Interactive heatmaps**: 
  - Activity magnitude visualization using `scipy.stats.binned_statistic_2d` for accurate binning
  - Hover shows "Activity: value" with 3 decimal precision
  - Heatmap hover enabled, arrow hover disabled for clarity
- **Vector arrows**: 
  - Directional flow visualization using Plotly `ff.create_quiver` 
  - Magnitude-based filtering (None, 'auto' for 10% threshold, or custom float)
  - Arrow head size scales with vector length (Plotly default behavior)
  - Hover disabled on arrows to avoid confusion with heatmap values
- **Unified sizing**: 
  - All brain plots maintain consistent dimensions through pre-calculated axis ranges
  - `scaleanchor="y"` and `scaleratio=1` for equal aspect ratio
  - `domain=[0, 1]` for full plot area utilization
- **Global colormap**: Fixed color scale (zmin/zmax) across all time points for intuitive temporal comparison
- **Smart deduplication**: Automatic selection of maximum activity when multiple 3D sources project to same 2D position
- **Zero-margin layout**: `margin=dict(l=0, r=0, t=30, b=0)` for optimized space utilization (horizontal mode)
- **Background**: White background (`plot_bgcolor="white"`) by default (dark background option commented out)

### Butterfly Plot
- **Time series visualization**: Brain activity magnitude over time
- **Multiple trace modes**: 
  - Individual source traces (when `show_max_only=False`, shows subset for performance)
  - Mean activity trace (always shown, red line with hover showing "Mean: value")
  - Maximum activity trace (always shown, dark blue line with hover showing "Max: value")
- **Precise time navigation**: 
  - Click mode (default): Explicit time selection by clicking on plot
  - Real-time mode: Dynamic hover-based updates with cursor tracking using `spikesnap="cursor"`
- **Auto-scaled units**: Automatic pA/nA/µA scaling based on data magnitude for optimal visibility
- **Optimized x-axis**: Exact data range `[time_min, time_max]` with no empty space
- **Unified hover**: `hovermode="x unified"` shows all traces at cursor position simultaneously

### Interactive Controls
- **Dual interaction modes**:
  - **Click mode** (default): Click butterfly plot to update brain views
  - **Real-time mode**: Hover over butterfly plot for instant updates
- **Precise time selection**: Cursor-based spike tracking (`spikesnap="cursor"`) for accurate time picking
- **Source selection**: Click on brain sources for detailed coordinate information
- **Synchronized updates**: All views update together for consistent visualization
- **Status indicators**: Real-time feedback on current time and selected sources
- **Horizontal colorbar**: Unified color scale display below brain plots (in horizontal layout mode)

**Note**: Individual brain plot colorbars are currently hidden to ensure consistent plot sizing. The horizontal colorbar below all brain plots (in horizontal layout) provides the unified color scale reference.

## Requirements

### Core Dependencies
- `dash >= 2.0.0` - Web application framework
- `plotly >= 5.0.0` - Interactive plotting
- `numpy >= 1.20.0` - Numerical computing
- `matplotlib >= 3.3.0` - Additional plotting support
- `scipy >= 1.7.0` - Scientific computing

### Optional Dependencies
- `eelbrain` - For NDVar data support and advanced parcellation
- `kaleido` - For image export (auto-installed with plotly)

## Examples

### Complete Example Script

```python
#!/usr/bin/env python3
"""
Complete example of LiveNeuron brain visualization usage.
"""

from eelbrain_plotly_viz import EelbrainPlotly2DViz

def main():
    print("🧠 Creating LiveNeuron Brain Visualization...")
    
    # Method 1: Use built-in sample data with default settings
    print("\n1. Basic visualization with sample data:")
    viz1 = EelbrainPlotly2DViz()
    
    # Method 2: Custom visualization options
    print("\n2. Custom visualization with Reds colormap:")
    viz2 = EelbrainPlotly2DViz(
        y=None,
        region=None,
        cmap='Reds',
        show_max_only=True,
        arrow_threshold='auto'
    )
    
    # Method 3: With brain region filtering
    print("\n3. With parcellation (aparc+aseg):")
    viz3 = EelbrainPlotly2DViz(
        y=None,
        region='aparc+aseg',
        cmap='Viridis',
        show_max_only=False,
        arrow_threshold=0.1
    )
    
    # Export images
    print("\n📷 Exporting images...")
    result = viz3.export_images(
        output_dir="./example_output", 
        time_idx=20,
        format="png"
    )
    
    # Run interactive visualization
    print("\n🌐 Starting interactive visualization...")
    print("The server will start on a random port. Check the console for the exact URL to use.")
    viz3.run()

if __name__ == "__main__":
    main()
```

## API Reference

### EelbrainPlotly2DViz Class

#### Constructor
```python
EelbrainPlotly2DViz(
    y=None,                      # Data input (NDVar or None for sample data)
    region=None,                 # Brain region ('aparc+aseg' or None for full brain)
    cmap='YlOrRd',              # Colormap (string or custom list)
    show_max_only=False,         # Butterfly plot mode (True: mean+max only)
    arrow_threshold=None,        # Arrow display threshold (None, 'auto', or float)
    arrow_scale=1.0,             # Arrow length scale (0.5=short, 1.0=default, 2.0=long)
    realtime=False,              # Enable real-time hover updates (default: click mode)
    layout_mode='vertical',      # Layout: 'vertical' or 'horizontal'
    display_mode='lyr'           # Display mode: 'ortho', 'lyr', 'lyrz', etc.
)
```

#### Parameters
- **y** (NDVar, optional): Input data with dimensions `([case,] time, source[, space])`. If None, uses MNE sample data.
- **region** (str, optional): Brain region for parcellation (e.g., 'aparc+aseg'). If None, uses full brain.
- **cmap** (str or list): Plotly colorscale name or custom colorscale list. Default: 'YlOrRd'.
- **show_max_only** (bool): If True, butterfly plot shows only mean and max traces. Default: False.
- **arrow_threshold** (None, 'auto', or float): Threshold for displaying arrows. 'auto' uses 10% of max magnitude.
- **arrow_scale** (float): Relative arrow length multiplier. Default: 1.0. Range: 0.5-2.0.
- **realtime** (bool): Enable real-time hover updates. Default: False (click mode).
- **layout_mode** (str): 'vertical' (butterfly on top) or 'horizontal' (butterfly on left). Default: 'vertical'.
- **display_mode** (str): Anatomical view configuration. Options: 'ortho', 'x', 'y', 'z', 'xz', 'yx', 'yz', 'l', 'r', 'lr', 'lyr', 'lzr', 'lyrz', 'lzry'. Default: 'lyr'.

#### Methods
- `run(port=None, debug=True, mode='external', width=1200, height=900)` - Start interactive app
- `show_in_jupyter(width=1200, height=900, debug=False)` - Display inline in Jupyter
- `export_images(output_dir, time_idx=None, format='png')` - Export static images
- `create_2d_brain_projections_plotly(time_idx, source_idx=None)` - Get projection figures
- `create_butterfly_plot(selected_time_idx=0)` - Get butterfly plot figure

### Sample Data Functions

#### create_sample_brain_data
```python
create_sample_brain_data(
    n_sources=200,             # Number of brain sources
    n_times=50,                # Number of time points  
    has_vector_data=True,      # Vector vs scalar data
    random_seed=42             # Random seed
)
```

## Contributing

We welcome contributions! Please see our contributing guidelines for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Running Tests

Our project uses pytest for testing with GitHub Actions for continuous integration.

#### Quick test run:
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run fast tests (skips slow performance tests)
pytest -m "not slow"

# Run all tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=term-missing
```

#### Test types:
- **Basic tests**: Core functionality (`test_basic.py`)
- **Integration tests**: End-to-end workflows (`test_integration.py`)  
- **Performance tests**: Memory usage and speed (`test_performance.py`)

#### CI/CD:
- Tests run automatically on push/PR for Python 3.8-3.11
- Code quality checks with flake8 and black
- Coverage reporting with codecov

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use this package in your research, please cite:

```bibtex
@software{liveneuron,
  title={LiveNeuron: Interactive 2D Brain Visualization},
  author={LiveNeuron Team},
  year={2024},
  url={https://github.com/liang-bo96/LiveNeuron}
}
```

## Support

- 📖 **Documentation**: See this README and docstrings
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/liang-bo96/LiveNeuron/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/liang-bo96/LiveNeuron/discussions)
- 📧 **Email**: liveneuron@example.com

## Changelog

### v2.0.0 (2025)
- **New Features**:
  - 10+ display modes (ortho, lyr, lyrz, hemisphere views, etc.)
  - Horizontal and vertical layout modes
  - Real-time hover mode for rapid time exploration
  - Unified view sizing for consistent brain plot dimensions
  - Horizontal colorbar for horizontal layouts
  - Arrow scaling parameter for customizable vector visualization
- **Performance Improvements**:
  - Quiver plot-based arrow rendering using `ff.create_quiver`
  - Smart deduplication for overlapping 2D projections
  - Optimized time selection with cursor-based spike tracking
  - Zero-margin layouts for maximum space utilization
- **Bug Fixes**:
  - Fixed brain plot size consistency across all views
  - Improved time axis precision with `spikesnap="cursor"`
  - Corrected hover value display for overlapping voxels
  - Fixed colorbar interference with brain plot sizing

### v1.0.0 (2024)
- Initial release
- Interactive 2D brain projections with axial, sagittal, and coronal views
- Optimized arrow rendering
- Support for Eelbrain NDVar and built-in MNE sample data
- Jupyter notebook integration with modern Dash support
- Image export capabilities
- Customizable colormaps and arrow thresholds
- Real-time interactive controls 