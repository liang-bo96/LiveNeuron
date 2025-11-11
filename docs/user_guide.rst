User Guide
==========

This comprehensive guide covers all features and configuration options of LiveNeuron.

Understanding Display Modes
----------------------------

Display modes control which anatomical views are shown and in what order.

Anatomical Axes
^^^^^^^^^^^^^^^

* **X-axis (Sagittal)**: Left-right view through the brain
* **Y-axis (Coronal)**: Front-back view through the brain
* **Z-axis (Axial)**: Top-bottom view through the brain
* **L**: Left hemisphere lateral view
* **R**: Right hemisphere lateral view

Display Mode Syntax
^^^^^^^^^^^^^^^^^^^

Combine letters to create custom view layouts:

* Single letters: ``"l"``, ``"r"``, ``"x"``, ``"y"``, ``"z"``
* Multiple views: ``"lr"`` (left + right), ``"xyz"`` (three orthogonal views)
* Special mode: ``"ortho"`` (equivalent to ``"xyz"``)
* Four-view modes: ``"lyrz"``, ``"lzry"``, etc.

View Order
^^^^^^^^^^

The order of letters determines the display order from left to right (horizontal layout) or top to bottom (vertical layout).

Examples:

* ``"lyr"`` → Left, Y-axis, Right
* ``"lzr"`` → Left, Z-axis, Right
* ``"yx"`` → Y-axis, X-axis

Layout Modes
------------

Vertical Layout
^^^^^^^^^^^^^^^

**When to use:** Default mode, good for standard displays.

**Characteristics:**

* Butterfly plot on top
* Brain views stacked vertically below
* Colorbar positioned horizontally below brain views

.. code-block:: python

   viz = EelbrainPlotly2DViz(
       display_mode="lyr",
       layout_mode="vertical"
   )

Horizontal Layout
^^^^^^^^^^^^^^^^^

**When to use:** Wide screens, presentations, or when you want more horizontal space for brain views.

**Characteristics:**

* Butterfly plot on the left
* Brain views arranged horizontally to the right
* Colorbar positioned horizontally below brain views
* Optimized space allocation for multiple views

.. code-block:: python

   viz = EelbrainPlotly2DViz(
       display_mode="lyr",
       layout_mode="horizontal"
   )

Arrow Visualization
-------------------

Understanding Arrows
^^^^^^^^^^^^^^^^^^^^

Arrows represent vector fields in the brain data, showing both magnitude and direction of neural activity.

Arrow Scale
^^^^^^^^^^^

The ``arrow_scale`` parameter controls arrow length relative to the default:

* **Default (1.0)**: Balanced for most datasets
* **< 1.0**: Shorter arrows, useful for dense vector fields
* **> 1.0**: Longer arrows, useful for sparse or small-magnitude fields

.. code-block:: python

   # For very dense data, use shorter arrows
   viz = EelbrainPlotly2DViz(arrow_scale=0.5)
   
   # For sparse data, use longer arrows
   viz = EelbrainPlotly2DViz(arrow_scale=1.5)

Arrow Threshold
^^^^^^^^^^^^^^^

The ``arrow_threshold`` parameter filters arrows based on magnitude:

* **0.0**: Show all arrows (default)
* **> 0.0**: Only show arrows with magnitude above threshold
* Helps reduce visual clutter and focus on significant activity

.. code-block:: python

   # Show only significant arrows
   viz = EelbrainPlotly2DViz(
       arrow_threshold=0.2,  # Only show if magnitude > 0.2
       arrow_scale=1.0
   )

Performance Considerations
^^^^^^^^^^^^^^^^^^^^^^^^^^

For large datasets with many vectors:

1. Increase ``arrow_threshold`` to reduce arrow count
2. Decrease ``arrow_scale`` to reduce visual overlap
3. Use appropriate display mode to focus on regions of interest

Color Mapping
-------------

Colormaps
^^^^^^^^^

LiveNeuron uses Plotly colormaps. Common options:

* **Sequential**: ``"Reds"``, ``"Blues"``, ``"Greens"``, ``"Viridis"``, ``"Plasma"``
* **Diverging**: ``"RdBu"``, ``"RdYlBu"``, ``"Spectral"``
* **Perceptually Uniform**: ``"Viridis"``, ``"Plasma"``, ``"Inferno"``

.. code-block:: python

   viz = EelbrainPlotly2DViz(cmap="Viridis")

Color Range
^^^^^^^^^^^

Colors are automatically scaled to the data range:

* Heatmap shows activity magnitude
* Unified colorbar provides reference
* Consistent scaling across all views and time points

Interactive Features
--------------------

Hover Information
^^^^^^^^^^^^^^^^^

**Brain Plots:**

* Hover shows activity value at each voxel
* Semi-transparent popup to minimize occlusion
* Only heatmap hover is shown (arrow hover disabled for clarity)

**Butterfly Plot:**

* Hover shows max and min activity at each time point
* Unified hover mode shows vertical line across all traces

Time Navigation
^^^^^^^^^^^^^^^

**Precise Click Detection:**

* Click anywhere on the butterfly plot's x-axis
* Brain views update to show activity at that exact time
* Implemented with ``spikesnap="cursor"`` for accurate time selection

**Visual Feedback:**

* Spike line indicates current time position
* Smooth updates when clicking different time points

Zoom and Pan
^^^^^^^^^^^^

**Mouse Controls:**

* **Wheel**: Zoom in/out
* **Click + Drag**: Pan the view
* **Double-click**: Reset to original view
* Works independently for butterfly and brain plots

**Axis Locking:**

* Brain plots maintain aspect ratio during zoom
* Prevents distortion of anatomical features

Data Handling
-------------

Input Data Format
^^^^^^^^^^^^^^^^^

LiveNeuron expects data with:

* **Spatial coordinates**: 3D positions (X, Y, Z)
* **Time series**: Activity values over time
* **Optional vectors**: Direction and magnitude for arrow visualization

Sample Data
^^^^^^^^^^^

Use built-in sample data for testing:

.. code-block:: python

   from eelbrain_plotly_viz.sample_data import create_sample_brain_data
   
   data = create_sample_brain_data()

Performance Optimization
------------------------

Smart Binning
^^^^^^^^^^^^^

* Automatically bins 3D data to 2D projection grid
* Reduces rendering overhead for dense datasets
* Configurable bin size (default: 200x200)

Deduplication
^^^^^^^^^^^^^

* When multiple 3D sources project to same 2D position
* Selects source with maximum activity for display
* Ensures consistency between heatmap and arrows

Update Optimization
^^^^^^^^^^^^^^^^^^^

* Incremental updates when clicking butterfly plot
* Only redraws brain views, butterfly stays static
* Minimizes computational overhead

Best Practices
--------------

For Large Datasets
^^^^^^^^^^^^^^^^^^

1. Use horizontal layout for better space utilization
2. Increase ``arrow_threshold`` to reduce arrow density
3. Choose focused display modes (e.g., ``"lr"`` instead of ``"lyrz"``)
4. Consider downsampling time series if not needed

For Presentations
^^^^^^^^^^^^^^^^^

1. Use horizontal layout for better visibility
2. Adjust ``arrow_scale`` for clear arrow visualization
3. Choose high-contrast colormaps (e.g., ``"Reds"``, ``"Blues"``)
4. Use browser mode (``show()``) for full-screen capability

For Publications
^^^^^^^^^^^^^^^^

1. Use consistent display modes across figures
2. Document ``arrow_scale`` and ``arrow_threshold`` values
3. Export specific time points as needed
4. Consider vertical layout for traditional figure orientation

Troubleshooting
---------------

Brain Plots Different Sizes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If brain plots appear inconsistent:

* Ensure you're using the latest version
* Try refreshing the browser
* Check that display mode is valid

Slow Performance
^^^^^^^^^^^^^^^^

If visualization is slow:

* Increase ``arrow_threshold`` to reduce arrows
* Use simpler display modes
* Consider downsampling time series
* Check system memory availability

Arrow Display Issues
^^^^^^^^^^^^^^^^^^^^

If arrows are not visible or look wrong:

* Adjust ``arrow_scale`` (try values between 0.5 and 2.0)
* Check ``arrow_threshold`` (lower to see more arrows)
* Verify input data has vector components

Time Click Not Working
^^^^^^^^^^^^^^^^^^^^^^

If clicking butterfly plot doesn't update views:

* Ensure you're clicking within the plot area
* Try clicking directly on the time axis
* Refresh the browser if issue persists

