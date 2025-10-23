import base64
import io
import random
from typing import Optional, Union, List, Dict, Any

import dash
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from dash import dcc, html, Input, Output, State
from scipy.stats import binned_statistic_2d

from eelbrain import set_parc, NDVar, datasets


# Check if we're running in a Jupyter environment
def _is_jupyter_environment():
    """Check if we're running in a Jupyter notebook environment."""
    try:
        from IPython import get_ipython

        return get_ipython() is not None
    except ImportError:
        return False


JUPYTER_AVAILABLE = _is_jupyter_environment()


class EelbrainPlotly2DViz:
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
    show_max_only
        If True, butterfly plot shows only mean and max traces.
        If False, butterfly plot shows individual source traces, mean, and max.
        Default is False.
    arrow_threshold
        Threshold for displaying arrows in brain projections. Only arrows with
        magnitude greater than this value will be displayed. If None, all arrows
        are shown. If 'auto', uses 10% of the maximum magnitude as threshold.
        Default is None.
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

    Notes
    -----
    Expected input format follows the same pattern as :class:`plot.GlassBrain`:

    - For vector data: NDVar with dimensions ([case,] time, source, space)
    - For scalar data: NDVar with dimensions ([case,] time, source)
    - If case dimension present: mean across cases is plotted
    - If space dimension present: norm across space is plotted for butterfly plot
    """

    def __init__(
        self,
        y: Optional[NDVar] = None,
        region: Optional[str] = None,
        cmap: Union[str, List] = "YlOrRd",
        show_max_only: bool = False,
        arrow_threshold: Optional[Union[float, str]] = None,
        realtime: bool = False,
        layout_mode: str = "vertical",
        display_mode: str = "lyr",
    ):
        """Initialize the visualization app and load data."""
        # Use regular Dash with modern Jupyter integration
        self.app: dash.Dash = dash.Dash(__name__)

        # Initialize data attributes
        self.glass_brain_data: Optional[np.ndarray] = None  # (n_sources, 3, n_times)
        self.butterfly_data: Optional[np.ndarray] = None  # (n_sources, n_times)
        self.source_coords: Optional[np.ndarray] = None  # (n_sources, 3)
        self.time_values: Optional[np.ndarray] = None  # (n_times,)
        self.region_of_brain: Optional[str] = region  # Region of brain to visualize
        self.cmap: Union[str, List] = cmap  # Colorscale for heatmaps
        self.show_max_only: bool = show_max_only  # Control butterfly plot display mode
        # Threshold for displaying arrows
        self.arrow_threshold: Optional[Union[float, str]] = arrow_threshold
        self.is_jupyter_mode: bool = False  # Track if running in Jupyter mode
        self.realtime_mode_default = (
            ["realtime"] if realtime else []
        )  # Default state for real-time mode

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

        # Calculate global colormap range across all time points for consistent visualization
        self._calculate_global_colormap_range()

        # Setup app
        self._setup_layout()
        self._setup_callbacks()

    def _load_source_data(self, region: Optional[str] = None) -> None:
        """Load MNE sample data and prepare for 2D brain visualization.

        Parameters
        ----------
        region
            Brain region to load using aparc+aseg parcellation.
            If None, loads all regions.
        """
        # Load MNE sample data
        data_ds = datasets.get_mne_sample(src="vol", ori="vector")

        # Set parcellation if region is specified
        if region is not None:
            try:
                data_ds["src"] = set_parc(data_ds["src"], region)
                self.region_of_brain = region
            except Exception as e:
                print(f"Failed to apply parcellation {region}: {e}")
                print("Using full brain data instead")
                self.region_of_brain = "Full Brain"
        else:
            self.region_of_brain = "Full Brain"

        # Average over trials/cases
        src_ndvar = data_ds["src"].mean("case")

        # Extract coordinates and data
        self.glass_brain_data = src_ndvar.get_data(("source", "space", "time"))
        self.source_coords = src_ndvar.source.coordinates  # (n_sources, 3)
        self.time_values = src_ndvar.time.times

        # Store source space info
        self.source_space: Any = src_ndvar.source
        if hasattr(self.source_space, "parc"):
            self.parcellation: Any = self.source_space.parc
        else:
            self.parcellation: Optional[Any] = None

        # Compute norm for butterfly plot
        self.butterfly_data = np.linalg.norm(self.glass_brain_data, axis=1)

    def _load_ndvar_data(self, y: NDVar) -> None:
        """Load data from NDVar directly.

        Parameters
        ----------
        y
            Data with dimensions ([case,] time, source[, space]).
        """
        if y.has_case:
            y = y.mean("case")

        # Extract source dimension info
        source = y.get_dim("source")
        self.source_coords = source.coordinates
        self.time_values = y.time.times

        # Store source space info
        self.source_space: Any = source
        if hasattr(self.source_space, "parc"):
            self.parcellation: Any = self.source_space.parc
            self.region_of_brain = str(self.parcellation)
        else:
            self.parcellation: Optional[Any] = None
            self.region_of_brain = "Full Brain"

        # Handle space dimension (vector data)
        if y.has_dim("space"):
            # Extract 3D vector data
            self.glass_brain_data = y.get_data(
                ("source", "space", "time")
            )  # (n_sources, 3, n_times)
            # Compute norm for butterfly plot
            self.butterfly_data = np.linalg.norm(self.glass_brain_data, axis=1)
        else:
            # Scalar data - no space dimension
            self.glass_brain_data = y.get_data(
                ("source", "time")
            )  # (n_sources, n_times)
            self.butterfly_data = self.glass_brain_data.copy()
            # Expand to 3D for consistency (assuming scalar represents magnitude)
            # (n_sources, 1, n_times)
            self.glass_brain_data = self.glass_brain_data[:, np.newaxis, :]

    def _parse_display_mode(self, mode: str) -> List[str]:
        """Parse display_mode string into list of required brain views.

        Parameters
        ----------
        mode
            Display mode string (e.g., 'ortho', 'x', 'xz')

        Returns
        -------
        List[str]
            List of brain view types to generate
        """
        mode_mapping = {
            "ortho": ["sagittal", "coronal", "axial"],  # Traditional 3-view
            "x": ["sagittal"],
            "y": ["coronal"],
            "z": ["axial"],
            "xz": ["sagittal", "axial"],
            "yx": ["coronal", "sagittal"],
            "yz": ["coronal", "axial"],
            "l": ["left_hemisphere"],  # Left hemisphere view
            "r": ["right_hemisphere"],  # Right hemisphere view
            "lr": ["left_hemisphere", "right_hemisphere"],  # Both hemispheres
            "lzr": [
                "left_hemisphere",
                "axial",
                "right_hemisphere",
            ],  # Left + Axial + Right
            "lyr": [
                "left_hemisphere",
                "coronal",
                "right_hemisphere",
            ],  # Left + Coronal + Right (GlassBrain default)
            "lzry": [
                "left_hemisphere",
                "axial",
                "right_hemisphere",
                "coronal",
            ],  # Left + Axial + Right + Coronal
            "lyrz": [
                "left_hemisphere",
                "coronal",
                "right_hemisphere",
                "axial",
            ],  # Left + Coronal + Right + Axial
        }

        if mode in mode_mapping:
            return mode_mapping[mode]
        else:
            raise ValueError(f"Unsupported display_mode: {mode}")

    def _calculate_view_ranges(self) -> None:
        """Calculate fixed axis ranges for each brain view to prevent size changes.

        This ensures that brain plots maintain consistent size across all time points.
        """
        if self.source_coords is None:
            self.view_ranges = {}
            return

        coords = self.source_coords
        self.view_ranges = {}

        for view_name in self.brain_views:
            # Get the appropriate coordinate projections for each view
            if view_name == "axial":  # Z view (X vs Y)
                x_coords = coords[:, 0]
                y_coords = coords[:, 1]
            elif view_name == "sagittal":  # X view (Y vs Z)
                x_coords = coords[:, 1]
                y_coords = coords[:, 2]
            elif view_name == "coronal":  # Y view (X vs Z)
                x_coords = coords[:, 0]
                y_coords = coords[:, 2]
            elif view_name == "left_hemisphere":  # Left hemisphere (Y vs Z, X <= 0)
                # Include midline voxels (X=0) in left hemisphere view
                left_mask = coords[:, 0] <= 0
                if np.any(left_mask):
                    x_coords = -coords[left_mask, 1]  # Flipped Y
                    y_coords = coords[left_mask, 2]
                else:
                    x_coords = np.array([0])
                    y_coords = np.array([0])
            elif view_name == "right_hemisphere":  # Right hemisphere (Y vs Z, X >= 0)
                # Include midline voxels (X=0) in right hemisphere view
                right_mask = coords[:, 0] >= 0
                if np.any(right_mask):
                    x_coords = coords[right_mask, 1]
                    y_coords = coords[right_mask, 2]
                else:
                    x_coords = np.array([0])
                    y_coords = np.array([0])
            else:
                # Fallback for unknown views
                x_coords = coords[:, 0]
                y_coords = coords[:, 1]

            # Calculate ranges with some padding
            x_min, x_max = x_coords.min(), x_coords.max()
            y_min, y_max = y_coords.min(), y_coords.max()

            # Add 5% padding on each side
            x_range = x_max - x_min
            y_range = y_max - y_min
            x_padding = x_range * 0.05 if x_range > 0 else 0.01
            y_padding = y_range * 0.05 if y_range > 0 else 0.01

            self.view_ranges[view_name] = {
                "x": [x_min - x_padding, x_max + x_padding],
                "y": [y_min - y_padding, y_max + y_padding],
            }

    def _calculate_global_colormap_range(self) -> None:
        """Calculate global min/max activity across all time points for fixed colormap.

        This ensures consistent color mapping across time, making it easier to
        compare activity levels at different time points.
        """
        if self.glass_brain_data is None:
            self.global_vmin = 0.0
            self.global_vmax = 1.0
            return

        # Calculate activity magnitude across all time points
        if self.glass_brain_data.ndim == 3:  # Vector data (n_sources, 3, n_times)
            # Compute norm for each source at each time point
            all_magnitudes = np.linalg.norm(
                self.glass_brain_data, axis=1
            )  # (n_sources, n_times)
        else:  # Scalar data (n_sources, n_times)
            all_magnitudes = self.glass_brain_data

        # Get global min/max across all sources and all time points
        self.global_vmin = np.min(all_magnitudes)
        self.global_vmax = np.max(all_magnitudes)

        # Ensure we have a valid range (avoid zero range)
        if self.global_vmax - self.global_vmin < 1e-10:
            self.global_vmax = self.global_vmin + 1.0

    def _get_layout_config(self) -> Dict[str, Any]:
        """Get layout configuration based on layout_mode, display_mode and environment."""
        # Get number of brain views for this display mode
        num_views = len(self.brain_views)

        # Base configurations for different layout modes
        layout_configs = {
            "vertical": {
                "butterfly_width": "100%",
                "brain_width": self._get_brain_width_for_views(num_views, "vertical"),
                "brain_margin": {"jupyter": "1.5%", "browser": "0.5%"},
                "plot_height": {"jupyter": "250px", "browser": "450px"},
                "butterfly_height": {"jupyter": "300px", "browser": "400px"},
                "container_padding": {"jupyter": "2px", "browser": "5px"},
                "arrangement": "vertical",
            },
            "horizontal": {
                "butterfly_width": "35%",
                "brain_width": self._get_brain_width_for_views(num_views, "horizontal"),
                "brain_margin": {"jupyter": "0.3%", "browser": "0.3%"},
                "plot_height": {"jupyter": "300px", "browser": "350px"},
                "butterfly_height": {"jupyter": "300px", "browser": "350px"},
                "container_padding": {"jupyter": "5px", "browser": "10px"},
                "arrangement": "horizontal",
            },
        }

        base_config = layout_configs[self.layout_mode]
        env = "jupyter" if self.is_jupyter_mode else "browser"

        # Build final configuration
        config = {
            "butterfly_width": base_config["butterfly_width"],
            "brain_width": base_config["brain_width"][env],
            "brain_margin": base_config["brain_margin"][env],
            "plot_height": base_config["plot_height"][env],
            "butterfly_height": base_config["butterfly_height"][env],
            "container_padding": base_config["container_padding"][env],
            "arrangement": base_config["arrangement"],
            "num_views": num_views,
            "brain_views": self.brain_views,
        }

        # Special adjustments for 4-view modes (lzry, lyrz) in horizontal layout
        if (
            self.layout_mode == "horizontal"
            and self.display_mode in ["lzry", "lyrz"]
            and num_views == 4
        ):
            config["brain_margin"] = "0.02%"  # Very small margin
            config["butterfly_width"] = (
                "25%"  # Smaller butterfly plot: 25% + 4*16% + margins = ~90%
            )

        return config

    def _get_brain_width_for_views(
        self, num_views: int, layout_mode: str
    ) -> Dict[str, str]:
        """Calculate brain view width based on number of views and layout mode."""
        if layout_mode == "vertical":
            # In vertical mode, views are arranged horizontally below butterfly plot
            if num_views == 1:
                return {"jupyter": "98%", "browser": "98%"}
            elif num_views == 2:
                return {"jupyter": "48%", "browser": "48%"}
            else:  # 3 or more views
                return {"jupyter": "30%", "browser": "32%"}
        else:  # horizontal mode
            # In horizontal mode, views share space with butterfly plot
            # Special case for 4-view modes (lzry, lyrz) - arrange all in one row
            if self.display_mode in ["lzry", "lyrz"] and num_views == 4:
                return {
                    "jupyter": "16%",
                    "browser": "16%",
                }  # 4 views: 25% + 4*16% + small margins = ~90%
            elif num_views == 1:
                return {"jupyter": "60%", "browser": "60%"}
            elif num_views == 2:
                return {"jupyter": "30%", "browser": "30%"}
            else:  # 3 views (like lyr, lzr)
                return {"jupyter": "20%", "browser": "20%"}

    def _create_brain_view_containers(
        self,
        brain_plots: Dict[str, go.Figure],
        brain_height: str,
        brain_width: str,
        brain_margin: str,
    ) -> List:
        """Create dynamic brain view containers based on display_mode."""
        containers = []

        for view_name in self.brain_views:
            container = html.Div(
                [
                    dcc.Graph(
                        id=f"brain-{view_name}-plot",
                        figure=brain_plots[view_name],
                        style={"height": brain_height},
                    )
                ],
                style={
                    "width": brain_width,
                    "display": "inline-block",
                    "margin": brain_margin,
                },
            )
            containers.append(container)

        return containers

    def _create_brain_view_containers_horizontal(
        self,
        brain_plots: Dict[str, go.Figure],
        brain_height: str,
        brain_width: str,
        brain_margin: str,
    ) -> List:
        """Create dynamic brain view containers for horizontal layout."""
        containers = []

        for i, view_name in enumerate(self.brain_views):
            container = html.Div(
                [
                    dcc.Graph(
                        id=f"brain-{view_name}-plot",
                        figure=brain_plots[view_name],
                        style={"height": brain_height},
                    )
                ],
                style={
                    "width": brain_width,
                    "display": "inline-block",
                    "verticalAlign": "top",
                    "margin": brain_margin,
                    "padding": "0px",
                },
            )
            containers.append(container)

            # Add line break after every 2 views only for modes with more than 4 views
            # For 3-view modes (ortho, lyr, lzr) and 4-view modes (lzry, lyrz), keep all in one row
            if (
                len(self.brain_views) > 4
                and (i + 1) % 2 == 0
                and i < len(self.brain_views) - 1
            ):
                line_break = html.Div(style={"width": "100%", "height": "0px"})
                containers.append(line_break)

        return containers

    def _setup_layout(self) -> None:
        """Setup the Dash app layout based on layout_mode."""
        # Create initial figures
        initial_butterfly = self.create_butterfly_plot(0)
        initial_brain_plots = self.create_2d_brain_projections_plotly(0)

        # Get layout configuration
        config = self._get_layout_config()

        # Setup layout based on mode
        if self.layout_mode == "horizontal":
            self._setup_horizontal_layout(
                initial_butterfly, initial_brain_plots, config
            )
        else:
            self._setup_vertical_layout(initial_butterfly, initial_brain_plots, config)

    def _setup_vertical_layout(
        self, initial_butterfly, initial_brain_plots, config
    ) -> None:
        """Setup traditional vertical layout (butterfly top, brain views below)."""
        # Build butterfly and brain styles
        if self.layout_mode == "vertical":
            butterfly_style = {
                "width": config["butterfly_width"],
                "margin-bottom": "20px" if not self.is_jupyter_mode else "10px",
            }
        else:
            butterfly_style = {"width": config["butterfly_width"]}

        butterfly_graph_style = {"height": config["butterfly_height"]}
        brain_height = config["plot_height"]
        brain_width = config["brain_width"]
        brain_margin = config["brain_margin"]
        container_padding = config["container_padding"]

        self.app.layout = html.Div(
            [
                html.H1(
                    "Eelbrain Plotly 2D Brain Visualization",
                    style={"textAlign": "center", "margin": "10px 0"},
                ),
                # Real-time mode switch
                dcc.Checklist(
                    id="realtime-mode-switch",
                    options=[
                        {"label": "Real-time Update on Hover", "value": "realtime"}
                    ],
                    value=self.realtime_mode_default,
                    style={"textAlign": "center", "margin": "10px 0"},
                ),
                # Hidden stores for state management
                dcc.Store(id="selected-time-idx", data=0),
                dcc.Store(id="selected-source-idx", data=None),
                # Main content - arranged vertically
                html.Div(
                    [
                        # Top: Butterfly plot
                        html.Div(
                            [
                                dcc.Graph(
                                    id="butterfly-plot",
                                    figure=initial_butterfly,
                                    style=butterfly_graph_style,
                                )
                            ],
                            style=butterfly_style,
                        ),
                        # Bottom: 2D Brain projections using Plotly
                        html.Div(
                            [
                                # Dynamic brain view plots based on display_mode
                                html.Div(
                                    self._create_brain_view_containers(
                                        initial_brain_plots,
                                        brain_height,
                                        brain_width,
                                        brain_margin,
                                    ),
                                    style={"textAlign": "center"},
                                ),
                                # Status indicator
                                html.Div(
                                    id="update-status",
                                    children="Click on butterfly plot to update brain views",
                                    style={
                                        "textAlign": "center",
                                        "padding": "10px",
                                        "fontStyle": "italic",
                                        "color": "#666",
                                    },
                                ),
                            ],
                            style={"width": "100%"},
                        ),
                    ]
                ),
                # Info panel
                html.Div(
                    id="info-panel",
                    style={"clear": "both", "padding": "10px", "textAlign": "center"},
                ),
            ],
            style={"width": "100%", "height": "100%", "padding": container_padding},
        )

    def _setup_horizontal_layout(
        self, initial_butterfly, initial_brain_plots, config
    ) -> None:
        """Setup horizontal layout (butterfly left, brain views right)."""
        butterfly_graph_style = {"height": config["butterfly_height"]}
        brain_height = config["plot_height"]
        brain_width = config["brain_width"]
        brain_margin = config["brain_margin"]
        container_padding = config["container_padding"]

        self.app.layout = html.Div(
            [
                html.H1(
                    "Eelbrain Plotly 2D Brain Visualization - Horizontal Layout",
                    style={"textAlign": "center", "margin": "10px 0"},
                ),
                # Real-time mode switch
                dcc.Checklist(
                    id="realtime-mode-switch",
                    options=[
                        {"label": "Real-time Update on Hover", "value": "realtime"}
                    ],
                    value=self.realtime_mode_default,
                    style={"textAlign": "center", "margin": "10px 0"},
                ),
                # Hidden stores for state management
                dcc.Store(id="selected-time-idx", data=0),
                dcc.Store(id="selected-source-idx", data=None),
                # Main content - arranged horizontally
                html.Div(
                    [
                        # Left: Butterfly plot (compact)
                        html.Div(
                            [
                                dcc.Graph(
                                    id="butterfly-plot",
                                    figure=initial_butterfly,
                                    style=butterfly_graph_style,
                                )
                            ],
                            style={
                                "width": config["butterfly_width"],
                                "display": "inline-block",
                                "verticalAlign": "top",
                                "margin": brain_margin,
                                "padding": "0px",
                            },
                        )
                    ]
                    + self._create_brain_view_containers_horizontal(
                        initial_brain_plots, brain_height, brain_width, brain_margin
                    ),
                    style={"textAlign": "center"},
                ),
                # Status indicator
                html.Div(
                    id="update-status",
                    children="Click on butterfly plot to update brain views | Hover for real-time updates",
                    style={
                        "textAlign": "center",
                        "padding": "10px",
                        "fontStyle": "italic",
                        "color": "#666",
                    },
                ),
                # Info panel
                html.Div(
                    id="info-panel",
                    style={"clear": "both", "padding": "10px", "textAlign": "center"},
                ),
            ],
            style={"width": "100%", "height": "100%", "padding": container_padding},
        )

    def _setup_callbacks(self) -> None:
        """Setup all Dash callbacks."""

        @self.app.callback(
            Output("butterfly-plot", "figure"), Input("selected-time-idx", "data")
        )
        def update_butterfly(time_idx: int) -> go.Figure:
            if time_idx is None:
                time_idx = 0
            return self.create_butterfly_plot(time_idx)

        # Dynamic brain plot outputs based on display_mode
        brain_outputs = [
            Output(f"brain-{view_name}-plot", "figure")
            for view_name in self.brain_views
        ]

        @self.app.callback(
            brain_outputs,
            Input("selected-time-idx", "data"),
            Input("selected-source-idx", "data"),
        )
        def update_brain_projections(time_idx: int, source_idx: int):
            if time_idx is None:
                time_idx = 0

            try:
                brain_plots = self.create_2d_brain_projections_plotly(
                    time_idx, source_idx
                )
                return tuple(brain_plots[view_name] for view_name in self.brain_views)
            except Exception:
                # Return empty plots on error
                empty_fig = go.Figure()
                empty_fig.add_annotation(
                    text="Error loading brain data",
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                )
                return tuple(empty_fig for _ in self.brain_views)

        @self.app.callback(
            Output("selected-time-idx", "data"),
            Output("selected-source-idx", "data"),
            Output("realtime-mode-switch", "value"),
            Input("butterfly-plot", "clickData"),
            Input("butterfly-plot", "hoverData"),
            State("realtime-mode-switch", "value"),
        )
        def handle_butterfly_interaction(
            click_data: Optional[Dict[str, Any]],
            hover_data: Optional[Dict[str, Any]],
            realtime_value: List[str],
        ) -> tuple[Any, Any, Any]:
            """Handle user interaction with butterfly plot."""
            ctx = dash.callback_context
            if not ctx.triggered or self.time_values is None:
                return dash.no_update, dash.no_update, dash.no_update

            triggered_id = ctx.triggered[0]["prop_id"]
            is_realtime = realtime_value and "realtime" in realtime_value

            # Handle hover events in real-time mode
            if "hoverData" in triggered_id and is_realtime:
                if not hover_data:
                    return dash.no_update, dash.no_update, dash.no_update

                try:
                    point = hover_data["points"][0]
                    hover_time = point["x"]
                    time_idx = np.argmin(np.abs(self.time_values - hover_time))
                    # Do not update source index on hover to avoid frantic updates
                    return time_idx, dash.no_update, dash.no_update
                except (KeyError, IndexError, TypeError):
                    return dash.no_update, dash.no_update, dash.no_update

            # Handle click events
            if "clickData" in triggered_id:
                if not click_data:
                    return dash.no_update, dash.no_update, dash.no_update

                try:
                    point = click_data["points"][0]
                    clicked_time = point["x"]
                    time_idx = np.argmin(np.abs(self.time_values - clicked_time))
                    source_idx = point.get("customdata", None)

                    # If in real-time mode, a click will select the time and disable
                    # real-time mode for focused inspection
                    new_realtime_value = [] if is_realtime else dash.no_update

                    return time_idx, source_idx, new_realtime_value
                except (KeyError, IndexError, TypeError):
                    return dash.no_update, dash.no_update, dash.no_update

            return dash.no_update, dash.no_update, dash.no_update

        @self.app.callback(
            Output("update-status", "children"),
            Output("update-status", "style"),
            Input("selected-time-idx", "data"),
        )
        def update_status(time_idx: int) -> tuple[str, Dict[str, str]]:
            if (
                time_idx is not None
                and self.time_values is not None
                and 0 <= time_idx < len(self.time_values)
            ):
                time_val = self.time_values[time_idx]
                status_text = (
                    f"Brain views updated for time: {time_val:.3f}s (index {time_idx})"
                )
                status_style = {
                    "textAlign": "center",
                    "padding": "10px",
                    "fontStyle": "italic",
                    "color": "#2E8B57",
                    "backgroundColor": "#F0FFF0",
                }
            else:
                status_text = "Click on butterfly plot to update brain views"
                status_style = {
                    "textAlign": "center",
                    "padding": "10px",
                    "fontStyle": "italic",
                    "color": "#666",
                }

            return status_text, status_style

        @self.app.callback(
            Output("info-panel", "children"),
            Input("selected-time-idx", "data"),
            Input("selected-source-idx", "data"),
        )
        def update_info(time_idx: int, source_idx: int) -> html.P:
            info = []

            if (
                self.time_values is not None
                and time_idx is not None
                and 0 <= time_idx < len(self.time_values)
            ):
                info.append(
                    f"Time: {self.time_values[time_idx]:.3f} s (index {time_idx})"
                )

            if (
                source_idx is not None
                and self.source_coords is not None
                and 0 <= source_idx < len(self.source_coords)
            ):
                coord = self.source_coords[source_idx]
                info.append(f"Selected source: {source_idx}")
                info.append(
                    f"Coordinates: ({coord[0]:.3f}, {coord[1]:.3f}, {coord[2]:.3f}) m"
                )

            result = (
                html.P(" | ".join(info))
                if info
                else html.P("Click on the plots to interact")
            )
            return result

    def create_butterfly_plot(self, selected_time_idx: int = 0) -> go.Figure:
        """Create butterfly plot figure."""
        fig = go.Figure()

        if self.butterfly_data is None or self.time_values is None:
            fig.add_annotation(
                text="No data loaded",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )
            return fig

        n_sources, n_times = self.butterfly_data.shape

        # Auto-scale data for visibility
        data_to_plot = self.butterfly_data.copy()
        scale_factor = 1.0
        unit_suffix = ""

        max_abs_val = np.max(np.abs(data_to_plot))
        if max_abs_val < 1e-10:
            scale_factor = 1e12
            unit_suffix = " (pA)"
        elif max_abs_val < 1e-6:
            scale_factor = 1e9
            unit_suffix = " (nA)"
        elif max_abs_val < 1e-3:
            scale_factor = 1e6
            unit_suffix = " (µA)"

        data_to_plot = data_to_plot * scale_factor

        # Calculate y-axis range for layout and clickable background
        y_min, y_max = data_to_plot.min(), data_to_plot.max()
        y_margin = (y_max - y_min) * 0.1 if y_max != y_min else 1

        # Add invisible clickable markers FIRST so they're behind other traces
        # Create a dense grid of invisible markers to capture clicks anywhere
        n_rows = 5  # Number of rows of markers to cover the plot vertically
        y_positions = np.linspace(y_min - y_margin / 2, y_max + y_margin / 2, n_rows)

        # Create markers at multiple vertical positions
        x_grid = np.tile(self.time_values, n_rows)
        y_grid = np.repeat(y_positions, len(self.time_values))

        fig.add_trace(
            go.Scatter(
                x=x_grid,
                y=y_grid,
                mode="markers",
                marker=dict(
                    size=35,  # Large invisible markers
                    color="rgba(0,0,0,0.001)",  # Nearly transparent (but not completely)
                    line=dict(width=0),
                ),
                showlegend=False,
                hovertemplate="Time: %{x:.3f}s<extra></extra>",  # Show time on hover
                name="clickable_background",
            )
        )

        # Add individual source traces only if show_max_only is False
        if not self.show_max_only:
            # Plot subset of traces for performance
            max_traces = 20
            step = max(1, n_sources // max_traces)
            indices_to_plot = list(range(0, n_sources, step))

            # Add individual traces
            for idx, i in enumerate(indices_to_plot[:10]):
                trace_data = data_to_plot[i, :]

                fig.add_trace(
                    go.Scatter(
                        x=self.time_values,
                        y=trace_data,
                        mode="lines",
                        name=f"Source {i}",
                        customdata=[i] * n_times,
                        showlegend=(idx < 3),
                        opacity=0.6,
                        line=dict(width=1),
                    )
                )

        # Add mean trace (always shown)
        mean_activity = np.mean(data_to_plot, axis=0)
        fig.add_trace(
            go.Scatter(
                x=self.time_values,
                y=mean_activity,
                mode="lines",
                name="Mean Activity",
                line=dict(color="red", width=3),
                showlegend=True,
            )
        )

        # Add max trace (always shown)
        max_activity = np.max(data_to_plot, axis=0)
        fig.add_trace(
            go.Scatter(
                x=self.time_values,
                y=max_activity,
                mode="lines",
                name="Max Activity",
                line=dict(color="darkblue", width=3),
                showlegend=True,
            )
        )

        # Add vertical line for selected time
        if 0 <= selected_time_idx < len(self.time_values):
            selected_time = self.time_values[selected_time_idx]
            fig.add_vline(
                x=selected_time, line_width=2, line_dash="dash", line_color="blue"
            )

        # Update title based on display mode
        if self.show_max_only:
            title_text = (
                f"Source Activity Time Series - Mean & Max Only ({n_sources} sources)"
            )
        else:
            title_text = (
                f"Source Activity Time Series (showing subset of {n_sources} sources)"
            )

        # Adjust layout based on mode
        if self.is_jupyter_mode:
            height = 300
            margin = dict(l=40, r=40, t=60, b=40)  # Reduced margins for Jupyter
        else:
            height = 500
            margin = dict(l=40, r=40, t=60, b=40)  # Standard margins

        fig.update_layout(
            title=title_text,
            xaxis_title="Time (s)",
            yaxis_title=f"Activity{unit_suffix}",
            yaxis=dict(range=[y_min - y_margin, y_max + y_margin]),
            hovermode="closest",
            height=height,
            margin=margin,
            showlegend=True,
            # Enable clicking on the plot area
            clickmode="event+select",
        )

        return fig

    def create_2d_brain_projections_plotly(
        self, time_idx: int = 0, source_idx: Optional[int] = None
    ) -> Dict[str, go.Figure]:
        """Create 2D brain projections using Plotly scatter plots."""
        if (
            self.glass_brain_data is None
            or self.source_coords is None
            or self.time_values is None
        ):
            placeholder_fig = go.Figure()
            placeholder_fig.add_annotation(
                text="No brain data",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )
            return {view: placeholder_fig for view in self.brain_views}

        try:
            # Get time slice of data
            if time_idx >= len(self.time_values):
                time_idx = 0

            time_value = self.time_values[time_idx]

            # Get activity at this time point
            if self.glass_brain_data.ndim == 3:  # (n_sources, 3, n_times)
                time_activity = self.glass_brain_data[:, :, time_idx]  # (n_sources, 3)
                activity_magnitude = np.linalg.norm(
                    time_activity, axis=1
                )  # (n_sources,)
            else:  # (n_sources, n_times)
                activity_magnitude = self.glass_brain_data[:, time_idx]

            # Use global min/max for consistent colormap across all time points
            # This allows intuitive comparison of activity levels across time
            global_min = self.global_vmin
            global_max = self.global_vmax

            # Create brain projections
            brain_plots = {}
            views = self.brain_views

            for i, view_name in enumerate(views):
                try:
                    # Only show colorbar on the last view
                    show_colorbar = i == len(views) - 1
                    brain_fig = self._create_plotly_brain_projection(
                        view_name,
                        self.source_coords,
                        activity_magnitude,
                        time_value,
                        source_idx,
                        show_colorbar=show_colorbar,
                        zmin=global_min,
                        zmax=global_max,
                    )
                    brain_plots[view_name] = brain_fig
                except Exception:
                    brain_plots[view_name] = go.Figure()
                    brain_plots[view_name].add_annotation(
                        text=f"Error: {view_name}",
                        xref="paper",
                        yref="paper",
                        x=0.5,
                        y=0.5,
                        showarrow=False,
                    )

            return brain_plots

        except Exception:
            placeholder_fig = go.Figure()
            placeholder_fig.add_annotation(
                text="No brain data",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )
            return {
                "axial": placeholder_fig,
                "sagittal": placeholder_fig,
                "coronal": placeholder_fig,
            }

    def _create_plotly_brain_projection(
        self,
        view_name: str,
        coords: np.ndarray,
        activity: np.ndarray,
        time_value: float,
        selected_source: Optional[int] = None,
        show_colorbar: bool = True,
        zmin: float = None,
        zmax: float = None,
    ) -> go.Figure:
        """Create a Plotly plot for a specific brain view with vector arrows."""
        # Show all data without filtering
        active_coords = coords
        active_activity = activity
        active_indices = np.arange(len(coords))

        # Create Plotly figure
        fig = go.Figure()

        # Get time index for vector components
        time_idx = np.argmin(np.abs(self.time_values - time_value))

        # Get vector components for active sources
        if self.glass_brain_data is not None and len(active_indices) > 0:
            # (n_active, 3) or (n_active, 1)
            active_vectors = self.glass_brain_data[active_indices, :, time_idx]
        else:
            active_vectors = None

        # Check if we have vector data (3D) or scalar data (1D)
        has_vector_data = active_vectors is not None and active_vectors.shape[1] == 3

        # Project to 2D based on view
        if view_name == "axial":  # Z view (X vs Y)
            x_coords = active_coords[:, 0]
            y_coords = active_coords[:, 1]
            if has_vector_data:
                u_vectors = active_vectors[:, 0]  # X components
                v_vectors = active_vectors[:, 1]  # Y components
            title = None
        elif view_name == "sagittal":  # X view (Y vs Z)
            x_coords = active_coords[:, 1]
            y_coords = active_coords[:, 2]
            if has_vector_data:
                u_vectors = active_vectors[:, 1]  # Y components
                v_vectors = active_vectors[:, 2]  # Z components
            title = None
        elif view_name == "coronal":  # Y view (X vs Z)
            x_coords = active_coords[:, 0]
            y_coords = active_coords[:, 2]
            if has_vector_data:
                u_vectors = active_vectors[:, 0]  # X components
                v_vectors = active_vectors[:, 2]  # Z components
            title = None
        elif (
            view_name == "left_hemisphere"
        ):  # Left hemisphere lateral view (Y vs Z, X <= 0)
            # Filter for left hemisphere (include midline voxels with X=0)
            left_mask = active_coords[:, 0] <= 0
            if np.any(left_mask):
                active_coords = active_coords[left_mask]
                active_activity = active_activity[left_mask]
                active_indices = active_indices[left_mask]
                if has_vector_data:
                    active_vectors = active_vectors[left_mask]

            # For left hemisphere, flip Y coordinates to match neuroimaging convention
            x_coords = -active_coords[:, 1]  # Negative Y coordinates (flipped)
            y_coords = active_coords[:, 2]  # Z coordinates
            if has_vector_data:
                u_vectors = -active_vectors[:, 1]  # Negative Y components (flipped)
                v_vectors = active_vectors[:, 2]  # Z components
            title = "Left Hemisphere"
        elif (
            view_name == "right_hemisphere"
        ):  # Right hemisphere lateral view (Y vs Z, X >= 0)
            # Filter for right hemisphere (include midline voxels with X=0)
            right_mask = active_coords[:, 0] >= 0
            if np.any(right_mask):
                active_coords = active_coords[right_mask]
                active_activity = active_activity[right_mask]
                active_indices = active_indices[right_mask]
                if has_vector_data:
                    active_vectors = active_vectors[right_mask]

            x_coords = active_coords[:, 1]  # Y coordinates
            y_coords = active_coords[:, 2]  # Z coordinates
            if has_vector_data:
                u_vectors = active_vectors[:, 1]  # Y components
                v_vectors = active_vectors[:, 2]  # Z components
            title = "Right Hemisphere"
        else:
            # Fallback for unknown view types
            x_coords = active_coords[:, 0]
            y_coords = active_coords[:, 1]
            if has_vector_data:
                u_vectors = active_vectors[:, 0]
                v_vectors = active_vectors[:, 1]
            title = f"Unknown View: {view_name}"

        if len(active_coords) > 0:
            # Create data-driven grid using unique coordinate values
            unique_x = np.unique(x_coords)
            unique_y = np.unique(y_coords)

            # Create grid boundaries around each unique coordinate point
            x_spacing = np.diff(unique_x).min() / 2 if len(unique_x) > 1 else 0.001
            y_spacing = np.diff(unique_y).min() / 2 if len(unique_y) > 1 else 0.001

            # Create grid boundaries: small intervals around each data point
            x_edges = []
            for i, x_val in enumerate(unique_x):
                if i == 0:
                    x_edges.append(x_val - x_spacing)
                x_edges.append(x_val + x_spacing)

            y_edges = []
            for i, y_val in enumerate(unique_y):
                if i == 0:
                    y_edges.append(y_val - y_spacing)
                y_edges.append(y_val + y_spacing)

            x_edges = np.array(x_edges)
            y_edges = np.array(y_edges)

            # Use binned_statistic_2d to get maximum value per bin
            H_max, x_edges_used, y_edges_used, _ = binned_statistic_2d(
                x_coords,
                y_coords,
                active_activity,
                statistic="max",  # Take maximum value in each bin
                bins=[x_edges, y_edges],
            )

            # Use grid center points for display
            x_centers = (x_edges_used[:-1] + x_edges_used[1:]) / 2
            y_centers = (y_edges_used[:-1] + y_edges_used[1:]) / 2

            # Set NaN values to NaN to make them transparent in heatmap
            # binned_statistic_2d returns NaN for empty bins
            H_display = H_max.copy()  # Use maximum value per bin

            # Add heatmap trace
            fig.add_trace(
                go.Heatmap(
                    x=x_centers,
                    y=y_centers,
                    z=H_display.T,  # Transpose to match Plotly orientation
                    colorscale=self.cmap,
                    colorbar=dict(title="") if show_colorbar else None,
                    showscale=show_colorbar,
                    zmin=zmin,
                    zmax=zmax,
                    hovertemplate="Activity: %{z:.2e}<extra></extra>",
                )
            )

            # Update layout to have white background
            fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")

            # Add vector arrows if we have vector data (not scalar data)
            if has_vector_data:
                arrow_scale = 0.025  # Scale arrows for visibility - increased for better visibility

                # Calculate arrow magnitudes for filtering
                arrow_magnitudes = np.linalg.norm(active_vectors, axis=1)

                # Determine threshold for showing arrows
                if self.arrow_threshold is None:
                    # Show all arrows
                    show_arrow_mask = np.ones(len(active_vectors), dtype=bool)
                elif self.arrow_threshold == "auto":
                    # Use 10% of maximum magnitude as threshold
                    threshold_value = 0.1 * np.max(arrow_magnitudes)
                    show_arrow_mask = arrow_magnitudes > threshold_value
                else:
                    # Use specified threshold
                    threshold_value = float(self.arrow_threshold)
                    show_arrow_mask = arrow_magnitudes > threshold_value

                # Group sources by position and select the one with maximum magnitude
                # for each position
                position_to_max_idx = {}

                # Remove performance limit, check all source points
                for i in range(len(active_coords)):
                    # Only consider arrows that meet the threshold criteria
                    if not show_arrow_mask[i]:
                        continue

                    # Create position key (rounded to avoid floating point precision
                    # issues)
                    pos_key = (round(x_coords[i], 6), round(y_coords[i], 6))

                    # If this position hasn't been seen, or current arrow has larger
                    # magnitude
                    if (
                        pos_key not in position_to_max_idx
                        or arrow_magnitudes[i]
                        > arrow_magnitudes[position_to_max_idx[pos_key]]
                    ):
                        position_to_max_idx[pos_key] = i

                # OPTIMIZED BATCH ARROW RENDERING
                if position_to_max_idx:
                    # Extract arrow data for selected sources
                    selected_indices = list(position_to_max_idx.values())
                    arrow_x = x_coords[selected_indices]
                    arrow_y = y_coords[selected_indices]
                    arrow_u = u_vectors[selected_indices]
                    arrow_v = v_vectors[selected_indices]

                    # Create all arrows as 2 traces instead of 179+ individual
                    # annotations
                    self._create_batch_arrows(
                        fig, arrow_x, arrow_y, arrow_u, arrow_v, arrow_scale
                    )

            # Highlight selected source if provided
            if selected_source is not None and selected_source in active_indices:
                selected_pos = np.where(active_indices == selected_source)[0]
                if len(selected_pos) > 0:
                    pos = selected_pos[0]
                    fig.add_trace(
                        go.Scatter(
                            x=[x_coords[pos]],
                            y=[y_coords[pos]],
                            mode="markers",
                            marker=dict(
                                size=12,
                                color="cyan",
                                symbol="circle-open",
                                line=dict(width=3),
                            ),
                            name="Selected Source",
                            showlegend=False,
                            hovertemplate="SELECTED SOURCE<extra></extra>",
                        )
                    )

                    # Highlight selected source arrow if vectors available
                    if has_vector_data:
                        # Check if the selected source arrow meets the threshold
                        selected_arrow_magnitude = np.linalg.norm(active_vectors[pos])
                        show_selected_arrow = True

                        if self.arrow_threshold is not None:
                            if self.arrow_threshold == "auto":
                                threshold_value = 0.1 * np.max(
                                    np.linalg.norm(active_vectors, axis=1)
                                )
                            else:
                                threshold_value = float(self.arrow_threshold)
                            show_selected_arrow = (
                                selected_arrow_magnitude > threshold_value
                            )

                        if show_selected_arrow:
                            x_start = x_coords[pos]
                            y_start = y_coords[pos]

                            # Add highlighted arrow for selected source (optimized)
                            self._create_batch_arrows(
                                fig,
                                np.array([x_start]),
                                np.array([y_start]),
                                np.array([u_vectors[pos]]),
                                np.array([v_vectors[pos]]),
                                arrow_scale,
                                color="cyan",
                                width=2,
                                size=1.0,
                            )
        else:
            # Add annotation if no active sources
            fig.add_annotation(
                text=f"No active sources for {view_name} view",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )

        # Update layout based on mode
        if self.is_jupyter_mode:
            height = 250
            margin = dict(l=30, r=30, t=30, b=30)  # Reduced margins for Jupyter
        else:
            height = 450
            margin = dict(l=40, r=40, t=40, b=40)  # Standard margins

        # Get fixed axis ranges for this view to prevent size changes across time
        axis_ranges = self.view_ranges.get(view_name, {})
        x_range = axis_ranges.get("x", None)
        y_range = axis_ranges.get("y", None)

        fig.update_layout(
            title=title,
            xaxis=dict(
                scaleanchor="y",
                scaleratio=1,
                showticklabels=False,
                title="",
                range=x_range,  # Fixed range to prevent size changes
            ),
            # Equal aspect ratio, hide labels
            yaxis=dict(
                showticklabels=False,
                title="",
                range=y_range,  # Fixed range to prevent size changes
            ),
            height=height,
            margin=margin,
            showlegend=False,
        )

        return fig

    def _create_batch_arrows(
        self,
        fig: go.Figure,
        x_coords: np.ndarray,
        y_coords: np.ndarray,
        u_vectors: np.ndarray,
        v_vectors: np.ndarray,
        arrow_scale: float,
        color: str = "black",
        width: int = 1,
        size: float = 0.8,
    ) -> None:
        """Create all arrows using batch method."""

        if len(x_coords) == 0:
            return

        # Calculate all endpoints at once (vectorized)
        x_ends = x_coords + u_vectors * arrow_scale
        y_ends = y_coords + v_vectors * arrow_scale

        # Create all arrow lines as a single trace
        # Use None to separate individual line segments
        x_lines = []
        y_lines = []
        for i in range(len(x_coords)):
            x_lines.extend([x_coords[i], x_ends[i], None])
            y_lines.extend([y_coords[i], y_ends[i], None])

        # Add all arrow lines as single trace (instead of 179+ individual annotations)
        fig.add_trace(
            go.Scatter(
                x=x_lines,
                y=y_lines,
                mode="lines",
                line=dict(color=color, width=width),
                opacity=0.6,
                showlegend=False,
                hoverinfo="skip",
                name="arrow_lines",
            )
        )

        # Calculate arrow angles for proper arrowhead rotation
        angles = np.degrees(np.arctan2(v_vectors, u_vectors))
        magnitudes = np.sqrt(u_vectors**2 + v_vectors**2)

        # Add all arrowheads as single trace (instead of 179+ individual annotations)
        fig.add_trace(
            go.Scatter(
                x=x_ends,
                y=y_ends,
                mode="markers",
                marker=dict(
                    symbol="triangle-right",
                    size=6 * size,  # Scale the marker size
                    color=color,
                    opacity=0.8,
                    angle=angles,  # Rotate markers to match vector direction
                ),
                showlegend=False,
                hovertemplate="Vector magnitude: %{customdata:.3f}<extra></extra>",
                customdata=magnitudes,
                name="arrow_heads",
            )
        )

    def _fig_to_base64(self, fig: plt.Figure) -> str:
        """Convert matplotlib figure to base64 string for Dash display."""
        try:
            # Save figure to bytes buffer
            img_buffer = io.BytesIO()
            fig.savefig(
                img_buffer,
                format="png",
                bbox_inches="tight",
                dpi=100,
                facecolor="white",
            )
            img_buffer.seek(0)

            # Convert to base64 string
            img_base64 = base64.b64encode(img_buffer.read()).decode("utf-8")
            img_buffer.close()

            return f"data:image/png;base64,{img_base64}"

        except Exception:
            return self._create_placeholder_image("Conversion Error")

    def _create_placeholder_image(self, text: str = "No Data") -> str:
        """Create a placeholder image when brain plotting fails."""

        # Create a simple matplotlib figure
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(
            0.5,
            0.5,
            text,
            ha="center",
            va="center",
            fontsize=16,
            transform=ax.transAxes,
        )
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        # Convert to base64
        img_base64 = self._fig_to_base64(fig)
        plt.close(fig)

        return img_base64

    def run(
        self,
        port: Optional[int] = None,
        debug: bool = True,
        mode: str = "external",
        width: int = 1200,
        height: int = 900,
    ) -> None:
        """Run the Dash app with Jupyter integration support.

        Parameters
        ----------
        port
            Port number for the server. If None, uses random port.
        debug
            Enable debug mode. Default is True.
        mode
            Display mode. Options:
            - 'external': Open in separate browser window (default)
            - 'inline': Embed directly in Jupyter notebook (modern Dash)
            - 'jupyterlab': Open in JupyterLab tab (modern Dash)
        width
            Display width in pixels for Jupyter integration. Default is 1200.
        height
            Display height in pixels for Jupyter integration. Default is 900.
        """
        if port is None:
            port = random.randint(8001, 9001)

        if JUPYTER_AVAILABLE and mode in ["inline", "jupyterlab"]:
            print(
                "\nStarting 2D Brain Visualization with modern Dash Jupyter integration..."
            )
            print(f"Mode: {mode}, Size: {width}x{height}px")

            # Use modern Dash Jupyter integration
            self.app.run(debug=debug, port=port, mode=mode, width=width, height=height)
        else:
            print(f"\nStarting 2D Brain Visualization Dash app on port {port}...")
            print(f"Open http://127.0.0.1:{port}/ in your browser")
            if not JUPYTER_AVAILABLE and mode != "external":
                print(
                    "Note: Jupyter environment not detected, using external browser mode"
                )
            print()

            self.app.run(debug=debug, port=port)

    def show_in_jupyter(
        self, width: int = 1200, height: int = 900, debug: bool = False
    ) -> None:
        """Convenience method to display the visualization inline in Jupyter notebooks.

        Parameters
        ----------
        width
            Display width in pixels. Default is 1200.
        height
            Display height in pixels. Default is 900.
        debug
            Enable debug mode. Default is False for cleaner output.

        Examples
        --------
        Basic usage in Jupyter:
        >>> viz = EelbrainPlotly2DViz()
        >>> viz.show_in_jupyter()

        Custom sizing:
        >>> viz.show_in_jupyter(width=1400, height=1000)
        """
        if not JUPYTER_AVAILABLE:
            print("Warning: Jupyter environment not detected.")
            print("Falling back to external browser mode...")
            self.run(debug=debug)
            return

        # Set Jupyter mode and rebuild layout with Jupyter-specific styles
        self.is_jupyter_mode = True
        self._setup_layout()  # Rebuild layout with Jupyter styles

        self.run(mode="inline", width=width, height=height, debug=debug)

    def export_images(
        self,
        output_dir: str = "./images",
        time_idx: Optional[int] = None,
        format: str = "png",
    ) -> Dict[str, Any]:
        """Export current plots as image files.

        Parameters
        ----------
        output_dir
            Directory to save image files. Default is "./images".
        time_idx
            Time index to export. If None, uses 0.
        format
            Image format ('png', 'jpg', 'svg', 'pdf'). Default is 'png'.

        Returns
        -------
        dict
            Dictionary with exported file paths and status.
        """
        import os
        from datetime import datetime

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Use provided time_idx or default to 0
        if time_idx is None:
            time_idx = 0

        # Timestamp for unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        exported_files = {}

        try:
            # Export butterfly plot
            butterfly_fig = self.create_butterfly_plot(time_idx)
            butterfly_path = os.path.join(
                output_dir, f"butterfly_plot_{timestamp}.{format}"
            )
            butterfly_fig.write_image(butterfly_path, width=1200, height=600)
            exported_files["butterfly_plot"] = butterfly_path

            # Export brain projections
            brain_plots = self.create_2d_brain_projections_plotly(time_idx)

            for view_name, fig in brain_plots.items():
                brain_path = os.path.join(
                    output_dir, f"{view_name}_view_{timestamp}.{format}"
                )
                fig.write_image(brain_path, width=800, height=600)
                exported_files[f"{view_name}_view"] = brain_path

            print(
                f"✓ Successfully exported {len(exported_files)} image files to {output_dir}"
            )
            for file_type, path in exported_files.items():
                print(f"  - {file_type}: {path}")

            return {"status": "success", "files": exported_files}

        except Exception as e:
            error_msg = f"Image export failed: {str(e)}"
            print(f"✗ {error_msg}")
            return {"status": "error", "message": error_msg, "files": exported_files}


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

        # Method 1: Pass data directly using y parameter (same as plot.GlassBrain)
        # from eelbrain import datasets
        #
        # # Load your data - NDVar with dimensions ([case,] time, source[, space])
        # data_ds = datasets.get_mne_sample(src='vol', ori='vector')
        # y = data_ds['src']  # NDVar with dimensions (case, time, source, space)
        #
        # # Create visualization with your data
        # viz_2d = EelbrainPlotly2DViz(
        #     y=y,  # Pass NDVar directly - same format as plot.GlassBrain
        #     cmap=cmap,
        #     show_max_only=False,
        #     arrow_threshold='auto'  # Only show significant arrows
        # )

        # Method 2: Use default MNE sample data with region filtering
        viz_2d = EelbrainPlotly2DViz(
            region="aparc+aseg",
            cmap="Reds",
            show_max_only=False,
            arrow_threshold=None,  # Show all arrows
            layout_mode="vertical",
            display_mode="ortho",
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
        # viz_2d.show_in_jupyter(width=1200, height=900)

        # For regular Python scripts or external browser:
        viz_2d.run()

    except Exception as e:
        print(f"Error starting 2D visualization app: {e}")
        import traceback

        traceback.print_exc()