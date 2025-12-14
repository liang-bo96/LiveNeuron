"""
LiveNeuro 2D Brain Visualization.

This module provides the core LiveNeuro class, an interactive 2D visualization
interface for Eelbrain's NDVar data structures. It transforms neuroscience data
into explorable brain maps and time-series plots.
"""

from typing import Optional, Union, List, Dict, Any

import dash
import numpy as np
from eelbrain import NDVar

from ._data_loader_helper import BrainData, DataLoaderHelper
from ._plot_factory_helper import PlotFactoryHelper
from ._layout_helper import LayoutBuilderHelper, LAYOUTS
from ._app_controller_helper import AppControllerHelper


class LiveNeuro:
    """Interactive 2D brain visualization for brain data using Plotly and Dash.

    Visualization for 3D vector field time series. Provides activity time course
    with interactive 2D projections of brain volume vector data.

    Parameters
    ----------
    y
        Data to plot ([case,] time, source[, space]).
        If ``y`` has a case dimension, the mean is plotted.
        If ``y`` has a space dimension, the norm is plotted.
        If None, uses MNE sample data for demonstration.
        Pass an Eelbrain NDVar or the sample data object returned by
        :func:`liveneuro.create_sample_brain_data`.
    cmap
        Plotly colorscale for heatmaps. Can be:
        - Built-in colorscale name (e.g., 'YlOrRd', 'OrRd', 'Reds', 'Viridis')
        - Custom colorscale list (e.g., [[0, 'white'], [1, 'red']])
        Default is 'YlOrRd' (Yellow-Orange-Red) which works well with white
        background and doesn't obscure arrows. See
        https://plotly.com/python/builtin-colorscales/ for all available options.
    vmin
        Optional lower bound for the color range. If provided, locks the minimum
        for all projections and time points. Always 0.
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
    Expected input format

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
                "href": (
                    "data:text/css;charset=utf-8,"
                    + "*{box-sizing:border-box;}"
                    + "html{margin:0!important;padding:0!important;"
                    + "height:auto!important;overflow:hidden;}"
                    + "body{margin:0!important;padding:0!important;"
                    + "height:auto!important;overflow:hidden;}"
                    + "#react-entry-point{margin:0!important;padding:0!important;"
                    + "height:auto!important;}"
                    + "#_dash-app-content{margin:0!important;padding:0!important;"
                    + "height:auto!important;}"
                    + "._dash-loading{margin:0!important;padding:0!important;}"
                ),
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

        # Initialize source space attributes
        self.source_space: Any = None
        self.parcellation: Optional[Any] = None
        self.view_ranges: Dict[str, Dict[str, List[float]]] = {}
        self.global_vmin: float = 0.0
        self.global_vmax: float = 1.0

        # Internal data model (populated during initialization)
        self._brain_data: Optional[BrainData] = None

        # Internal helper components
        self._data_loader = DataLoaderHelper()
        self._plot_factory = PlotFactoryHelper(self)
        self._layout_helper = LayoutBuilderHelper(self)
        self._app_controller = AppControllerHelper(self)

        # Validate and set layout mode (allow registered custom layouts)
        valid_layouts = list(LAYOUTS.keys())
        if layout_mode not in valid_layouts:
            raise ValueError(
                f"layout_mode must be one of {valid_layouts}, got '{layout_mode}'"
            )
        self.layout_mode: str = layout_mode

        # Set display mode and parse required views
        self.display_mode: str = display_mode
        # Parse display mode to determine required views (includes validation)
        self.brain_views = self._data_loader._parse_display_mode(display_mode)

        # Load data (data loader helper responsibility)
        if y is not None:
            brain_data = self._data_loader._load_ndvar_data(y)
        else:
            brain_data = self._data_loader._load_source_data()

        # Store data model and mirror key attributes for backward compatibility
        self._brain_data = brain_data
        self.glass_brain_data = brain_data.glass_brain_data
        self.butterfly_data = brain_data.butterfly_data
        self.source_coords = brain_data.source_coords
        self.time_values = brain_data.time_values
        self.source_space = brain_data.source_space
        self.parcellation = brain_data.parcellation

        # Calculate and store fixed axis ranges for each view to prevent size changes
        self.view_ranges = self._data_loader._calculate_view_ranges(
            self.source_coords, self.brain_views
        )

        # Unify view sizes to ensure all brain plots have consistent display size
        # This is especially important in horizontal layout mode
        self.view_ranges = self._data_loader._unify_view_sizes_for_jupyter(
            self.view_ranges
        )

        # Calculate global colormap range across all time points for consistent visualization
        self.global_vmin, self.global_vmax = (
            self._data_loader._calculate_global_colormap_range(
                self.glass_brain_data, self.user_vmax
            )
        )

        # Setup app layout and callbacks
        self._rebuild_layout()
        self._app_controller._setup_callbacks()

    def _rebuild_layout(self) -> None:
        """Rebuild Dash layout and update current layout config."""
        layout_info = self._layout_helper._setup_layout()
        config = layout_info.get("config")
        layout = layout_info.get("layout")
        if config is not None:
            self._current_layout_config = config
        if layout is not None:
            self.app.layout = layout

    def _prepare_for_jupyter(self) -> None:
        """Prepare visualization for Jupyter display (layout + sizing)."""
        self.is_jupyter_mode = True
        # Unify view sizes for Jupyter mode to ensure consistent display
        self.view_ranges = self._data_loader._unify_view_sizes_for_jupyter(
            self.view_ranges
        )
        # Rebuild layout with Jupyter-specific styles
        self._rebuild_layout()

    def run(
        self,
        port: Optional[int] = None,
        debug: bool = False,
        mode: Optional[str] = None,
    ) -> None:
        self._app_controller.run(port=port, debug=debug, mode=mode)

    def _show_in_jupyter(self, debug: bool = False) -> None:
        self._app_controller._show_in_jupyter(debug=debug)

    def export_images(
        self,
        output_dir: str = "./images",
        time_idx: Optional[int] = None,
        format: str = "png",
    ):
        return self._app_controller.export_images(
            output_dir=output_dir, time_idx=time_idx, format=format
        )


# Run the app when script is executed directly
if __name__ == "__main__":
    try:
        # Colormap options (default is 'YlOrRd' - white-background friendly):
        # cmap = 'YlOrRd'        # Yellow → Orange → Red (DEFAULT, best for white background)
        # cmap = 'OrRd'          # Orange → Red (good for white background)
        # cmap = 'Reds'          # White → Red (minimal contrast)
        # cmap = 'Viridis'       # Purple → Blue → Green → Yellow (perceptually uniform)
        # cmap = 'Hot'           # Black → Red → Yellow → White (NOT recommended - obscures arrows)

        # Example: Custom cmap (starts from white to avoid obscuring arrows)
        # cmap = [
        #     [0, "rgba(255,255,255,0.8)"],  # White with 80% opacity (low activity)
        #     [0.5, "rgba(255,165,0,0.9)"],  # Orange with 90% opacity
        #     [1, "rgba(255,0,0,1.0)"],  # Red with full opacity (high activity)
        # ]

        # Butterfly plot display options:
        # show_max_only=False: Shows individual source traces + mean + max (default)
        # show_max_only=True:  Shows only mean + max traces (cleaner view)

        # Arrow threshold options:
        # arrow_threshold=None: Show all arrows (default)
        # arrow_threshold='auto': Show arrows with magnitude > 10% of max
        # arrow_threshold=0.01: Show arrows with magnitude > 0.01 (custom threshold)

        # Arrow scale options:
        # arrow_scale=1.0: Default arrow length (good for most cases)
        # arrow_scale=0.5: Half length (useful for dense or high-magnitude data)
        # arrow_scale=2.0: Double length (useful for sparse or low-magnitude data)

        # Method 1: Pass data directly using y parameter (same as plot.GlassBrain)
        # from eelbrain import datasets
        #
        # # Load your data - NDVar with dimensions ([case,] time, source[, space])
        # data_ds = datasets.get_mne_sample(src='vol', ori='vector')
        # y = data_ds['src']  # NDVar with dimensions (case, time, source, space)
        #
        # # Create visualization with your data
        # viz_2d = LiveNeuro(
        #     y=y,  # Pass NDVar directly - same format as plot.GlassBrain
        #     cmap=cmap,
        #     show_max_only=False,
        #     arrow_threshold='auto'  # Only show significant arrows
        # )

        # Method 2: Use default MNE sample data with custom options
        viz_2d = LiveNeuro(
            cmap="Reds",
            show_max_only=False,
            arrow_threshold=None,  # Show all arrows
            layout_mode="vertical",
            display_mode="lzry",
            arrow_scale=0.5,  # Shorter arrows for better visibility
        )

        # Example: Export plot images
        # Uncomment the lines below to export images before running the app:
        # result = viz_2d.export_images(
        #     output_dir="./brain_images",
        #     time_idx=10,  # Export plots for time index 10
        #     format="png"  # Can be 'png', 'jpg', 'svg', 'pdf'
        # )
        # print("Export result:", result)

        # For Jupyter notebooks, use:
        # viz_2d._show_in_jupyter()

        # For regular Python scripts or external browser:
        viz_2d.run()

    except Exception as e:
        print(f"Error starting 2D visualization app: {e}")
        import traceback

        traceback.print_exc()
