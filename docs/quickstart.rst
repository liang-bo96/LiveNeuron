Quick Start Guide
=================

This guide will help you get started with LiveNeuron quickly.

Basic Visualization
-------------------

Creating a Simple Visualization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Create visualization with default settings
   viz = EelbrainPlotly2DViz()
   
   # Launch in browser
   viz.show()

Using Sample Data
^^^^^^^^^^^^^^^^^

LiveNeuron includes sample data for quick testing:

.. code-block:: python

   from eelbrain_plotly_viz.sample_data import create_sample_brain_data

   # Generate sample data
   data = create_sample_brain_data()
   
   # Create visualization
   viz = EelbrainPlotly2DViz()
   viz.show()

Display Modes
-------------

LiveNeuron supports 17 different anatomical view configurations:

Single View Modes
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Left hemisphere only
   viz = EelbrainPlotly2DViz(display_mode="l")
   
   # Right hemisphere only
   viz = EelbrainPlotly2DViz(display_mode="r")
   
   # Sagittal view (X-axis)
   viz = EelbrainPlotly2DViz(display_mode="x")
   
   # Coronal view (Y-axis)
   viz = EelbrainPlotly2DViz(display_mode="y")
   
   # Axial view (Z-axis)
   viz = EelbrainPlotly2DViz(display_mode="z")

Multi-View Modes
^^^^^^^^^^^^^^^^

.. code-block:: python

   # Orthogonal views (sagittal, coronal, axial)
   viz = EelbrainPlotly2DViz(display_mode="ortho")
   
   # Left and right hemispheres
   viz = EelbrainPlotly2DViz(display_mode="lr")
   
   # Left, coronal, right
   viz = EelbrainPlotly2DViz(display_mode="lyr")
   
   # Four views: left, axial, sagittal, right
   viz = EelbrainPlotly2DViz(display_mode="lzry")

Layout Modes
------------

Vertical Layout (Default)
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   viz = EelbrainPlotly2DViz(
       display_mode="lyr",
       layout_mode="vertical"  # Default
   )

Horizontal Layout
^^^^^^^^^^^^^^^^^

Better for wide screens:

.. code-block:: python

   viz = EelbrainPlotly2DViz(
       display_mode="lyr",
       layout_mode="horizontal"
   )

Customizing Arrows
------------------

Adjusting Arrow Length
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Default arrow length
   viz = EelbrainPlotly2DViz(arrow_scale=1.0)
   
   # Shorter arrows (half length)
   viz = EelbrainPlotly2DViz(arrow_scale=0.5)
   
   # Longer arrows (double length)
   viz = EelbrainPlotly2DViz(arrow_scale=2.0)

Filtering Small Arrows
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Show only arrows with magnitude > 0.1
   viz = EelbrainPlotly2DViz(arrow_threshold=0.1)
   
   # Show all arrows
   viz = EelbrainPlotly2DViz(arrow_threshold=0.0)
   
   # Show only strong arrows
   viz = EelbrainPlotly2DViz(arrow_threshold=0.5)

Customizing Colors
------------------

.. code-block:: python

   # Use different colormaps
   viz = EelbrainPlotly2DViz(cmap="Reds")      # Red color scheme
   viz = EelbrainPlotly2DViz(cmap="Blues")     # Blue color scheme
   viz = EelbrainPlotly2DViz(cmap="Viridis")   # Viridis color scheme

Using in Jupyter Notebook
--------------------------

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Create visualization
   viz = EelbrainPlotly2DViz(
       display_mode="lyr",
       layout_mode="horizontal"
   )
   
   # Display in notebook
   viz.show_jupyter()

Interactive Features
--------------------

Hover to Explore
^^^^^^^^^^^^^^^^

* Hover over brain plots to see activity values
* Hover over butterfly plot to see max/min activity

Click to Navigate
^^^^^^^^^^^^^^^^^

* Click on the butterfly plot's time axis to jump to specific time points
* The brain views update automatically to show activity at that time

Zoom and Pan
^^^^^^^^^^^^

* Use mouse wheel to zoom
* Click and drag to pan
* Double-click to reset view

Next Steps
----------

* Read the :doc:`user_guide` for detailed information
* Check :doc:`examples` for more use cases
* Explore the :doc:`api_reference` for all available options

