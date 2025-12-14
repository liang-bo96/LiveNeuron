Welcome to LiveNeuro's documentation!
======================================

**LiveNeuro** is an interactive 2D brain visualization library using Plotly and Dash, designed for real-time exploration of neural activity data.

.. image:: liveNeuron.png
   :alt: LiveNeuro visualization overview
   :align: center
   :width: 720px

.. image:: https://img.shields.io/badge/python-3.8%2B-blue
   :target: https://www.python.org/downloads/
   :alt: Python Version

.. image:: https://img.shields.io/badge/license-MIT-green
   :target: https://opensource.org/licenses/MIT
   :alt: License

.. image:: https://img.shields.io/badge/docs-ReadTheDocs-blue
   :target: https://liveneuron.readthedocs.io/en/latest/index.html
   :alt: Documentation

Key Features
------------

* **Interactive 2D brain projections** - axial, sagittal, coronal, and hemisphere views
* **Activity time-course plots** for time series visualization
* **Optimized arrow rendering** for smoother interaction with dense vector fields
* **Real-time controls** for time navigation and interaction
* **Flexible data input** - supports Eelbrain NDVar, numpy arrays, and built-in MNE sample data
* **Jupyter notebook support** for interactive development
* **Customizable colormaps** and visualization options
* **Export capabilities** for static images

Quick Start
-----------

Installation
^^^^^^^^^^^^

**Install from GitHub**

.. code-block:: bash

   pip install https://github.com/liang-bo96/LiveNeuro/archive/refs/heads/main.zip

Basic Usage
^^^^^^^^^^^

.. code-block:: python

   from liveneuro import LiveNeuro

   # Create visualization with built-in sample data
   viz = LiveNeuro()
   
   # Launch in interactive plot
   viz.run()

For a full walkthrough of layouts and controls, start with the :doc:`user_guide`.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   user_guide
   api_reference
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
