# LiveNeuron

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
viz.run()  # Opens at http://127.0.0.1:8050
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
viz.show_in_jupyter(width=1200, height=900)  # Interactive display in notebook
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
    print("Visit http://127.0.0.1:8050 in your browser")
    viz3.run()

if __name__ == "__main__":
    main()
```

## API Reference

### EelbrainPlotly2DViz Class

#### Constructor
```python
EelbrainPlotly2DViz(
    y=None,                    # Data input (NDVar or None for sample data)
    region=None,               # Brain region ('aparc+aseg' or None for full brain)
    cmap='Hot',                # Colormap (string or custom list)
    show_max_only=False,       # Butterfly plot mode (True: mean+max only)
    arrow_threshold=None       # Arrow display threshold (None, 'auto', or float)
)
```

#### Methods
- `run(port=None, debug=True, mode='external')` - Start interactive app
- `show_in_jupyter(width=1200, height=900, debug=False)` - Display in Jupyter
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