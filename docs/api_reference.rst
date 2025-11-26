API Reference
=============

This page contains the complete API reference for LiveNeuron.

Main Class
----------

.. autoclass:: eelbrain_plotly_viz.viz_2d.EelbrainPlotly2DViz
   :members: run, export_images
   :exclude-members: __init__
   :show-inheritance:

   The main visualization class for interactive 2D brain projections with activity time-course plots.

Sample Data Module
------------------

.. autofunction:: eelbrain_plotly_viz.sample_data.create_sample_brain_data

**Note:** :func:`create_sample_brain_data` returns a minimal NDVar-like object that can be passed directly as ``y`` to :class:`EelbrainPlotly2DViz`.

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
