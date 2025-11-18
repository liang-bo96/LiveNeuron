Changelog
=========

All notable changes to LiveNeuron are documented here.

Version 1.0.0 (2025-11-11)
--------------------------

Initial release with comprehensive features for interactive 2D brain visualization.

New Features
^^^^^^^^^^^^

**Display Modes**

* 17 different anatomical view configurations
* Single views: ``l``, ``r``, ``x``, ``y``, ``z``
* Multi views: ``lr``, ``lyr``, ``lzr``, ``xyz``, ``ortho``
* Four-view modes: ``lyrz``, ``lzry``, and all permutations
* Smart parsing of display mode strings

**Layout Modes**

* Vertical layout (default): butterfly on top, brain views below
* Horizontal layout: butterfly on left, brain views on right
* Optimized space allocation for multiple views
* Consistent sizing across all brain plots

**Interactive Features**

* Real-time hover information on brain plots showing activity values
* Click navigation on butterfly plot's time axis for precise time selection
* Unified hover mode on butterfly plot showing max/min activity
* Zoom and pan capabilities with aspect ratio preservation
* Semi-transparent hover labels to minimize occlusion

**Visualization Components**

* Heatmap-based brain projections with activity magnitude
* Vector field arrows showing direction and magnitude
* Butterfly plot for temporal dynamics
* Horizontal colorbar with unified scaling
* Dark-themed plots for better contrast

**Arrow Customization**

* ``arrow_scale`` parameter for intuitive length adjustment (default: 1.0)
* ``arrow_threshold`` parameter for magnitude-based filtering (default: 0.0)
* Smart deduplication when multiple 3D sources project to same 2D position
* Optimized rendering using Plotly's ``ff.create_quiver``

**Performance Optimizations**

* Efficient 2D binning with ``scipy.stats.binned_statistic_2d``
* Smart deduplication selecting maximum activity sources
* Incremental updates for time navigation
* Configurable bin size for resolution vs. performance trade-off

**User Experience**

* Clean, professional UI with consistent styling
* Automatic aspect ratio adjustment for brain plots
* Precise time click detection with ``spikesnap="cursor"``
* Optimized axis limits to eliminate empty space
* Hover only on heatmap (arrow hover disabled for clarity)

Technical Details
^^^^^^^^^^^^^^^^^

**Architecture**

* Built on Plotly and Dash for interactive web visualizations
* Supports both browser mode and Jupyter notebook mode
* Modular design with clear separation of concerns
* Comprehensive type hints for better IDE support

**Dependencies**

* Python >= 3.8
* Plotly >= 5.0.0
* Dash >= 2.0.0
* NumPy >= 1.20.0
* Matplotlib >= 3.3.0
* SciPy >= 1.7.0
* Eelbrain (optional)

**Testing**

* Comprehensive test suite with pytest
* Performance benchmarks
* Integration tests
* Mock utilities for isolated testing

**Documentation**

* Complete API reference
* User guide with best practices
* Quick start guide
* 18 practical examples
* Read the Docs integration

Bug Fixes
^^^^^^^^^

* Fixed hover display for quiver arrows using ``customdata``
* Fixed time click precision with proper spike configuration
* Fixed butterfly plot axis limits to eliminate empty space
* Fixed brain plot sizing consistency across all views
* Fixed colorbar positioning to prevent layout interference
* Fixed deduplication logic to select maximum activity sources
* Fixed initial vs. updated plot height inconsistency

Known Issues
^^^^^^^^^^^^

* Colorbar title may require manual adjustment in some themes
* Very large datasets (>10,000 sources) may have slower rendering
* Some edge cases in display mode parsing may not be handled

Future Plans
------------

Version 1.1.0 (Planned)
^^^^^^^^^^^^^^^^^^^^^^^

* Add R/A/S coordinate display in hover labels
* Export functionality for static images
* Support for additional data formats
* Custom colormap definitions
* Animation controls for time series

Version 1.2.0 (Planned)
^^^^^^^^^^^^^^^^^^^^^^^

* 3D visualization mode
* Multiple dataset comparison view
* Statistical overlays
* Region of interest (ROI) highlighting
* Annotation tools

Version 2.0.0 (Planned)
^^^^^^^^^^^^^^^^^^^^^^^

* Complete UI redesign with modern framework
* Real-time data streaming support
* Collaborative features for multi-user exploration
* Cloud deployment options
* Mobile-responsive design

Contributing
------------

We welcome contributions! Areas of interest:

* Performance optimizations for large datasets
* Additional display modes
* Enhanced interactivity features
* Better documentation and examples
* Bug fixes and testing

See our GitHub repository for contribution guidelines.

Migration Guide
---------------

From Pre-release Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^

If you were using pre-release or development versions, here are key changes:

**Arrow Scale**

* Old: ``arrow_scale=0.025`` (absolute scale)
* New: ``arrow_scale=1.0`` (relative scale)
* **Action**: Multiply your old scale by 40 (e.g., 0.025 → 1.0, 0.0125 → 0.5)

**Display Mode**

* Old: May have used custom view configurations
* New: Use standardized display mode strings
* **Action**: Verify your display mode strings against documentation

**Layout**

* Old: May have used custom layout parameters
* New: Use ``layout_mode="vertical"`` or ``"horizontal"``
* **Action**: Update to new layout mode parameter

**Colorbar**

* Old: Vertical colorbar next to last brain plot
* New: Horizontal colorbar below all brain plots
* **Action**: No action needed, automatically updated

**Hover Information**

* Old: Both heatmap and arrow hover enabled
* New: Only heatmap hover enabled (arrows disabled)
* **Action**: No action needed, better user experience

Release Notes
-------------

Version 1.0.0 Release Notes
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the first stable release of LiveNeuron, representing months of development
and testing. The library provides a robust, performant, and user-friendly solution
for interactive 2D brain visualization.

Key highlights:

* **Comprehensive**: 17 display modes, 2 layout modes, extensive customization
* **Performant**: Optimized rendering, smart binning, efficient updates
* **Interactive**: Real-time hover, click navigation, zoom and pan
* **Professional**: Dark theme, consistent sizing, transparent hover labels
* **Well-documented**: Complete API reference, user guide, 18 examples

We're excited to see how researchers use LiveNeuron to explore and understand
neural activity data. Feedback and contributions are welcome!

Acknowledgments
^^^^^^^^^^^^^^^

Special thanks to:

* The Plotly and Dash teams for excellent visualization tools
* The Eelbrain community for domain expertise
* Early adopters and testers for valuable feedback
* Contributors to the codebase and documentation

Support
-------

For questions, bug reports, or feature requests:

* GitHub Issues: https://github.com/liang-bo96/LiveNeuron/issues
* Documentation: https://liveneuron.readthedocs.io
* Email: liveneuron@example.com

License
-------

LiveNeuron is released under the MIT License. See LICENSE file for details.


