"""
LiveNeuron - Interactive 2D Brain Visualization Package

Interactive 2D brain visualization using Plotly and Dash.
Supports Eelbrain NDVar data format with built-in MNE sample data.
"""

from typing import Any, Dict, List, Optional, Union

import dash
import numpy as np

from eelbrain import NDVar

from .app_controller import AppControllerMixin
from .data_loader import DataLoaderMixin
from .layout_builder import LayoutBuilderMixin
from .plot_factory import PlotFactoryMixin
from .sample_data import create_sample_brain_data

__version__ = "1.0.0"
__author__ = "LiveNeuron Team"


class EelbrainPlotly2DViz(
    DataLoaderMixin,
    PlotFactoryMixin,
    LayoutBuilderMixin,
    AppControllerMixin,
):
    """Interactive 2D brain visualization for brain data using Plotly and Dash.

    Based on :class:`plot.GlassBrain`, provides interactive 2D projections of brain
    volume data with butterfly plot and arrow visualization for vector data.

    Parameters
    ----------
    y
        Data to plot ([case,] time, source[, space]).
        If ``y`` has a case dimension, the mean is plotted.
        If ``y`` has a space dimension, the norm is plotted.
        If None, uses MNE sample data for demonstration.
        pass an Eelbrain NDVar or the
        :class:`~eelbrain_plotly_viz.sample_data.SampleDataNDVar` returned by
        :func:`eelbrain_plotly_viz.sample_data.create_sample_brain_data`.
    region
        Brain region to load using aparc+aseg parcellation.
        If None, loads all regions. Only used when y is None.
    cmap
        Plotly colorscale for heatmaps. Can be:
        - Built-in colorscale name (e.g., 'YlOrRd', 'OrRd', 'Reds', 'Viridis')
        - Custom colorscale list (e.g., [[0, 'white'], [1, 'red']])
        Default is 'YlOrRd' (Yellow-Orange-Red) which works well with white
        background and doesn't obscure arrows. See
        https://plotly.com/python/builtin-colorscales/ for all available options.
    vmin
        Optional lower bound for the color range. If provided, locks the minimum
        for all projections and time points.
    vmax
        Optional upper bound for the color range. If provided, locks the maximum
        for all projections and time points.
    show_max_only
        If True, butterfly plot shows only mean and max traces.
        If False, butterfly plot shows individual source traces, mean, and max.
        Default is False.
    arrow_threshold
        Threshold for displaying arrows in brain projections. Only arrows with
        magnitude greater than this value will be displayed. If None, all arrows
        are shown. If 'auto', uses 10% of the maximum magnitude as threshold.
        Default is None.
    arrow_scale
        Relative scale factor for arrow length in brain projections. The default
        value of 1.0 provides a good balance for most datasets. Use 0.5 for half
        the length, 2.0 for double the length, etc. Useful for adjusting
        visualization clarity when vectors have large magnitudes or high density.
        Default is 1.0. Typical range: 0.5 (short) to 2.0 (long).
    layout_mode
        Layout arrangement mode for the visualization interface. Options:
        - 'vertical': Traditional layout with butterfly plot on top, brain views below (default)
        - 'horizontal': Compact layout with butterfly plot on left, brain views on right
        Default is 'vertical' for backward compatibility.
    display_mode
        Anatomical view mode for brain projections. Options:
        - 'ortho': Orthogonal views (sagittal + coronal + axial) - Default
        - 'x': Sagittal view only
        - 'y': Coronal view only
        - 'z': Axial view only
        - 'xz': Sagittal + Axial views
        - 'yx': Coronal + Sagittal views
        - 'yz': Coronal + Axial views
        - 'l': Left hemisphere view only
        - 'r': Right hemisphere view only
        - 'lr': Both hemisphere views (left + right)
        - 'lzr': Left + Axial + Right hemispheres
        - 'lyr': Left + Coronal + Right (GlassBrain default - best for hemisphere comparison)
        - 'lzry': Left + Axial + Right + Coronal (4-view comprehensive)
        - 'lyrz': Left + Coronal + Right + Axial (4-view comprehensive)
        Default is 'lyr' (GlassBrain standard) for optimal hemisphere comparison.
    show_labels
        If True, shows plot titles and legends (e.g., 'Source Activity Time Series',
        'Source 0', 'Source 1', etc.). If False, hides all titles and legends for a
        cleaner visualization. Default is False.

    Notes
    -----
    Expected input format follows the same pattern as :class:`plot.GlassBrain`:

    - For vector data: NDVar with dimensions ([case,] time, source, space)
    - For scalar data: NDVar with dimensions ([case,] time, source)
    - If case dimension present: mean across cases is plotted
    - If space dimension present: norm across space is plotted for butterfly plot
    - ``create_sample_brain_data`` returns a minimal NDVar-like object compatible
      with the ``y`` parameter for quick demos
    """

    def __init__(
        self,
        y: Optional[NDVar] = None,
        region: Optional[str] = None,
        cmap: Union[str, List] = "YlOrRd",
        vmin: Optional[float] = None,
        vmax: Optional[float] = None,
        show_max_only: bool = False,
        arrow_threshold: Optional[Union[float, str]] = None,
        arrow_scale: float = 1.0,
        realtime: bool = False,
        layout_mode: str = "vertical",
        display_mode: str = "lyr",
        show_labels: bool = False,
    ):
        """Initialize the visualization app and load data."""
        # Use regular Dash with modern Jupyter integration
        # Add external CSS to remove ALL default margins/padding from Dash containers
        external_stylesheets = [
            {
                "href": "data:text/css;charset=utf-8,"
                + "*{box-sizing:border-box;}"
                + "html{margin:0!important;padding:0!important;height:auto!important;overflow:hidden;}"
                + "body{margin:0!important;padding:0!important;height:auto!important;overflow:hidden;}"
                + "#react-entry-point{margin:0!important;padding:0!important;height:auto!important;}"
                + "#_dash-app-content{margin:0!important;padding:0!important;height:auto!important;}"
                + "._dash-loading{margin:0!important;padding:0!important;}",
                "rel": "stylesheet",
            }
        ]
        self.app: dash.Dash = dash.Dash(
            __name__, external_stylesheets=external_stylesheets
        )

        # Initialize data attributes
        self.glass_brain_data: Optional[np.ndarray] = None  # (n_sources, 3, n_times)
        self.butterfly_data: Optional[np.ndarray] = None  # (n_sources, n_times)
        self.source_coords: Optional[np.ndarray] = None  # (n_sources, 3)
        self.time_values: Optional[np.ndarray] = None  # (n_times,)
        self.region_of_brain: Optional[str] = region  # Region of brain to visualize
        self.cmap: Union[str, List] = cmap  # Colorscale for heatmaps
        self.user_vmin: Optional[float] = vmin  # Optional user-specified color min
        self.user_vmax: Optional[float] = vmax  # Optional user-specified color max
        self.show_max_only: bool = show_max_only  # Control butterfly plot display mode
        # Threshold for displaying arrows
        self.arrow_threshold: Optional[Union[float, str]] = arrow_threshold
        # Scale factor for arrow length
        self.arrow_scale: float = arrow_scale
        self.is_jupyter_mode: bool = False  # Track if running in Jupyter mode
        self.realtime_mode_default = (
            ["realtime"] if realtime else []
        )  # Default state for real-time mode
        self.show_labels: bool = show_labels  # Control titles and legends display
        self._current_layout_config: Optional[Dict[str, Any]] = None

        # Validate and set layout mode
        valid_layouts = ["vertical", "horizontal"]
        if layout_mode not in valid_layouts:
            raise ValueError(
                f"layout_mode must be one of {valid_layouts}, got '{layout_mode}'"
            )
        self.layout_mode: str = layout_mode

        # Set display mode and parse required views
        self.display_mode: str = display_mode
        # Parse display mode to determine required views (includes validation)
        self.brain_views = self._parse_display_mode(display_mode)

        # Load data
        if y is not None:
            self._load_ndvar_data(y)
        else:
            self._load_source_data(region)

        # Calculate and store fixed axis ranges for each view to prevent size changes
        self._calculate_view_ranges()

        # Unify view sizes to ensure all brain plots have consistent display size
        # This is especially important in horizontal layout mode
        self._unify_view_sizes_for_jupyter()

        # Calculate global colormap range across all time points for consistent visualization
        self._calculate_global_colormap_range()

        # Setup app
        self._setup_layout()
        self._setup_callbacks()


# Create alias for backward compatibility
BrainPlotly2DViz = EelbrainPlotly2DViz

__all__ = [
    "EelbrainPlotly2DViz",
    "BrainPlotly2DViz",  # Alias for compatibility
    "create_sample_brain_data",
]
