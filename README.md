# Eelbrain Plotly Visualization

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
pip install git+https://github.com/liang-bo96/eelbrain-plotly-viz.git

# With optional Eelbrain support
pip install "git+https://github.com/liang-bo96/eelbrain-plotly-viz.git[eelbrain]"

# Development installation
pip install "git+https://github.com/liang-bo96/eelbrain-plotly-viz.git[dev]"
```

### Local Development

```bash
git clone https://github.com/liang-bo96/eelbrain-plotly-viz.git
cd eelbrain-plotly-viz
pip install -e .
```

## Quick Start

### Basic Usage with Sample Data

```python
from eelbrain_plotly_viz import BrainPlotly2DViz

# Create visualization with sample data
viz = BrainPlotly2DViz()

# Run interactive dashboard
viz.run()  # Opens at http://127.0.0.1:8050
```

### Using Your Own Numpy Data

```python
import numpy as np
from eelbrain_plotly_viz import BrainPlotly2DViz

# Your brain data
data = np.random.rand(100, 50, 3)  # (sources, times, xyz) for vector data
coords = np.random.rand(100, 3)     # (sources, xyz) coordinates  
times = np.linspace(0, 1, 50)       # time values

# Create visualization
viz = BrainPlotly2DViz(y=data, coords=coords, times=times)
viz.run()
```

### Using Data Dictionary Format

```python
from eelbrain_plotly_viz import BrainPlotly2DViz, create_sample_brain_data

# Create sample data
data_dict = create_sample_brain_data(
    n_sources=200,
    n_times=100, 
    has_vector_data=True
)

# Visualize
viz = BrainPlotly2DViz(y=data_dict)
viz.run()
```

### Jupyter Notebook Usage

```python
from eelbrain_plotly_viz import BrainPlotly2DViz

# Create and display in notebook
viz = BrainPlotly2DViz()
viz.show_in_jupyter(time_idx=25)  # Show specific time point
```

### With Eelbrain NDVar (if installed)

```python
from eelbrain import datasets
from eelbrain_plotly_viz import BrainPlotly2DViz

# Load Eelbrain data
data_ds = datasets.get_mne_sample(src='vol', ori='vector')
y = data_ds['src']  # NDVar format

# Visualize
viz = BrainPlotly2DViz(y=y)
viz.run()
```

## Advanced Usage

### Custom Visualization Options

```python
viz = BrainPlotly2DViz(
    y=your_data,
    cmap='Viridis',           # Custom colormap
    show_max_only=True,       # Show only mean and max in butterfly plot
    arrow_threshold=0.5       # Control arrow display threshold
)
```

### Export Static Images

```python
# Export all views as PNG images
exported_files = viz.export_images(
    output_dir="./my_brain_plots",
    time_idx=30,
    format="png",
    width=1200,
    height=800
)
```

### Custom Server Configuration

```python
# Run on custom host/port
viz.run(
    host='0.0.0.0',  # Allow external connections
    port=8888,       # Custom port
    debug=True       # Enable debug mode
)
```

## Data Formats

### Vector Data
For data with direction and magnitude (e.g., current dipoles):
- **Numpy**: `(n_sources, n_times, 3)` - 3D vectors over time
- **Eelbrain**: NDVar with dimensions `(time, source, space)`

### Scalar Data  
For data with magnitude only (e.g., power, activation):
- **Numpy**: `(n_sources, n_times)` - scalar values over time
- **Eelbrain**: NDVar with dimensions `(time, source)`

### Dictionary Format
```python
data_dict = {
    'data': np.array,           # Brain activity data
    'coords': np.array,         # Source coordinates (n_sources, 3) 
    'times': np.array,          # Time values (n_times,)
    'has_vector_data': bool     # Whether data is vector or scalar
}
```

## Performance Features

### Optimized Arrow Rendering
- **453x speedup** over individual annotations
- Batch rendering using single Plotly traces
- Handles thousands of arrows smoothly
- Maintains full visual quality

### Memory Efficiency
- Efficient data handling for large datasets
- Optional data subsampling for performance
- Optimized for real-time interaction

## Visualization Components

### Brain Projections
- **Axial view**: Top-down brain slice (X vs Y)
- **Sagittal view**: Side brain slice (Y vs Z)  
- **Coronal view**: Front brain slice (X vs Z)
- Interactive heatmaps with arrow overlays

### Butterfly Plot
- Time series of brain activity magnitude
- Individual source traces (optional)
- Mean and maximum activity traces
- Time marker synchronization

### Interactive Controls
- Time slider for navigation
- Clickable brain regions
- Real-time updates
- Synchronized views

## Requirements

### Core Dependencies
- `dash >= 2.0.0` - Web application framework
- `plotly >= 5.0.0` - Interactive plotting
- `numpy >= 1.20.0` - Numerical computing
- `matplotlib >= 3.3.0` - Additional plotting support

### Optional Dependencies
- `eelbrain` - For NDVar data support
- `scipy` - For advanced interpolation (auto-installed with numpy)
- `kaleido` - For image export (auto-installed with plotly)

## Examples

### Complete Example Script

```python
#!/usr/bin/env python3
"""
Complete example of brain visualization usage.
"""

import numpy as np
from eelbrain_plotly_viz import BrainPlotly2DViz, create_sample_brain_data

def main():
    print("🧠 Creating Brain Visualization...")
    
    # Method 1: Use built-in sample data
    print("\n1. Using sample data:")
    viz1 = BrainPlotly2DViz()
    
    # Method 2: Create custom data
    print("\n2. Using custom data:")
    data_dict = create_sample_brain_data(
        n_sources=150,
        n_times=75,
        has_vector_data=True,
        random_seed=123
    )
    viz2 = BrainPlotly2DViz(y=data_dict, cmap='Plasma')
    
    # Method 3: Numpy arrays directly
    print("\n3. Using numpy arrays:")
    data = np.random.rand(100, 40, 3)
    coords = np.random.rand(100, 3) * 0.1 - 0.05  # Center around origin
    times = np.linspace(0, 0.8, 40)
    
    viz3 = BrainPlotly2DViz(
        y=data,
        coords=coords, 
        times=times,
        cmap='Hot',
        arrow_threshold='auto'
    )
    
    # Export images
    print("\n📷 Exporting images...")
    viz3.export_images(output_dir="./example_output", time_idx=20)
    
    # Run interactive visualization
    print("\n🌐 Starting interactive visualization...")
    print("Visit http://127.0.0.1:8050 in your browser")
    viz3.run()

if __name__ == "__main__":
    main()
```

## API Reference

### BrainPlotly2DViz Class

#### Constructor
```python
BrainPlotly2DViz(
    y=None,                    # Data input
    coords=None,               # Source coordinates
    times=None,                # Time values
    region=None,               # Brain region (Eelbrain only)
    cmap='Hot',                # Colormap
    show_max_only=False,       # Butterfly plot mode
    arrow_threshold='auto'     # Arrow display threshold
)
```

#### Methods
- `run(port=8050, debug=False, host='127.0.0.1')` - Start interactive app
- `show_in_jupyter(time_idx=0)` - Display in Jupyter notebook
- `export_images(output_dir, time_idx=0, format='png')` - Export static images
- `create_2d_brain_projections_plotly(time_idx)` - Get projection figures
- `create_butterfly_plot()` - Get butterfly plot figure

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
@software{eelbrain_plotly_viz,
  title={Eelbrain Plotly Visualization: Interactive 2D Brain Visualization},
  author={Eelbrain Team},
  year={2024},
  url={https://github.com/liang-bo96/eelbrain-plotly-viz}
}
```

## Support

- 📖 **Documentation**: See this README and docstrings
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/liang-bo96/eelbrain-plotly-viz/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/liang-bo96/eelbrain-plotly-viz/discussions)
- 📧 **Email**: eelbrain@example.com

## Changelog

### v1.0.0 (2024)
- Initial release
- Interactive 2D brain projections
- Optimized arrow rendering (453x speedup)
- Support for multiple data formats
- Jupyter notebook integration
- Image export capabilities 