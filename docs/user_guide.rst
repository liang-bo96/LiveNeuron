User Guide
==========

This comprehensive guide covers all features and configuration options of LiveNeuron based on the actual implementation.

Getting Started
---------------

Basic Workflow
^^^^^^^^^^^^^^

1. **Create** visualization object with desired parameters
2. **Launch** with ``run()``
3. **Interact** with hover, click, and zoom
4. **Export** static images if needed

.. code-block:: python

   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Step 1: Create
   viz = EelbrainPlotly2DViz(display_mode="lyr")

   # Step 2: Launch
   viz.run()  # Auto inline in Jupyter; external browser otherwise

   # Step 3: Interact (in browser/notebook)
   # Step 4: Export
   viz.export_images(output_dir="./plots", time_idx=30)

Run Modes
---------

.. note::

   In IPython shells (outside notebooks), explicitly pass ``mode="external"`` to
   ``run()`` to start a visualization that can be accessed in a browser.
* **Interpreter / shell**: uses built-in MNE sample data if ``y`` is omitted; launches a server on a random port (explicit ``mode="external"`` recommended).

  .. code-block:: python

     viz = EelbrainPlotly2DViz()
     viz.run(mode="external")

* **Notebook**: auto-selects ``mode="inline"`` (embedded IFrame). Choose explicitly if you want a browser or a Lab tab.

  .. code-block:: python

     viz = EelbrainPlotly2DViz()
     viz.run()                    # inline by default in notebooks; use mode="external" for shells
     # viz.run(mode="jupyterlab")  # open in JupyterLab tab
     # viz.run(mode="external")    # force external browser

Understanding Display Modes
----------------------------

Display modes control which anatomical views are shown and in what order.

Anatomical Coordinate System
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* **X-axis (Sagittal)**: Side view, left-right through brain
* **Y-axis (Coronal)**: Front view, front-back through brain
* **Z-axis (Axial)**: Top view, top-bottom through brain
* **L**: Left hemisphere lateral view
* **R**: Right hemisphere lateral view

Single View Modes
^^^^^^^^^^^^^^^^^

Use single letters for individual views:

.. code-block:: python

   viz = EelbrainPlotly2DViz(display_mode="x")  # Sagittal only
   viz = EelbrainPlotly2DViz(display_mode="y")  # Coronal only
   viz = EelbrainPlotly2DViz(display_mode="z")  # Axial only
   viz = EelbrainPlotly2DViz(display_mode="l")  # Left hemisphere only
   viz = EelbrainPlotly2DViz(display_mode="r")  # Right hemisphere only

Multi-View Modes
^^^^^^^^^^^^^^^^

Combine letters for multiple views:

.. code-block:: python

   # Orthogonal views (special keyword)
   viz = EelbrainPlotly2DViz(display_mode="ortho")  # x + y + z

   # Hemisphere combinations
   viz = EelbrainPlotly2DViz(display_mode="lr")     # Left + Right
   viz = EelbrainPlotly2DViz(display_mode="lyr")    # Left + Coronal + Right (default)
   viz = EelbrainPlotly2DViz(display_mode="lzr")    # Left + Axial + Right

   # Axis combinations
   viz = EelbrainPlotly2DViz(display_mode="xz")     # Sagittal + Axial
   viz = EelbrainPlotly2DViz(display_mode="yx")     # Coronal + Sagittal
   viz = EelbrainPlotly2DViz(display_mode="yz")     # Coronal + Axial

Four-View Modes
^^^^^^^^^^^^^^^

For comprehensive anatomical coverage:

.. code-block:: python

   # Four views in different orders
   viz = EelbrainPlotly2DViz(display_mode="lyrz")   # L + Coronal + R + Axial
   viz = EelbrainPlotly2DViz(display_mode="lzry")   # L + Axial + R + Coronal

**Note:** Order of letters determines display order of anatomical projections (left-to-right).

Layout Modes
------------

Vertical Layout (Default)
^^^^^^^^^^^^^^^^^^^^^^^^^^

**When to use:**

* General use, including 1–4 projections
* When the detailed activity time course should be prominent
* When you want more horizontal space per projection

**Characteristics:**

* Detailed activity time course on top
* Brain projections arranged beneath
* Good for multiple projections while preserving horizontal space

.. code-block:: python

   viz = EelbrainPlotly2DViz(
       display_mode="lyr",
       layout_mode="vertical"  # Default
   )

Horizontal Layout
^^^^^^^^^^^^^^^^^

**When to use:**

* Wide screens or presentations
* When spatial layout (left-to-right comparison) is the focus

**Characteristics:**

* Detailed activity time course on the left
* Brain projections arranged to the right


.. code-block:: python

   viz = EelbrainPlotly2DViz(
       display_mode="lyrz",
       layout_mode="horizontal"
   )

Custom Layouts
^^^^^^^^^^^^^^

Create custom layouts by inheriting from :class:`~eelbrain_plotly_viz.layout_builder_mixin.LayoutBuilder` and registering them with :func:`~eelbrain_plotly_viz.layout_builder_mixin.register_layout`.
See the *Layout System* section in the API reference for a complete example.

Once registered, you can select your layout with ``layout_mode``:

.. code-block:: python

   viz = EelbrainPlotly2DViz(layout_mode="custom")

Arrow Visualization
-------------------

Understanding Arrows
^^^^^^^^^^^^^^^^^^^^

Arrows represent vector fields in brain data:

* **Direction**: Shows orientation of activity (e.g., current flow)
* **Length**: Indicates magnitude (controlled by ``arrow_scale``)
* **Visibility**: Filtered by ``arrow_threshold``

Arrow Scale Parameter
^^^^^^^^^^^^^^^^^^^^^

The ``arrow_scale`` parameter (default: 1.0) controls arrow length:

.. code-block:: python

   # Short arrows for dense data
   viz = EelbrainPlotly2DViz(arrow_scale=0.5)

   # Default balanced length
   viz = EelbrainPlotly2DViz(arrow_scale=1.0)

   # Long arrows for sparse data
   viz = EelbrainPlotly2DViz(arrow_scale=2.0)

**Recommendations:**

* Dense vector fields: 0.5 - 0.8
* Moderate density: 1.0 (default)
* Sparse fields: 1.2 - 2.0

Arrow Threshold Parameter
^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``arrow_threshold`` parameter filters arrows by magnitude:

.. code-block:: python

   # Show all arrows
   viz = EelbrainPlotly2DViz(arrow_threshold=None)

   # Auto threshold (10% of maximum magnitude)
   viz = EelbrainPlotly2DViz(arrow_threshold='auto')

   # Custom threshold
   viz = EelbrainPlotly2DViz(arrow_threshold=0.15)

**When to use:**

* ``None``: Small datasets or when all vectors are important
* ``'auto'``: Good default for most cases
* *float*: Fine-tune based on data characteristics

Combined Arrow Optimization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For best results, combine both parameters:

.. code-block:: python

   # Dense data with many small vectors
   viz = EelbrainPlotly2DViz(
       arrow_scale=0.7,
       arrow_threshold='auto'
   )

   # Sparse data with clear patterns
   viz = EelbrainPlotly2DViz(
       arrow_scale=1.5,
       arrow_threshold=0.05
   )

Color Mapping
-------------

Built-in Colormaps
^^^^^^^^^^^^^^^^^^

LiveNeuron supports Plotly's built-in colorscales:

.. code-block:: python

   # Sequential colormaps
   viz = EelbrainPlotly2DViz(cmap='YlOrRd')    # Yellow-Orange-Red (default)
   viz = EelbrainPlotly2DViz(cmap='Hot')       # Hot (red/orange/yellow)
   viz = EelbrainPlotly2DViz(cmap='Viridis')   # Perceptually uniform
   viz = EelbrainPlotly2DViz(cmap='OrRd')      # Orange-Red
   viz = EelbrainPlotly2DViz(cmap='Reds')      # Red scale

See https://plotly.com/python/builtin-colorscales/ for all options.

Custom Colormaps
^^^^^^^^^^^^^^^^

Create custom colorscales with transparency:

.. code-block:: python

   # Custom gradient with transparency
   custom_cmap = [
       [0, 'rgba(255,255,0,0.5)'],    # Yellow, 50% transparent
       [0.5, 'rgba(255,165,0,0.8)'],  # Orange, 80% opaque
       [1, 'rgba(255,0,0,1.0)']       # Red, fully opaque
   ]

   viz = EelbrainPlotly2DViz(cmap=custom_cmap)

**Color Range:**

* Automatically scaled to data range (min to max)
* Consistent across all views and time points
* Unified colorbar shows current scaling
* Override manually with ``vmin`` / ``vmax`` to lock the range

.. code-block:: python

   viz = EelbrainPlotly2DViz(vmin=-2.0, vmax=2.0)

Activity Time Course Plot Modes
--------------------

Full Mode (Default)
^^^^^^^^^^^^^^^^^^^

Shows a sampled set of source traces plus statistics (random subset for readability):

.. code-block:: python

   viz = EelbrainPlotly2DViz(show_max_only=False)

**Displays:**

* Random subset of source activity traces
* Mean activity
* Maximum activity across all sources

Simplified Mode
^^^^^^^^^^^^^^^

Shows only summary statistics:

.. code-block:: python

   viz = EelbrainPlotly2DViz(show_max_only=True)

**Displays:**

* Mean activity
* Maximum activity

**When to use:**

* You want a clean summary without individual traces
* Presentations or screenshots where mean/max is enough

Interactive Features
--------------------

Hover Information
^^^^^^^^^^^^^^^^^

**Brain Plots:**

* Hover over any voxel to see activity value
* Shows magnitude at current time point

**Detailed activity time course:**

* Hover over time axis to see max and min activity
* Displays values for all visible traces

Time Navigation
^^^^^^^^^^^^^^^

**Click to Navigate:**

* Click anywhere on the time-course axis
* Brain views instantly update to that time point
* Precise time selection with spike indicator


Zoom and Pan
^^^^^^^^^^^^

**Mouse Controls:**

* **Mouse Wheel**: Zoom in/out
* **Click + Drag**: Box zoom (default drag mode)
* **Pan**: Select the pan tool in the toolbar, then drag to move the view
* **Double-click**: Reset to original view


Data Input
----------

Using Built-in Sample Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Simplest option for testing and learning:

.. code-block:: python

   # Use built-in MNE sample data
   viz = EelbrainPlotly2DViz(y=None)

**Characteristics:**

* 1589 sources in volumetric source space
* 76 time points (-100ms to 400ms)
* Vector data (3D current dipoles)
* Requires Eelbrain installed

Using Eelbrain NDVar
^^^^^^^^^^^^^^^^^^^^^

For your own data:

.. code-block:: python

   from eelbrain import datasets
   from eelbrain_plotly_viz import EelbrainPlotly2DViz

   # Load Eelbrain data
   data_ds = datasets.get_mne_sample(src='vol', ori='vector')
   y = data_ds['src']  # NDVar with dimensions (case, time, source, space)

   # Visualize
   viz = EelbrainPlotly2DViz(y=y)

**Expected Dimensions:**

* Vector data: ``([case,] time, source, space)``
* Scalar data: ``([case,] time, source)``
* If case dimension present: mean is computed automatically


Running the Application
-----------------------

Browser Mode
^^^^^^^^^^^^^^^^^^^^^^^

Opens in external browser:

.. code-block:: python

   viz = EelbrainPlotly2DViz()
   viz.run(mode="external")  # Random port; defaults to inline in notebooks, external browser otherwise

   # Or specify port
   viz.run(port=8888, mode="external")  # Force browser if inline is detected


Jupyter Modes (Default)
^^^^^^^^^^^^^

Multiple options for Jupyter notebooks:

.. code-block:: python

   # Inline display (embedded in notebook) - auto size
   viz.run()

   # JupyterLab tab (opens in separate tab)
   viz.run(mode='jupyterlab')


Exporting Images
----------------

Basic Export
^^^^^^^^^^^^

Export current view as static image:

.. code-block:: python

   result = viz.export_images(
       output_dir="./images",
       time_idx=30,
       format="png"
   )

   if result["status"] == "success":
       for plot_type, filepath in result["files"].items():
           print(f"{plot_type}: {filepath}")

**Exports:**

* All brain projection views
* Activity Time Course plot
* Separate files for each

Supported Formats
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # PNG (default, best for presentations)
   viz.export_images(format="png")

   # JPEG (smaller file size)
   viz.export_images(format="jpg")

   # SVG (vector, scalable)
   viz.export_images(format="svg")

   # PDF (publication quality)
   viz.export_images(format="pdf")

Performance Optimization
------------------------

For Large Datasets
^^^^^^^^^^^^^^^^^^

1. **Use arrow threshold**:

   .. code-block:: python

      viz = EelbrainPlotly2DViz(arrow_threshold='auto')

2. **Simplify detailed activity time course**:

   .. code-block:: python

      viz = EelbrainPlotly2DViz(show_max_only=True)

3. **Use focused display modes**:

   .. code-block:: python

      viz = EelbrainPlotly2DViz(display_mode="lr")  # Fewer views

Combined Optimization
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Optimized for large dataset
   viz = EelbrainPlotly2DViz(
       display_mode="lr",          # Only 2 views
       layout_mode="horizontal",   # Better layout
       arrow_scale=0.7,            # Smaller arrows
       arrow_threshold='auto',     # Filter weak vectors
       show_max_only=True,         # Simplified time course
       cmap='Hot'
   )

Best Practices
--------------

For Presentations
^^^^^^^^^^^^^^^^^

.. code-block:: python

   viz = EelbrainPlotly2DViz(
       display_mode="lyr",          # Standard comparison view
       layout_mode="horizontal",    # Wide screen friendly
       arrow_scale=1.2,            # Slightly larger arrows
       arrow_threshold='auto',     # Clean visualization
       show_max_only=True,         # Focus on patterns
       cmap='Hot'                  # High contrast
   )

   viz.run(mode='external')  # Full screen

For Publications
^^^^^^^^^^^^^^^^

.. code-block:: python

   viz = EelbrainPlotly2DViz(
       display_mode="lyr",
       arrow_scale=1.0,
       arrow_threshold='auto',
       cmap='YlOrRd'               # Publication-friendly
   )

   # Export high-quality images
   viz.export_images(
       output_dir="./publication_figures",
       time_idx=30,
       format="pdf"  # Vector format for publications
   )

For Interactive Exploration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   viz = EelbrainPlotly2DViz(
       display_mode="lyrz",         # Comprehensive views
       layout_mode="horizontal",    # Better for exploration
       arrow_scale=1.0,
       arrow_threshold=None,        # See all vectors initially
       show_max_only=False,         # Full time-course information
       cmap='Viridis'
   )

   viz.run()  # Enable debug with debug=True when troubleshooting

Troubleshooting
---------------

Common Issues
^^^^^^^^^^^^^

**Issue: Random port is inconvenient**

Solution:

.. code-block:: python

   viz.run(port=8888)  # Use fixed port

**Issue: Arrows too dense or unclear**

Solution:

.. code-block:: python

   viz = EelbrainPlotly2DViz(
       arrow_scale=0.7,            # Reduce size
       arrow_threshold='auto'      # Filter weak ones
   )

**Issue: Detailed activity time course too cluttered**

Solution:

.. code-block:: python

   viz = EelbrainPlotly2DViz(show_max_only=True)

**Issue: Slow performance**

Solution:

.. code-block:: python

   viz = EelbrainPlotly2DViz(
       display_mode="lr",          # Fewer views
       arrow_threshold='auto',     # Fewer arrows
       show_max_only=True         # Simpler time course
   )

**Issue: Export fails**

Check:

1. Output directory exists or can be created
2. Kaleido is installed (included in dependencies, upgrade if needed): ``pip install -U kaleido``
3. Sufficient disk space

Debug Mode
^^^^^^^^^^

Debug mode is off by default for a clean UI. Enable it when troubleshooting:

.. code-block:: python

   viz.run(debug=True)

This provides:

* Detailed console output
* Error tracebacks
* Performance information
