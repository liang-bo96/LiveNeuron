Quick Start Guide
=================

This guide will help you get started with LiveNeuron quickly.

Basic Visualization
-------------------

Creating a Simple Visualization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Create visualization with built-in MNE sample data
   viz = EelbrainPlotly2DViz()
   
   # Launch in browser (uses random port)
   viz.run()

The server will start on a random port. Check the console output for the exact URL.

Using Custom Options
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Customize visualization
   viz = EelbrainPlotly2DViz(
       y=None,                    # Use built-in sample data
       region=None,               # Use full brain
       cmap='Hot',                # Colormap (default: 'YlOrRd')
       show_max_only=True,        # Show only mean and max in butterfly plot
       arrow_threshold='auto'     # Auto threshold for arrows
   )
   
   viz.run()

Display Modes
-------------

LiveNeuron supports multiple anatomical view configurations:

Basic Views
^^^^^^^^^^^

.. code-block:: python

   # Orthogonal views (sagittal + coronal + axial)
   viz = EelbrainPlotly2DViz(display_mode="ortho")
   
   # Sagittal view only (X-axis)
   viz = EelbrainPlotly2DViz(display_mode="x")
   
   # Coronal view only (Y-axis)
   viz = EelbrainPlotly2DViz(display_mode="y")
   
   # Axial view only (Z-axis)
   viz = EelbrainPlotly2DViz(display_mode="z")

Hemisphere Views
^^^^^^^^^^^^^^^^

.. code-block:: python

   # Left hemisphere only
   viz = EelbrainPlotly2DViz(display_mode="l")
   
   # Right hemisphere only
   viz = EelbrainPlotly2DViz(display_mode="r")
   
   # Both hemispheres (left + right)
   viz = EelbrainPlotly2DViz(display_mode="lr")
   
   # Left + Coronal + Right (default, best for comparison)
   viz = EelbrainPlotly2DViz(display_mode="lyr")

Multi-View Modes
^^^^^^^^^^^^^^^^

.. code-block:: python

   # Left + Axial + Right
   viz = EelbrainPlotly2DViz(display_mode="lzr")
   
   # Four views: Left + Coronal + Right + Axial
   viz = EelbrainPlotly2DViz(display_mode="lyrz")
   
   # Four views: Left + Axial + Right + Coronal
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
   viz.run()

Horizontal Layout
^^^^^^^^^^^^^^^^^

Better for wide screens:

.. code-block:: python

   viz = EelbrainPlotly2DViz(
       display_mode="lyr",
       layout_mode="horizontal"
   )
   viz.run()

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

Filtering Arrows by Magnitude
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Show all arrows
   viz = EelbrainPlotly2DViz(arrow_threshold=None)
   
   # Auto threshold (10% of max magnitude)
   viz = EelbrainPlotly2DViz(arrow_threshold='auto')
   
   # Custom threshold
   viz = EelbrainPlotly2DViz(arrow_threshold=0.1)

Customizing Colors
------------------

.. code-block:: python

   # Use different built-in colormaps
   viz = EelbrainPlotly2DViz(cmap='Hot')        # Hot (red/yellow)
   viz = EelbrainPlotly2DViz(cmap='YlOrRd')     # Yellow-Orange-Red (default)
   viz = EelbrainPlotly2DViz(cmap='Viridis')    # Viridis (perceptually uniform)
   viz = EelbrainPlotly2DViz(cmap='OrRd')       # Orange-Red

   # Custom colormap
   custom_cmap = [
       [0, 'rgba(255,255,0,0.5)'],    # Yellow with 50% transparency
       [0.5, 'rgba(255,165,0,0.8)'],  # Orange with 80% transparency
       [1, 'rgba(255,0,0,1.0)']       # Red with full opacity
   ]
   viz = EelbrainPlotly2DViz(cmap=custom_cmap)

Using in Jupyter Notebook
--------------------------

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Create visualization
   viz = EelbrainPlotly2DViz(
       display_mode="lyr",
       layout_mode="horizontal"
   )
   
   # Display inline in notebook (embedded) - auto size
   viz.run()
   
   # Or open in JupyterLab tab
   viz.run(mode='jupyterlab')
   
   # Or open in external browser (default outside Jupyter)
   viz.run(mode='external')

Working with Eelbrain Data
---------------------------

.. code-block:: python

   from eelbrain import datasets
   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Load Eelbrain NDVar data
   data_ds = datasets.get_mne_sample(src='vol', ori='vector')
   y = data_ds['src']  # NDVar format
   
   # Visualize
   viz = EelbrainPlotly2DViz(y=y, cmap='Hot')
   viz.run()

Using Brain Region Filtering
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Apply parcellation to filter specific brain regions
   viz = EelbrainPlotly2DViz(
       y=None,                 # Built-in sample data
       region='aparc+aseg',    # Apply aparc+aseg parcellation
       cmap='Viridis'
   )
   viz.run()

Exporting Images
----------------

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Create visualization
   viz = EelbrainPlotly2DViz(display_mode="lyr")
   
   # Export all views as PNG
   result = viz.export_images(
       output_dir="./my_brain_plots",
       time_idx=30,
       format="png"
   )
   
   if result["status"] == "success":
       print("Exported files:")
       for plot_type, filepath in result["files"].items():
           print(f"  {plot_type}: {filepath}")

Custom Server Configuration
----------------------------

.. code-block:: python

   # Run on custom port
   viz.run(port=8888)  # Enable debug=True only when troubleshooting
   
   # Run on random port (default)
   viz.run()  # Check console for URL

Interactive Features
--------------------

Once running, you can:

* **Hover** over brain plots to see activity values
* **Hover** over butterfly plot to see max/min activity at each time point
* **Click** on butterfly plot to navigate to specific time points
* **Zoom and pan** on all plots using mouse controls
* **Double-click** to reset zoom

Next Steps
----------

* Read the :doc:`user_guide` for detailed information
* Check :doc:`examples` for more use cases
* Explore the :doc:`api_reference` for all available options
