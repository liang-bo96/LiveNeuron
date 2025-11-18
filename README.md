# LiveNeuron

[![Tests](https://github.com/liang-bo96/LiveNeuron/actions/workflows/test.yml/badge.svg)](https://github.com/liang-bo96/LiveNeuron/actions/workflows/test.yml)
[![Lint](https://github.com/liang-bo96/LiveNeuron/actions/workflows/lint.yml/badge.svg)](https://github.com/liang-bo96/LiveNeuron/actions/workflows/lint.yml)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Interactive 2D brain visualization using Plotly and Dash. A standalone Python package for creating web-based brain activity visualizations with performance-optimized arrow rendering.

## Features

- 🧠 **Interactive 2D brain projections** (axial, sagittal, coronal views)
- 🦋 **Butterfly plots** for time series visualization
- ⚡ **453x faster arrow rendering** using optimized batch techniques
- 🎛️ **Real-time controls** for time navigation and interaction
- 🔧 **Flexible data input** - supports Eelbrain NDVar, numpy arrays, and dictionaries
- 📊 **Export capabilities** for static images
- 📱 **Jupyter notebook support** for interactive development
- 🎨 **Customizable colormaps** and visualization options

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
    y=None,                    # Use built-in sample data
    region=None,               # Use full brain (or specify 'aparc+aseg' for parcellation)
    cmap='Viridis',           # Custom colormap
    show_max_only=True,       # Show only mean and max in butterfly plot
    arrow_threshold='auto'     # Show only significant arrows
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
viz.run(mode='inline', width=1200, height=900)  # Interactive display in notebook
```

### Using Sample Data Generator

```python
from eelbrain_plotly_viz import EelbrainPlotly2DViz, create_sample_brain_data

# Create sample data
data_dict = create_sample_brain_data(
    n_sources=200,
    n_times=100, 
    has_vector_data=True
)

# Note: Direct dictionary input not supported in current implementation
# Use built-in sample data or Eelbrain NDVar instead
viz = EelbrainPlotly2DViz()  # Uses built-in MNE sample data
viz.run()
```

## Advanced Usage

### Custom Visualization Options

```python
# Custom colormap (list format)
custom_cmap = [
    [0, 'rgba(255,255,0,0.5)'],    # Yellow with 50% transparency
    [0.5, 'rgba(255,165,0,0.8)'],  # Orange with 80% transparency
    [1, 'rgba(255,0,0,1.0)']       # Red with full opacity
]

viz = EelbrainPlotly2DViz(
    y=None,                       # Use built-in data
    region='aparc+aseg',         # Apply parcellation
    cmap=custom_cmap,            # Custom colormap
    show_max_only=False,         # Show individual traces in butterfly plot
    arrow_threshold=0.1          # Custom arrow threshold
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
- **453x speedup** over individual annotations
- Batch rendering using single Plotly traces
- Handles thousands of arrows smoothly
- Maintains full visual quality
- Automatic arrow filtering based on magnitude thresholds

### Memory Efficiency
- Efficient data handling for large datasets
- Optional data subsampling for performance
- Optimized for real-time interaction

## Visualization Components

### Brain Projections
- **Axial view**: Top-down brain slice (X vs Y)
- **Sagittal view**: Side brain slice (Y vs Z)  
- **Coronal view**: Front brain slice (X vs Z)
- Interactive heatmaps with directional arrow overlays
- Consistent colormaps across all views

### Butterfly Plot
- Time series of brain activity magnitude
- Individual source traces (optional, controlled by `show_max_only`)
- Mean and maximum activity traces
- Clickable time navigation
- Auto-scaled units for optimal visibility

### Interactive Controls
- Click on butterfly plot to navigate time
- Click on brain sources for detailed information
- Real-time synchronized updates across all views
- Status indicators for current time and selected sources

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
    print("\n2. Custom visualization with Hot colormap:")
    viz2 = EelbrainPlotly2DViz(
        y=None,
        region=None,
        cmap='Hot',
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

The main visualization class providing interactive 2D brain projections with butterfly plots.

#### Constructor

```python
EelbrainPlotly2DViz(
    y=None,                         # NDVar data input (or None for sample data)
    region=None,                    # Brain region filter (e.g., 'aparc+aseg')
    cmap='YlOrRd',                  # Colormap name or custom list
    show_max_only=False,            # Butterfly plot mode (True: mean+max only)
    arrow_threshold=None,           # Arrow display threshold (None/'auto'/float)
    arrow_scale=1.0,                # Arrow length scale factor (default: 1.0)
    realtime=False,                 # Enable real-time hover updates
    layout_mode='vertical',         # Layout: 'vertical' or 'horizontal'
    display_mode='lyr'              # View mode: 'ortho', 'lyr', 'lzry', etc.
)
```

**Parameters:**

- **y** (*NDVar, optional*): Data with dimensions ([case,] time, source[, space]). If None, uses MNE sample data.
- **region** (*str, optional*): Brain region to load using aparc+aseg parcellation. If None, loads all regions.
- **cmap** (*str or list*): Plotly colorscale. Built-in names like 'YlOrRd', 'Viridis', or custom list. Default: 'YlOrRd'.
- **show_max_only** (*bool*): If True, butterfly plot shows only mean and max traces. Default: False.
- **arrow_threshold** (*None, 'auto', or float*): Threshold for displaying arrows. None shows all, 'auto' uses 10% of max. Default: None.
- **arrow_scale** (*float*): Relative scale factor for arrow length. Use 0.5 for shorter, 2.0 for longer arrows. Default: 1.0.
- **realtime** (*bool*): Enable real-time updates on hover (not just click). Default: False.
- **layout_mode** (*str*): Layout arrangement: 'vertical' (butterfly top, brains below) or 'horizontal' (butterfly left, brains right). Default: 'vertical'.
- **display_mode** (*str*): Anatomical view mode. Options: 'ortho', 'x', 'y', 'z', 'xz', 'yx', 'yz', 'l', 'r', 'lr', 'lzr', 'lyr', 'lzry', 'lyrz'. Default: 'lyr'.

#### Public Methods

##### run()
```python
run(port=None, debug=True, mode='external', width=1200, height=900)
```
Start the interactive Dash application.

**Parameters:**
- **port** (*int, optional*): Server port number. If None, uses random port.
- **debug** (*bool*): Enable debug mode. Default: True.
- **mode** (*str*): Display mode - 'external' (browser), 'inline' (Jupyter), or 'jupyterlab'. Default: 'external'.
- **width** (*int*): Display width in pixels for Jupyter modes. Default: 1200.
- **height** (*int*): Display height in pixels for Jupyter modes. Default: 900.

##### export_images()
```python
export_images(output_dir='./images', time_idx=None, format='png')
```
Export current plots as image files.

**Parameters:**
- **output_dir** (*str*): Directory to save images. Default: './images'.
- **time_idx** (*int, optional*): Time index to export. If None, uses 0.
- **format** (*str*): Image format - 'png', 'jpg', 'svg', or 'pdf'. Default: 'png'.

**Returns:**
- *dict*: Dictionary with status and exported file paths.

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

### v1.0.0 (2024)
- Initial release
- Interactive 2D brain projections with axial, sagittal, and coronal views
- Optimized arrow rendering (453x speedup)
- Support for Eelbrain NDVar and built-in MNE sample data
- Jupyter notebook integration with modern Dash support
- Image export capabilities
- Customizable colormaps and arrow thresholds
- Real-time interactive controls 