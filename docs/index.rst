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

* **Interactive Visualization**: Real-time exploration with hover, click, and zoom
* **Multiple Display Modes**: 17 different anatomical view configurations (ortho, l, r, lr, lyr, lzr, lyrz, etc.)
* **Dual Layout Modes**: Vertical (default) or horizontal layout for different screen sizes
* **Smart Performance**: Optimized rendering with binning and deduplication
* **Customizable Arrows**: Adjustable arrow scale and threshold for vector field visualization
* **Unified Sizing**: Consistent brain plot dimensions across all views
* **Professional UI**: Dark-themed plots with transparent hover labels

Quick Start
-----------

Installation
^^^^^^^^^^^^

.. code-block:: bash

   pip install LiveNeuron

Basic Usage
^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Create visualization with sample data
   viz = EelbrainPlotly2DViz(
       display_mode="lyr",      # Left, Y-axis (coronal), Right views
       layout_mode="horizontal", # Horizontal layout
       arrow_scale=1.0,         # Default arrow length
       arrow_threshold=0.1,     # Filter small arrows
       cmap="Reds"             # Colormap
   )
   
   # Launch in browser
   viz.show()

   # Or use in Jupyter
   viz.show_jupyter()

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

