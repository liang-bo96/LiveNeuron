Examples
========

This page provides practical examples of using LiveNeuron for various visualization tasks.

Basic Examples
--------------

Example 1: Quick Start with Sample Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz
   from eelbrain_plotly_viz.sample_data import create_sample_brain_data

   # Generate sample data
   data = create_sample_brain_data()
   
   # Create basic visualization
   viz = EelbrainPlotly2DViz()
   viz.show()

Example 2: Custom Display Mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Show left and right hemispheres only
   viz = EelbrainPlotly2DViz(display_mode="lr")
   viz.show()

Example 3: Horizontal Layout
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Better for wide screens
   viz = EelbrainPlotly2DViz(
       display_mode="lyr",
       layout_mode="horizontal"
   )
   viz.show()

Advanced Examples
-----------------

Example 4: Custom Arrow Visualization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Fine-tune arrow display
   viz = EelbrainPlotly2DViz(
       display_mode="lyr",
       arrow_scale=1.5,        # 50% longer arrows
       arrow_threshold=0.2,    # Only show significant arrows
       cmap="Viridis"         # Use perceptually uniform colormap
   )
   viz.show()

Example 5: Dense Vector Field Visualization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # For datasets with many small vectors
   viz = EelbrainPlotly2DViz(
       display_mode="ortho",
       arrow_scale=0.7,        # Shorter arrows to reduce overlap
       arrow_threshold=0.3,    # Filter out weak vectors
       cmap="Reds"
   )
   viz.show()

Example 6: Four-View Layout
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Comprehensive view with four perspectives
   viz = EelbrainPlotly2DViz(
       display_mode="lyrz",      # Left, Y-axis, Right, Z-axis
       layout_mode="horizontal", # Better for 4 views
       arrow_scale=1.0,
       cmap="Blues"
   )
   viz.show()

Jupyter Notebook Examples
--------------------------

Example 7: Basic Jupyter Usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Display inline in notebook
   viz = EelbrainPlotly2DViz(
       display_mode="lyr",
       layout_mode="horizontal"
   )
   viz.show_jupyter()

Example 8: Multiple Visualizations in Notebook
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Create multiple visualizations with different modes
   modes = ["l", "r", "lr", "lyr"]
   
   for mode in modes:
       print(f"Display Mode: {mode}")
       viz = EelbrainPlotly2DViz(
           display_mode=mode,
           layout_mode="horizontal"
       )
       viz.show_jupyter()

Research Examples
-----------------

Example 9: Time Series Analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Focus on temporal dynamics
   viz = EelbrainPlotly2DViz(
       display_mode="lr",        # Focus on hemispheres
       layout_mode="vertical",   # Better for time series focus
       arrow_scale=1.2,
       arrow_threshold=0.15,
       cmap="RdBu"              # Diverging colormap for activity changes
   )
   viz.show()
   
   # Users can click on butterfly plot to explore specific time points

Example 10: Spatial Pattern Analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Emphasize spatial patterns
   viz = EelbrainPlotly2DViz(
       display_mode="ortho",     # Three orthogonal views
       layout_mode="horizontal", # Better spatial layout
       arrow_scale=1.0,
       arrow_threshold=0.25,     # Show only strong patterns
       cmap="Viridis"
   )
   viz.show()

Example 11: Comparative Analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Create visualizations for comparison
   conditions = ["baseline", "stimulus", "response"]
   
   for condition in conditions:
       # Load data for each condition
       # data = load_condition_data(condition)
       
       viz = EelbrainPlotly2DViz(
           display_mode="lyr",
           layout_mode="horizontal",
           arrow_scale=1.0,
           cmap="Reds"
       )
       viz.show()  # Each opens in a new browser tab

Customization Examples
----------------------

Example 12: Custom Colormap
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Try different colormaps for different purposes
   colormaps = {
       "activity": "Reds",      # For activity magnitude
       "change": "RdBu",        # For bidirectional changes
       "continuous": "Viridis"  # For continuous data
   }
   
   for purpose, cmap in colormaps.items():
       print(f"{purpose}: {cmap}")
       viz = EelbrainPlotly2DViz(
           display_mode="lyr",
           cmap=cmap
       )
       viz.show_jupyter()

Example 13: Progressive Arrow Filtering
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Compare different threshold levels
   thresholds = [0.0, 0.1, 0.2, 0.3]
   
   for threshold in thresholds:
       print(f"Threshold: {threshold}")
       viz = EelbrainPlotly2DViz(
           display_mode="lr",
           arrow_threshold=threshold,
           arrow_scale=1.0,
           cmap="Reds"
       )
       viz.show_jupyter()

Example 14: All Display Modes Demo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Demonstrate all available display modes
   single_views = ["l", "r", "x", "y", "z"]
   multi_views = ["lr", "lyr", "lzr", "ortho"]
   four_views = ["lyrz", "lzry"]
   
   all_modes = single_views + multi_views + four_views
   
   for mode in all_modes:
       print(f"\nDisplay Mode: {mode}")
       viz = EelbrainPlotly2DViz(
           display_mode=mode,
           layout_mode="horizontal" if len(mode) > 2 else "vertical"
       )
       viz.show_jupyter()

Performance Examples
--------------------

Example 15: Optimized for Large Datasets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Optimize for large, dense datasets
   viz = EelbrainPlotly2DViz(
       display_mode="lr",        # Fewer views = faster
       arrow_threshold=0.4,      # Aggressive filtering
       arrow_scale=0.8,          # Smaller arrows
       bin_size=150,             # Lower resolution
       cmap="Reds"
   )
   viz.show()

Example 16: High-Quality Publication Mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # High quality for publication figures
   viz = EelbrainPlotly2DViz(
       display_mode="lyr",
       layout_mode="horizontal",
       arrow_scale=1.0,
       arrow_threshold=0.1,      # Balanced filtering
       bin_size=250,             # Higher resolution
       cmap="Viridis"           # Perceptually uniform
   )
   viz.show()

Integration Examples
--------------------

Example 17: With Custom Data Processing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import numpy as np
   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Custom data preprocessing
   def preprocess_brain_data(raw_data):
       # Apply custom filtering, normalization, etc.
       processed = raw_data.copy()
       # ... processing steps ...
       return processed
   
   # Load and process data
   # raw_data = load_brain_data()
   # processed_data = preprocess_brain_data(raw_data)
   
   # Visualize
   viz = EelbrainPlotly2DViz(
       display_mode="lyr",
       layout_mode="horizontal"
   )
   viz.show()

Example 18: Batch Processing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz
   import time

   # Process multiple subjects
   subjects = ["sub01", "sub02", "sub03"]
   
   for subject in subjects:
       print(f"Processing {subject}...")
       
       # Load subject data
       # data = load_subject_data(subject)
       
       # Create visualization
       viz = EelbrainPlotly2DViz(
           display_mode="lyr",
           layout_mode="horizontal",
           arrow_scale=1.0,
           cmap="Reds"
       )
       
       # Save or display
       viz.show()
       time.sleep(2)  # Allow time to view

Tips and Tricks
---------------

Tip 1: Finding the Right Arrow Scale
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Start with default (1.0) and adjust based on visual density:

.. code-block:: python

   # If arrows are too crowded or unclear:
   # - Increase arrow_threshold (0.2, 0.3, etc.)
   # - Decrease arrow_scale (0.7, 0.5, etc.)
   
   # If arrows are too sparse or small:
   # - Decrease arrow_threshold (0.05, 0.0, etc.)
   # - Increase arrow_scale (1.5, 2.0, etc.)

Tip 2: Choosing Layout Mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Use vertical layout for:
   # - 1-2 views
   # - Standard aspect ratio displays
   # - Focus on temporal dynamics (butterfly plot prominent)
   
   # Use horizontal layout for:
   # - 3+ views
   # - Wide displays or presentations
   # - Focus on spatial patterns (brain views prominent)

Tip 3: Colormap Selection
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Sequential (for magnitude):
   cmap = "Reds"      # Warm colors
   cmap = "Blues"     # Cool colors
   cmap = "Viridis"   # Perceptually uniform
   
   # Diverging (for changes around zero):
   cmap = "RdBu"      # Red-blue
   cmap = "RdYlBu"    # Red-yellow-blue

Tip 4: Interactive Exploration Workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # 1. Start with overview
   viz = EelbrainPlotly2DViz(display_mode="ortho")
   viz.show()
   
   # 2. Identify regions of interest from butterfly plot
   # 3. Click on specific time points to explore spatial patterns
   # 4. Hover over brain regions to see exact activity values
   # 5. Zoom and pan to focus on specific brain regions

