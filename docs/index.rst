Welcome to LiveNeuron's documentation!
======================================

**LiveNeuron** is an interactive 2D brain visualization library using Plotly and Dash, designed for real-time exploration of neural activity data.

.. image:: https://img.shields.io/badge/python-3.8%2B-blue
   :target: https://www.python.org/downloads/
   :alt: Python Version

.. image:: https://img.shields.io/badge/license-MIT-green
   :target: https://opensource.org/licenses/MIT
   :alt: License

Key Features
------------

* **Interactive 2D brain projections** - axial, sagittal, coronal, and hemisphere views
* **Butterfly plots** for time series visualization
* **453x faster arrow rendering** using optimized batch techniques
* **Real-time controls** for time navigation and interaction
* **Flexible data input** - supports Eelbrain NDVar, numpy arrays, and built-in MNE sample data
* **Jupyter notebook support** for interactive development
* **Customizable colormaps** and visualization options
* **Export capabilities** for static images

Quick Start
-----------

Installation
^^^^^^^^^^^^

**Method 1: Install from GitHub**

.. code-block:: bash

   pip install https://github.com/liang-bo96/LiveNeuron/archive/refs/heads/main.zip

**Method 2: Download and Install from ZIP**

.. code-block:: bash

   # Download the ZIP file
   wget https://github.com/liang-bo96/LiveNeuron/archive/refs/heads/main.zip
   
   # Or download manually from:
   # https://github.com/liang-bo96/LiveNeuron/archive/refs/heads/main.zip
   
   # Unzip the file
   unzip main.zip
   
   # Navigate to the directory
   cd LiveNeuron-main
   
   # Install the package
   pip install .

Basic Usage
^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Create visualization with built-in sample data
   viz = EelbrainPlotly2DViz()
   
   # Launch in interactive plot
   viz.run()

# Or use in Jupyter (inline mode)
viz.run(mode='inline', width=1200, height=900)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   user_guide
   api_reference
   examples
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

