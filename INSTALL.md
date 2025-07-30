# Installation Guide

This guide shows how to install and use the `eelbrain-plotly-viz` package following Python packaging best practices.

## Quick Installation from GitHub

### Basic Installation

```bash
# Install directly from GitHub
pip install git+https://github.com/liang-bo96/eelbrain-plotly-viz.git
```

### With Optional Dependencies

```bash
# Install with Eelbrain support
pip install "git+https://github.com/liang-bo96/eelbrain-plotly-viz.git[eelbrain]"

# Install with development tools
pip install "git+https://github.com/liang-bo96/eelbrain-plotly-viz.git[dev]"

# Install everything
pip install "git+https://github.com/liang-bo96/eelbrain-plotly-viz.git[all,dev]"
```

## Development Installation

### Clone and Install

```bash
# Clone the repository
git clone https://github.com/liang-bo96/eelbrain-plotly-viz.git
cd eelbrain-plotly-viz

# Install in development mode
pip install -e .

# Or with optional dependencies
pip install -e ".[dev,eelbrain]"
```

### Building from Source

```bash
# Make sure you have the latest build tools
python -m pip install --upgrade pip build

# Build the package
python -m build

# This creates files in dist/:
# - eelbrain_plotly_viz-1.0.0.tar.gz (source distribution)
# - eelbrain_plotly_viz-1.0.0-py3-none-any.whl (wheel)
```

### Installing Built Package

```bash
# Install from wheel
pip install dist/eelbrain_plotly_viz-1.0.0-py3-none-any.whl

# Or install from source distribution
pip install dist/eelbrain_plotly_viz-1.0.0.tar.gz
```

## Testing Installation

### Quick Test

```python
# Test that the package imports correctly
python -c "import eelbrain_plotly_viz; print('✅ Package imported successfully!')"

# Test basic functionality
python -c "
from eelbrain_plotly_viz import BrainPlotly2DViz, create_sample_brain_data
viz = BrainPlotly2DViz()
print(f'✅ Created visualization with {viz.glass_brain_data.shape[0]} sources')
"
```

### Run Example Script

```bash
# Run the included example
python example.py
```

### Run Tests

```bash
# Install test dependencies
pip install pytest

# Run tests
pytest tests/

# Run tests with coverage
pip install pytest-cov
pytest tests/ --cov=eelbrain_plotly_viz
```

## Virtual Environment Setup

### Using venv

```bash
# Create virtual environment
python -m venv eelbrain_viz_env

# Activate (Linux/Mac)
source eelbrain_viz_env/bin/activate

# Activate (Windows)
eelbrain_viz_env\Scripts\activate

# Install package
pip install git+https://github.com/liang-bo96/eelbrain-plotly-viz.git

# Deactivate when done
deactivate
```

### Using conda

```bash
# Create conda environment
conda create -n eelbrain_viz python=3.11

# Activate
conda activate eelbrain_viz

# Install package
pip install git+https://github.com/liang-bo96/eelbrain-plotly-viz.git

# Deactivate when done
conda deactivate
```

## Usage Examples

### Basic Usage

```python
from eelbrain_plotly_viz import BrainPlotly2DViz

# Create visualization with sample data
viz = BrainPlotly2DViz()

# Run interactive web application
viz.run()  # Opens at http://127.0.0.1:8050
```

### With Your Data

```python
import numpy as np
from eelbrain_plotly_viz import BrainPlotly2DViz

# Your brain data (sources, times, xyz)
data = np.random.rand(100, 50, 3)
coords = np.random.rand(100, 3) * 0.1 - 0.05  # Brain coordinates
times = np.linspace(0, 1, 50)  # Time values

# Create visualization
viz = BrainPlotly2DViz(y=data, coords=coords, times=times)
viz.run()
```

### Export Images

```python
# Export static images
viz.export_images(
    output_dir="./my_brain_plots",
    time_idx=25,
    format="png"
)
```

### Jupyter Notebook

```python
# Display in Jupyter notebook
viz.show_in_jupyter(time_idx=30)
```

## Requirements

### Core Dependencies (automatically installed)

- `dash >= 2.0.0` - Web application framework
- `plotly >= 5.0.0` - Interactive plotting
- `numpy >= 1.20.0` - Numerical computing
- `matplotlib >= 3.3.0` - Additional plotting support
- `scipy >= 1.7.0` - Scientific computing

### Optional Dependencies

- `eelbrain` - For NDVar data support (install with `[eelbrain]`)
- `pytest` - For running tests (install with `[dev]`)

## Troubleshooting

### Common Installation Issues

1. **ImportError: No module named 'eelbrain_plotly_viz'**
   ```bash
   # Make sure package is installed
   pip list | grep eelbrain-plotly-viz
   
   # Reinstall if needed
   pip uninstall eelbrain-plotly-viz
   pip install git+https://github.com/liang-bo96/eelbrain-plotly-viz.git
   ```

2. **Missing dependencies**
   ```bash
   # Install all optional dependencies
   pip install "git+https://github.com/liang-bo96/eelbrain-plotly-viz.git[all]"
   ```

3. **Permission errors**
   ```bash
   # Use --user flag
   pip install --user git+https://github.com/liang-bo96/eelbrain-plotly-viz.git
   ```

4. **Build errors**
   ```bash
   # Update build tools
   python -m pip install --upgrade pip setuptools wheel build
   ```

### Getting Help

If you encounter issues:

1. Check the [GitHub Issues](https://github.com/liang-bo96/eelbrain-plotly-viz/issues)
2. Read the [README.md](README.md) for usage examples
3. Run the example script: `python example.py`
4. Check your Python version: `python --version` (requires Python 3.8+)

## Uninstalling

```bash
# Uninstall the package
pip uninstall eelbrain-plotly-viz
```

## Package Information

```bash
# Show package information
pip show eelbrain-plotly-viz

# List installed files
pip show -f eelbrain-plotly-viz
```

## Publishing to PyPI (for maintainers)

### Test PyPI

```bash
# Install twine
pip install twine

# Upload to Test PyPI
python -m twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ eelbrain-plotly-viz
```

### Production PyPI

```bash
# Upload to production PyPI
python -m twine upload dist/*

# Install from PyPI
pip install eelbrain-plotly-viz
``` 