API Reference
=============

This page contains the complete API reference for LiveNeuron.

Main Class
----------

.. autoclass:: eelbrain_plotly_viz.viz_2d.EelbrainPlotly2DViz
   :members: run, export_images
   :exclude-members: __init__
   :show-inheritance:
   
   The main visualization class for interactive 2D brain projections with butterfly plots.

Constructor
-----------

EelbrainPlotly2DViz
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   EelbrainPlotly2DViz(
       y=None,
       region=None,
       cmap='YlOrRd',
       show_max_only=False,
       arrow_threshold=None,
       arrow_scale=1.0,
       realtime=False,
       layout_mode='vertical',
       display_mode='lyr'
   )

**Parameters:**

* **y** (*NDVar or None*, default=None)
  
  Data to plot with dimensions ``([case,] time, source[, space])``.
  
  * If ``y`` has a case dimension, the mean is plotted
  * If ``y`` has a space dimension, the norm is plotted
  * If None, uses MNE sample data for demonstration
  
* **region** (*str or None*, default=None)
  
  Brain region to load using aparc+aseg parcellation.
  
  * If None, loads all regions
  * Only used when ``y`` is None
  * Examples: ``'aparc+aseg'``, ``'aseg'``
  
* **cmap** (*str or list*, default='YlOrRd')
  
  Plotly colorscale for heatmaps.
  
  * Built-in names: ``'YlOrRd'``, ``'Hot'``, ``'Viridis'``, ``'OrRd'``, ``'Reds'``
  * Custom colorscale: ``[[0, 'white'], [1, 'red']]``
  * See https://plotly.com/python/builtin-colorscales/
  
* **show_max_only** (*bool*, default=False)
  
  If True, butterfly plot shows only mean and max traces.
  If False, shows individual source traces, mean, and max.
  
* **arrow_threshold** (*float, str, or None*, default=None)
  
  Threshold for displaying arrows in brain projections.
  
  * ``None``: Show all arrows
  * ``'auto'``: Use 10% of maximum magnitude as threshold
  * *float*: Custom threshold value
  
* **arrow_scale** (*float*, default=1.0)
  
  Relative scale factor for arrow length in brain projections.
  
  * ``1.0``: Default length (good balance)
  * ``< 1.0``: Shorter arrows (e.g., 0.5 for half length)
  * ``> 1.0``: Longer arrows (e.g., 2.0 for double length)
  * Typical range: 0.5 to 2.0
  
* **realtime** (*bool*, default=False)
  
  If True, enables real-time mode by default.
  Internal parameter for future features.
  
* **layout_mode** (*str*, default='vertical')
  
  Layout arrangement mode. Options:
  
  * ``'vertical'``: Butterfly plot on top, brain views below (default)
  * ``'horizontal'``: Butterfly plot on left, brain views on right
  
* **display_mode** (*str*, default='lyr')
  
  Anatomical view mode for brain projections. Options:
  
  **Single views:**
  
  * ``'x'``: Sagittal view (left-right)
  * ``'y'``: Coronal view (front-back)
  * ``'z'``: Axial view (top-bottom)
  * ``'l'``: Left hemisphere view
  * ``'r'``: Right hemisphere view
  
  **Multi views:**
  
  * ``'ortho'``: Orthogonal views (x + y + z)
  * ``'lr'``: Both hemispheres (left + right)
  * ``'lyr'``: Left + Coronal + Right (default, best for comparison)
  * ``'lzr'``: Left + Axial + Right
  * ``'xz'``: Sagittal + Axial
  * ``'yx'``: Coronal + Sagittal
  * ``'yz'``: Coronal + Axial
  
  **Four-view modes:**
  
  * ``'lyrz'``: Left + Coronal + Right + Axial
  * ``'lzry'``: Left + Axial + Right + Coronal

Methods
-------

run()
^^^^^

Start the interactive Dash application.

.. code-block:: python

   viz.run(
       port=None,
       debug=True,
       mode='external',
       width=1200,
       height=900
   )

**Parameters:**

* **port** (*int or None*): Port number for server. If None, uses random port.
* **debug** (*bool*): Enable debug mode (default: True).
* **mode** (*str*): Display mode - ``'external'``, ``'inline'``, or ``'jupyterlab'``.
* **width** (*int*): Display width in pixels (default: 1200).
* **height** (*int*): Display height in pixels (default: 900).

**Returns:**
  None

**Example:**

.. code-block:: python

   # External browser (default)
   viz.run()
   
   # Custom port
   viz.run(port=8888)
   
   # Jupyter inline
   viz.run(mode='inline', width=1200, height=900)

export_images()
^^^^^^^^^^^^^^^

Export current plots as image files.

.. code-block:: python

   viz.export_images(
       output_dir='./images',
       time_idx=None,
       format='png'
   )

**Parameters:**

* **output_dir** (*str*): Directory to save image files (default: "./images").
* **time_idx** (*int or None*): Time index to export. If None, uses 0.
* **format** (*str*): Image format - ``'png'``, ``'jpg'``, ``'svg'``, or ``'pdf'`` (default: 'png').

**Returns:**
  *dict*: Dictionary with keys:
  
  * ``'status'``: ``'success'`` or ``'error'``
  * ``'files'``: Dictionary mapping plot types to file paths
  * ``'message'``: Status message

**Example:**

.. code-block:: python

   result = viz.export_images(
       output_dir="./my_plots",
       time_idx=30,
       format="png"
   )
   
   if result["status"] == "success":
       for plot_type, filepath in result["files"].items():
           print(f"{plot_type}: {filepath}")

Sample Data Module
------------------

create_sample_brain_data()
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generate sample brain data for testing and demonstration.

.. code-block:: python

   from eelbrain_plotly_viz import create_sample_brain_data
   
   data_dict = create_sample_brain_data(
       n_sources=200,
       n_times=50,
       has_vector_data=True,
       random_seed=42
   )

**Parameters:**

* **n_sources** (*int*): Number of brain sources (default: 200).
* **n_times** (*int*): Number of time points (default: 50).
* **has_vector_data** (*bool*): Generate vector data if True (default: True).
* **random_seed** (*int*): Random seed for reproducibility (default: 42).

**Returns:**
  *dict*: Dictionary with keys:
  
  * ``'data'``: Brain activity data array
  * ``'coords'``: Source coordinates
  * ``'times'``: Time values

**Note:** Direct dictionary input is not supported in current implementation. Use built-in MNE sample data or Eelbrain NDVar instead.

Data Format
-----------

Input Data Expectations
^^^^^^^^^^^^^^^^^^^^^^^^

**Vector Data** (with direction and magnitude):

* Eelbrain NDVar with dimensions: ``([case,] time, source, space)``
* MNE sample data: Built-in volumetric source with 3D vectors
* Space dimension: 3D components (X, Y, Z)

**Scalar Data** (magnitude only):

* Eelbrain NDVar with dimensions: ``([case,] time, source)``
* Single value per source at each time point

**Built-in Sample Data:**

* 1589 sources in volumetric source space
* 76 time points (-100ms to 400ms)
* Vector data (3D current dipoles)
* Optional brain region filtering

Exceptions
----------

The library may raise the following exceptions:

**ValueError**
  * Invalid ``display_mode`` string
  * Invalid ``layout_mode`` (not "vertical" or "horizontal")
  * Invalid parameter values

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
       viz.run()
   except RuntimeError as e:
       print(f"Visualization error: {e}")

Type Hints
----------

The library uses Python type hints for better IDE support:

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz
   from typing import Optional
   from eelbrain import NDVar
   
   def create_viz(
       data: Optional[NDVar] = None,
       mode: str = "lyr"
   ) -> EelbrainPlotly2DViz:
       return EelbrainPlotly2DViz(y=data, display_mode=mode)
