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

.. code-block:: bash

   # Install from GitHub
   pip install git+https://github.com/liang-bo96/LiveNeuron.git

Basic Usage
^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Create visualization with built-in sample data
   viz = EelbrainPlotly2DViz()
   
   # Launch in browser (random port)
   viz.run()

   # Or use in Jupyter
   viz.show_in_jupyter(width=1200, height=900)

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

