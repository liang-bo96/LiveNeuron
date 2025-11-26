Examples
========

This page provides practical, working examples based on the actual LiveNeuron API.

Basic Examples
--------------

Example 1: Quick Start with Sample Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Create basic visualization with built-in MNE sample data
   viz = EelbrainPlotly2DViz()
   
   # Run interactive dashboard (random port)
   viz.run()  # Check console output for the URL

Example 2: Custom Display Mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Show left hemisphere, coronal view, and right hemisphere
   viz = EelbrainPlotly2DViz(display_mode="lyr")
   viz.run()

Example 3: Horizontal Layout
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Better for wide screens
   viz = EelbrainPlotly2DViz(
       display_mode="lyr",
       layout_mode="horizontal"
   )
   viz.run()

Advanced Examples
-----------------

Example 4: Custom Arrow Visualization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Fine-tune arrow display
   viz = EelbrainPlotly2DViz(
       display_mode="lyr",
       arrow_scale=1.5,           # 50% longer arrows
       arrow_threshold='auto',     # Auto threshold (10% of max)
       cmap='Hot'                  # Hot colormap
   )
   viz.run()

Example 5: Simplified Butterfly Plot
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Show only mean and max in butterfly plot
   viz = EelbrainPlotly2DViz(
       display_mode="ortho",
       show_max_only=True,        # Hide individual traces
       cmap='Viridis'
   )
   viz.run()

Example 6: Four-View Layout
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Comprehensive view with four perspectives
   viz = EelbrainPlotly2DViz(
       display_mode="lyrz",       # Left, Coronal, Right, Axial
       layout_mode="horizontal",   # Better for 4 views
       arrow_scale=1.0,
       cmap='YlOrRd'
   )
   viz.run()

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
   viz.run()

Example 8: Jupyter with run() Method
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   viz = EelbrainPlotly2DViz(display_mode="lr")
   
   # Inline mode
   viz.run()
   
   # Or JupyterLab tab mode
   # viz.run(mode='jupyterlab')

Example 9: Multiple Visualizations in Notebook
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
       viz.run()

Working with Eelbrain Data
---------------------------

Example 10: Using Eelbrain NDVar
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain import datasets
   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Load Eelbrain data
   data_ds = datasets.get_mne_sample(src='vol', ori='vector')
   y = data_ds['src']  # NDVar format
   
   # Visualize
   viz = EelbrainPlotly2DViz(y=y, cmap='Hot')
   viz.run()

Example 11: Brain Region Filtering
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Apply parcellation to filter specific regions
   viz = EelbrainPlotly2DViz(
       y=None,                    # Use built-in sample data
       region='aparc+aseg',       # Apply aparc+aseg parcellation
       cmap='Viridis',
       show_max_only=True
   )
   viz.run()

Example 12: Custom Colormap with Region
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Custom colormap with parcellation
   custom_cmap = [
       [0, 'rgba(255,255,0,0.5)'],    # Yellow with 50% transparency
       [0.5, 'rgba(255,165,0,0.8)'],  # Orange with 80% transparency
       [1, 'rgba(255,0,0,1.0)']       # Red with full opacity
   ]
   
   viz = EelbrainPlotly2DViz(
       y=None,
       region='aparc+aseg',
       cmap=custom_cmap,
       show_max_only=False,
       arrow_threshold=0.1
   )
   viz.run()

Export Examples
---------------

Example 13: Export Static Images
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Create visualization
   viz = EelbrainPlotly2DViz(display_mode="lyr")
   
   # Export all views as PNG images
   result = viz.export_images(
       output_dir="./my_brain_plots",
       time_idx=30,
       format="png"
   )
   
   if result["status"] == "success":
       print("Exported files:")
       for plot_type, filepath in result["files"].items():
           print(f"  {plot_type}: {filepath}")
   else:
       print(f"Export failed: {result['message']}")

Example 14: Export Different Formats
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   viz = EelbrainPlotly2DViz(display_mode="ortho", cmap='Hot')
   
   # Export as different formats
   for fmt in ['png', 'jpg', 'svg', 'pdf']:
       result = viz.export_images(
           output_dir=f"./output_{fmt}",
           time_idx=20,
           format=fmt
       )
       print(f"{fmt.upper()}: {result['status']}")

Server Configuration Examples
------------------------------

Example 15: Custom Port
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   viz = EelbrainPlotly2DViz(display_mode="lyr")
   
   # Run on specific port
   viz.run(port=8888)  # Add debug=True if you need verbose output

Example 16: Production Mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   viz = EelbrainPlotly2DViz(
       display_mode="lyr",
       layout_mode="horizontal"
   )
   
   # Run without debug mode (for production)
   viz.run(port=8050, debug=False)

Display Mode Examples
---------------------

Example 17: All Single View Modes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Demonstrate all single view modes
   single_views = {
       'x': 'Sagittal view (left-right)',
       'y': 'Coronal view (front-back)',
       'z': 'Axial view (top-bottom)',
       'l': 'Left hemisphere',
       'r': 'Right hemisphere'
   }
   
   for mode, description in single_views.items():
       print(f"\n{mode}: {description}")
       viz = EelbrainPlotly2DViz(display_mode=mode)
       viz.run()

Example 18: All Multi-View Modes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Demonstrate multi-view modes
   multi_views = {
       'ortho': 'Orthogonal views (x+y+z)',
       'lr': 'Both hemispheres',
       'lyr': 'Left + Coronal + Right',
       'lzr': 'Left + Axial + Right',
       'xz': 'Sagittal + Axial',
       'yx': 'Coronal + Sagittal',
       'yz': 'Coronal + Axial'
   }
   
   for mode, description in multi_views.items():
       print(f"\n{mode}: {description}")
       viz = EelbrainPlotly2DViz(
           display_mode=mode,
           layout_mode="horizontal"
       )
       viz.run()

Example 19: Four-View Modes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Four-view comprehensive layouts
   four_views = {
       'lyrz': 'Left + Coronal + Right + Axial',
       'lzry': 'Left + Axial + Right + Coronal'
   }
   
   for mode, description in four_views.items():
       print(f"\n{mode}: {description}")
       viz = EelbrainPlotly2DViz(
           display_mode=mode,
           layout_mode="horizontal",  # Recommended for 4 views
           arrow_scale=0.8            # Smaller arrows for clarity
       )
       viz.run()

Customization Examples
-----------------------

Example 20: Progressive Arrow Threshold
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Compare different threshold levels
   thresholds = [None, 'auto', 0.1, 0.2, 0.3]
   
   for threshold in thresholds:
       print(f"\nThreshold: {threshold}")
       viz = EelbrainPlotly2DViz(
           display_mode="lr",
           arrow_threshold=threshold,
           arrow_scale=1.0,
           cmap='Hot'
       )
       viz.run()

Example 21: Arrow Scale Comparison
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Compare different arrow scales
   scales = [0.5, 1.0, 1.5, 2.0]
   
   for scale in scales:
       print(f"\nArrow Scale: {scale}")
       viz = EelbrainPlotly2DViz(
           display_mode="lyr",
           arrow_scale=scale,
           arrow_threshold='auto',
           cmap='YlOrRd'
       )
       viz.run()

Example 22: Colormap Comparison
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Compare different built-in colormaps
   colormaps = ['YlOrRd', 'Hot', 'Viridis', 'OrRd', 'Reds']
   
   for cmap in colormaps:
       print(f"\nColormap: {cmap}")
       viz = EelbrainPlotly2DViz(
           display_mode="lyr",
           cmap=cmap,
           show_max_only=True
       )
       viz.run()

Complete Example Scripts
-------------------------

Example 23: Full Analysis Workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   #!/usr/bin/env python3
   """
   Complete workflow for LiveNeuron brain visualization.
   """
   
   from eelbrain_plotly_viz import EelbrainPlotly2DViz
   
   def main():
       print("🧠 Creating LiveNeuron Brain Visualization...")
       
       # Step 1: Basic visualization
       print("\n1. Basic visualization with sample data:")
       viz1 = EelbrainPlotly2DViz()
       
       # Step 2: Custom visualization
       print("\n2. Custom visualization with Hot colormap:")
       viz2 = EelbrainPlotly2DViz(
           y=None,
           region=None,
           cmap='Hot',
           show_max_only=True,
           arrow_threshold='auto'
       )
       
       # Step 3: With parcellation
       print("\n3. With parcellation (aparc+aseg):")
       viz3 = EelbrainPlotly2DViz(
           y=None,
           region='aparc+aseg',
           cmap='Viridis',
           show_max_only=False,
           arrow_threshold=0.1
       )
       
       # Step 4: Export images
       print("\n📷 Exporting images...")
       result = viz3.export_images(
           output_dir="./example_output", 
           time_idx=20,
           format="png"
       )
       
       if result["status"] == "success":
           print("✅ Export successful!")
           for plot_type, filepath in result["files"].items():
               print(f"  {plot_type}: {filepath}")
       
       # Step 5: Run interactive visualization
       print("\n🌐 Starting interactive visualization...")
       print("The server will start on a random port.")
       print("Check the console for the exact URL.")
       viz3.run()
   
   if __name__ == "__main__":
       main()

Tips and Best Practices
------------------------

Tip 1: Choosing Display Mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # For hemisphere comparison (recommended):
   viz = EelbrainPlotly2DViz(display_mode="lyr")
   
   # For comprehensive anatomical view:
   viz = EelbrainPlotly2DViz(display_mode="ortho")
   
   # For focused single view:
   viz = EelbrainPlotly2DViz(display_mode="l")

Tip 2: Optimizing Arrow Display
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # For dense data with many small vectors:
   viz = EelbrainPlotly2DViz(
       arrow_scale=0.7,        # Smaller arrows
       arrow_threshold='auto'   # Filter weak vectors
   )
   
   # For sparse data with strong vectors:
   viz = EelbrainPlotly2DViz(
       arrow_scale=1.5,        # Larger arrows
       arrow_threshold=None     # Show all arrows
   )

Tip 3: Layout Selection
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Vertical layout for:
   # - 1-2 views
   # - Standard displays
   # - Focus on temporal dynamics
   viz = EelbrainPlotly2DViz(
       display_mode="lr",
       layout_mode="vertical"
   )
   
   # Horizontal layout for:
   # - 3+ views
   # - Wide displays
   # - Focus on spatial patterns
   viz = EelbrainPlotly2DViz(
       display_mode="lyrz",
       layout_mode="horizontal"
   )

Tip 4: Jupyter vs Browser
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # For interactive exploration in notebook:
   viz.run()
   
   # For full-screen experience:
   viz.run(mode='external')
   
   # For quick inline preview:
   viz.run()
