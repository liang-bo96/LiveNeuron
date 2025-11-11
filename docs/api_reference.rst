API Reference
=============

This page contains the complete API reference for LiveNeuron.

Main Class
----------

.. autoclass:: eelbrain_plotly_viz.viz_2d.EelbrainPlotly2DViz
   :members:
   :undoc-members:
   :show-inheritance:

Constructor Parameters
----------------------

EelbrainPlotly2DViz
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   EelbrainPlotly2DViz(
       display_mode: str = "ortho",
       layout_mode: str = "vertical",
       arrow_scale: float = 1.0,
       arrow_threshold: float = 0.0,
       cmap: str = "Reds",
       is_jupyter_mode: bool = False,
       bin_size: int = 200
   )

**Parameters:**

* **display_mode** (*str*, default="ortho")
  
  Anatomical view configuration. Options:
  
  * Single views: ``"l"``, ``"r"``, ``"x"``, ``"y"``, ``"z"``
  * Multi views: ``"lr"``, ``"lyr"``, ``"lzr"``, ``"xyz"``, ``"ortho"``
  * Four views: ``"lyrz"``, ``"lzry"``, and all permutations
  
* **layout_mode** (*str*, default="vertical")
  
  Layout orientation:
  
  * ``"vertical"``: Butterfly on top, brain views below
  * ``"horizontal"``: Butterfly on left, brain views on right
  
* **arrow_scale** (*float*, default=1.0)
  
  Relative scale factor for arrow length. 
  
  * ``1.0`` = default length
  * ``< 1.0`` = shorter arrows
  * ``> 1.0`` = longer arrows
  * Typical range: 0.5 to 2.0
  
* **arrow_threshold** (*float*, default=0.0)
  
  Minimum vector magnitude to display arrows.
  
  * ``0.0`` = show all arrows
  * ``> 0.0`` = only show arrows with magnitude above threshold
  * Useful for reducing visual clutter in dense vector fields
  
* **cmap** (*str*, default="Reds")
  
  Plotly colormap name for heatmap visualization.
  
  * Sequential: ``"Reds"``, ``"Blues"``, ``"Greens"``, ``"Viridis"``
  * Diverging: ``"RdBu"``, ``"RdYlBu"``, ``"Spectral"``
  
* **is_jupyter_mode** (*bool*, default=False)
  
  Internal flag for Jupyter notebook mode. 
  Automatically set by ``show_jupyter()`` method.
  
* **bin_size** (*int*, default=200)
  
  Resolution of 2D projection grid (pixels).
  
  * Higher values = more detail but slower rendering
  * Lower values = faster but less detail
  * Typical range: 100 to 300

Methods
-------

show()
^^^^^^

Launch the visualization in a web browser using Dash server.

.. code-block:: python

   viz.show()

**Returns:**
  None

**Notes:**
  * Opens browser automatically
  * Runs local Dash server on http://127.0.0.1:8050
  * Press Ctrl+C to stop server

show_jupyter()
^^^^^^^^^^^^^^

Display the visualization inline in a Jupyter notebook.

.. code-block:: python

   viz.show_jupyter()

**Returns:**
  JupyterDash display object

**Notes:**
  * Automatically sets ``is_jupyter_mode=True``
  * Adjusts layout for notebook display
  * Interactive features work the same as browser mode

Private Methods
---------------

These methods are used internally and not typically called directly.

_parse_display_mode()
^^^^^^^^^^^^^^^^^^^^^

Parse display mode string into list of views.

_calculate_view_ranges()
^^^^^^^^^^^^^^^^^^^^^^^^^

Calculate fixed axis ranges for consistent view sizing.

_unify_view_sizes_for_jupyter()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ensure all brain plots have consistent dimensions.

_create_plotly_butterfly()
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create the butterfly plot showing activity over time.

_create_plotly_brain_projection()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create 2D brain projection heatmap with optional arrows.

_create_quiver_arrows()
^^^^^^^^^^^^^^^^^^^^^^^^

Create vector field arrows using Plotly's figure factory.

_create_batch_arrows()
^^^^^^^^^^^^^^^^^^^^^^^

Create arrow annotations for fallback rendering.

_create_horizontal_colorbar()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create standalone horizontal colorbar figure.

_generate_initial_plots()
^^^^^^^^^^^^^^^^^^^^^^^^^^

Generate initial brain plots for all views.

Sample Data Module
------------------

.. automodule:: eelbrain_plotly_viz.sample_data
   :members:
   :undoc-members:
   :show-inheritance:

create_sample_brain_data()
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generate sample brain data for testing and demonstration.

.. code-block:: python

   from eelbrain_plotly_viz.sample_data import create_sample_brain_data
   
   data = create_sample_brain_data()

**Returns:**
  * Sample brain data object compatible with EelbrainPlotly2DViz

**Notes:**
  * Generates synthetic data with realistic spatial and temporal patterns
  * Includes both scalar activity and vector field data
  * Useful for testing and learning the library

Type Hints
----------

The library uses Python type hints for better IDE support and code quality.

Example with type hints:

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz
   from typing import Optional
   
   def create_visualization(
       mode: str = "ortho",
       layout: str = "vertical",
       scale: float = 1.0
   ) -> EelbrainPlotly2DViz:
       """Create a new visualization with specified parameters."""
       return EelbrainPlotly2DViz(
           display_mode=mode,
           layout_mode=layout,
           arrow_scale=scale
       )

Exceptions
----------

The library may raise the following exceptions:

**ValueError**
  * Invalid display_mode string
  * Invalid layout_mode (not "vertical" or "horizontal")
  * Invalid parameter ranges (e.g., negative arrow_scale)

**ImportError**
  * Missing required dependencies
  * Eelbrain not installed when using eelbrain-specific features

**RuntimeError**
  * Data processing errors
  * Visualization rendering errors

Example error handling:

.. code-block:: python

   try:
       viz = EelbrainPlotly2DViz(display_mode="invalid")
   except ValueError as e:
       print(f"Invalid display mode: {e}")
   
   try:
       viz.show()
   except RuntimeError as e:
       print(f"Visualization error: {e}")

