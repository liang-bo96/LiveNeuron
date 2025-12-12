"""
Layout Builder Module - Responsible for arranging UI components.

This module provides the LayoutBuilder interface, concrete layout strategies,
and the LayoutBuilderHelper following the Open/Closed Principle.

New layout strategies can be added by:
1. Inheriting from LayoutBuilder and implementing the build() method
2. Registering the new layout with register_layout()

Example
-------
>>> from eelbrain_plotly_viz import LayoutBuilder, register_layout
>>>
>>> class GridLayout(LayoutBuilder):
...     def build(self, app):
...         # Custom layout implementation
...         pass
>>>
>>> register_layout("grid", GridLayout())
>>> viz = EelbrainPlotly2DViz(layout_mode="grid")
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import plotly.graph_objects as go
from dash import dcc, html

if TYPE_CHECKING:
    from .viz_2d import EelbrainPlotly2DViz


# =============================================================================
# LayoutBuilder Interface and Implementations
# =============================================================================


class LayoutBuilder(ABC):
    """Abstract interface for layout strategies.

    Layout strategies control how UI components (butterfly plot, brain views)
    are arranged in the Dash application. New layouts can be created by
    inheriting this class and implementing the build() method.

    To create a custom layout:
    1. Inherit from LayoutBuilder
    2. Implement the build(app) method
    3. Register with register_layout("name", YourLayout())
    4. Use with EelbrainPlotly2DViz(layout_mode="name")

    Methods
    -------
    build(app)
        Build and apply the layout to the visualization app.

    Example
    -------
    >>> class CompactLayout(LayoutBuilder):
    ...     def build(self, app):
    ...         # Access app.app.layout to set Dash layout
    ...         # Access app._plot_factory._create_butterfly_plot() for butterfly figure
    ...         # Access app._plot_factory._create_2d_brain_projections_plotly() for brain figures
    ...         pass
    """

    @abstractmethod
    def build(self, app: "EelbrainPlotly2DViz") -> None:
        """Build and apply layout to the visualization application.

        Parameters
        ----------
        app
            The EelbrainPlotly2DViz instance to configure layout for.
            Access app.app.layout to set the Dash layout.
        """
        pass

    def _get_layout_config(self, app: "EelbrainPlotly2DViz") -> Dict[str, Any]:
        """Get base layout configuration.

        Parameters
        ----------
        app
            The visualization app instance.

        Returns
        -------
        Dict[str, Any]
            Configuration dictionary with layout parameters.
        """
        num_views = len(app.brain_views)
        env = "jupyter" if app.is_jupyter_mode else "browser"
        return {"num_views": num_views, "env": env, "brain_views": app.brain_views}

    def _create_brain_view_containers(
        self,
        app: "EelbrainPlotly2DViz",
        brain_plots: Dict[str, go.Figure],
        brain_height: str,
        brain_width: str,
        brain_margin: str,
    ) -> List:
        """Create dynamic brain view containers based on display_mode.

        Parameters
        ----------
        app
            The visualization app instance.
        brain_plots
            Dictionary mapping view names to Plotly figures.
        brain_height
            CSS height string for brain plots.
        brain_width
            CSS width string for brain plot containers.
        brain_margin
            CSS margin string for brain plot containers.

        Returns
        -------
        List
            List of Dash HTML Div components containing the brain plots.
        """
        containers = []

        for view_name in app.brain_views:
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


class VerticalLayout(LayoutBuilder):
    """Vertical layout strategy - butterfly plot on top, brain views below.

    This is the traditional layout arrangement with the time series plot
    at the top and brain projections arranged horizontally below.
    """

    def build(self, app: "EelbrainPlotly2DViz") -> None:
        """Build vertical layout for the visualization app.

        Parameters
        ----------
        app
            The EelbrainPlotly2DViz instance to configure.
        """
        config = self._get_vertical_config(app)
        app._current_layout_config = config

        # Extract butterfly height from config
        butterfly_height = self._parse_height(config.get("butterfly_height"))

        # Create initial figures with configured height
        initial_butterfly = app._plot_factory._create_butterfly_plot(
            0, figure_height=butterfly_height
        )
        initial_brain_plots = app._plot_factory._create_2d_brain_projections_plotly(0)

        # Build layout
        self._setup_vertical_layout(app, initial_butterfly, initial_brain_plots, config)

    def _get_vertical_config(self, app: "EelbrainPlotly2DViz") -> Dict[str, Any]:
        """Get configuration for vertical layout."""
        base = self._get_layout_config(app)
        num_views = base["num_views"]
        env = base["env"]

        brain_width = self._get_brain_width_for_views(num_views)

        config = {
            "butterfly_width": "100%",
            "brain_width": brain_width[env],
            "brain_margin": "1.5%" if env == "jupyter" else "0.5%",
            "plot_height": "250px" if env == "jupyter" else "450px",
            "butterfly_height": "300px" if env == "jupyter" else "400px",
            "container_padding": "2px" if env == "jupyter" else "5px",
            "arrangement": "vertical",
            "num_views": num_views,
            "brain_views": base["brain_views"],
        }

        # Special adjustments for 4-view modes
        if app.display_mode in ["lzry", "lyrz"] and num_views == 4:
            config["brain_margin"] = "0.5%"

        return config

    def _get_brain_width_for_views(self, num_views: int) -> Dict[str, str]:
        """Calculate brain view width based on number of views."""
        if num_views == 1:
            return {"jupyter": "98%", "browser": "98%"}
        elif num_views == 2:
            return {"jupyter": "48%", "browser": "48%"}
        elif num_views == 3:
            return {"jupyter": "30%", "browser": "32%"}
        else:  # 4 views
            return {"jupyter": "24%", "browser": "24%"}

    def _parse_height(self, height_str: Any) -> Optional[int]:
        """Parse height string to integer pixels."""
        if isinstance(height_str, str) and height_str.endswith("px"):
            try:
                return int(float(height_str[:-2]))
            except ValueError:
                return None
        return None

    def _setup_vertical_layout(
        self,
        app: "EelbrainPlotly2DViz",
        initial_butterfly: go.Figure,
        initial_brain_plots: Dict[str, go.Figure],
        config: Dict[str, Any],
    ) -> None:
        """Setup traditional vertical layout (butterfly top, brain views below)."""
        butterfly_style = {
            "width": config["butterfly_width"],
            "margin-bottom": "10px" if app.is_jupyter_mode else "20px",
        }

        butterfly_graph_style = {"height": config["butterfly_height"]}
        brain_height = config["plot_height"]
        brain_width = config["brain_width"]
        brain_margin = config["brain_margin"]
        container_padding = config["container_padding"]

        app.app.layout = html.Div(
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
                    value=app.realtime_mode_default,
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
                                html.Div(
                                    self._create_brain_view_containers(
                                        app,
                                        initial_brain_plots,
                                        brain_height,
                                        brain_width,
                                        brain_margin,
                                    ),
                                    style={"textAlign": "center"},
                                ),
                            ],
                            style={"width": "100%"},
                        ),
                    ]
                ),
                # Info panel (hidden)
                html.Div(
                    id="info-panel",
                    style={"display": "none"},
                ),
            ],
            style={"width": "100%", "height": "auto", "padding": container_padding},
        )


class HorizontalLayout(LayoutBuilder):
    """Horizontal layout strategy - butterfly plot on left, brain views on right.

    This compact layout places the time series plot on the left side
    with brain projections arranged on the right side.
    """

    def build(self, app: "EelbrainPlotly2DViz") -> None:
        """Build horizontal layout for the visualization app.

        Parameters
        ----------
        app
            The EelbrainPlotly2DViz instance to configure.
        """
        config = self._get_horizontal_config(app)
        app._current_layout_config = config

        # Extract butterfly height from config
        butterfly_height = self._parse_height(config.get("butterfly_height"))

        # Create initial figures with configured height
        initial_butterfly = app._plot_factory._create_butterfly_plot(
            0, figure_height=butterfly_height
        )
        initial_brain_plots = app._plot_factory._create_2d_brain_projections_plotly(0)

        # Build layout
        self._setup_horizontal_layout(
            app, initial_butterfly, initial_brain_plots, config
        )

    def _get_horizontal_config(self, app: "EelbrainPlotly2DViz") -> Dict[str, Any]:
        """Get configuration for horizontal layout."""
        base = self._get_layout_config(app)
        num_views = base["num_views"]
        env = base["env"]

        brain_width = self._get_brain_width_for_views(num_views)

        config = {
            "butterfly_width": "30%",
            "brain_width": brain_width[env],
            "brain_margin": "0px",
            "plot_height": "200px" if env == "jupyter" else "350px",
            "butterfly_height": "200px" if env == "jupyter" else "350px",
            "container_padding": "5px" if env == "jupyter" else "10px",
            "arrangement": "horizontal",
            "num_views": num_views,
            "brain_views": base["brain_views"],
        }

        # Special adjustments for 4-view modes
        if app.display_mode in ["lzry", "lyrz"] and num_views == 4:
            config["brain_margin"] = "0px"
            config["butterfly_width"] = "25%"

        return config

    def _get_brain_width_for_views(self, num_views: int) -> Dict[str, str]:
        """Calculate brain view width for horizontal layout."""
        butterfly_width = 30
        available_for_brains = 100 - butterfly_width
        brain_width = available_for_brains / num_views
        brain_width_str = f"{brain_width:.2f}%"
        return {"jupyter": brain_width_str, "browser": brain_width_str}

    def _parse_height(self, height_str: Any) -> Optional[int]:
        """Parse height string to integer pixels."""
        if isinstance(height_str, str) and height_str.endswith("px"):
            try:
                return int(float(height_str[:-2]))
            except ValueError:
                return None
        return None

    def _create_horizontal_colorbar(self, app: "EelbrainPlotly2DViz") -> go.Figure:
        """Create a standalone horizontal colorbar figure."""
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker=dict(
                    colorscale=app.cmap,
                    showscale=True,
                    cmin=app.global_vmin,
                    cmax=app.global_vmax,
                    colorbar=dict(
                        thickness=20,
                        len=0.8,
                        x=0.5,
                        xanchor="center",
                        y=0.5,
                        yanchor="middle",
                        orientation="h",
                    ),
                ),
                showlegend=False,
                hoverinfo="skip",
            )
        )

        fig.update_layout(
            height=80,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
        )

        return fig

    def _create_brain_view_containers_horizontal(
        self,
        app: "EelbrainPlotly2DViz",
        brain_plots: Dict[str, go.Figure],
        brain_height: str,
        brain_width: str,
        brain_margin: str,
    ) -> List:
        """Create dynamic brain view containers for horizontal layout."""
        containers = []

        for i, view_name in enumerate(app.brain_views):
            container = html.Div(
                [
                    dcc.Graph(
                        id=f"brain-{view_name}-plot",
                        figure=brain_plots[view_name],
                        style={
                            "height": brain_height,
                            "width": "100%",
                            "margin": "0",
                            "padding": "0",
                        },
                        config={"displayModeBar": False},
                    )
                ],
                style={
                    "width": brain_width,
                    "display": "inline-block",
                    "verticalAlign": "top",
                    "margin": "0",
                    "padding": "0",
                    "boxSizing": "border-box",
                },
            )
            containers.append(container)

            # Add line break after every 2 views only for modes with more than 4 views
            if (
                len(app.brain_views) > 4
                and (i + 1) % 2 == 0
                and i < len(app.brain_views) - 1
            ):
                line_break = html.Div(style={"width": "100%", "height": "0px"})
                containers.append(line_break)

        return containers

    def _setup_horizontal_layout(
        self,
        app: "EelbrainPlotly2DViz",
        initial_butterfly: go.Figure,
        initial_brain_plots: Dict[str, go.Figure],
        config: Dict[str, Any],
    ) -> None:
        """Setup horizontal layout (butterfly left, brain views right)."""
        butterfly_graph_style = {"height": config["butterfly_height"]}
        brain_height = config["plot_height"]
        brain_width = config["brain_width"]
        brain_margin = config["brain_margin"]
        container_padding = config["container_padding"]

        # Create horizontal colorbar
        colorbar_fig = self._create_horizontal_colorbar(app)

        app.app.layout = html.Div(
            [
                # Hidden stores for state management
                dcc.Store(id="selected-time-idx", data=0),
                dcc.Store(id="selected-source-idx", data=None),
                # Top row: Realtime switch (left) and Colorbar (right)
                html.Div(
                    [
                        # Left: Real-time mode switch above butterfly plot area
                        html.Div(
                            [
                                dcc.Checklist(
                                    id="realtime-mode-switch",
                                    options=[
                                        {
                                            "label": "Real-time Update on Hover",
                                            "value": "realtime",
                                        }
                                    ],
                                    value=app.realtime_mode_default,
                                    style={"textAlign": "center", "marginTop": "20px"},
                                )
                            ],
                            style={
                                "width": "35%",
                                "display": "inline-block",
                                "verticalAlign": "top",
                            },
                        ),
                        # Right: Horizontal colorbar above brain plots
                        html.Div(
                            [
                                dcc.Graph(
                                    id="horizontal-colorbar",
                                    figure=colorbar_fig,
                                    style={"height": "80px"},
                                    config={"displayModeBar": False},
                                )
                            ],
                            style={
                                "width": "65%",
                                "display": "inline-block",
                                "verticalAlign": "top",
                                "textAlign": "center",
                            },
                        ),
                    ],
                    style={
                        "marginTop": "0px",
                        "marginBottom": "0px",
                    },
                ),
                # Main content - arranged horizontally
                html.Div(
                    [
                        # Left: Butterfly plot (compact)
                        html.Div(
                            [
                                dcc.Graph(
                                    id="butterfly-plot",
                                    figure=initial_butterfly,
                                    style={
                                        "height": butterfly_graph_style["height"],
                                        "width": "100%",
                                        "margin": "0",
                                        "padding": "0",
                                    },
                                    config={"displayModeBar": False},
                                )
                            ],
                            style={
                                "width": config["butterfly_width"],
                                "display": "inline-block",
                                "verticalAlign": "top",
                                "margin": "0",
                                "padding": "0",
                                "boxSizing": "border-box",
                            },
                        )
                    ]
                    + self._create_brain_view_containers_horizontal(
                        app,
                        initial_brain_plots,
                        brain_height,
                        brain_width,
                        brain_margin,
                    ),
                    style={
                        "marginBottom": "0px",
                        "fontSize": "0",
                    },
                ),
                # Info panel (hidden)
                html.Div(
                    id="info-panel",
                    style={"display": "none"},
                ),
            ],
            style={
                "width": "100%",
                "height": "auto",
                "maxHeight": "100%",
                "padding": container_padding,
                "margin": "0",
                "overflow": "hidden",
            },
        )


# =============================================================================
# Layout Strategy Registry - supports Open/Closed Principle
# =============================================================================

#: Registry of available layout strategies.
#: Contains 'vertical' and 'horizontal' by default.
#: New strategies can be added via register_layout() without modifying existing code.
LAYOUTS: Dict[str, LayoutBuilder] = {
    "vertical": VerticalLayout(),
    "horizontal": HorizontalLayout(),
}


def get_layout_builder(layout_mode: str) -> LayoutBuilder:
    """Get a layout builder by name from the registry.

    Parameters
    ----------
    layout_mode
        Name of the layout strategy ('vertical', 'horizontal', or custom registered name).

    Returns
    -------
    LayoutBuilder
        The layout builder instance.

    Raises
    ------
    ValueError
        If the layout_mode is not registered.

    Example
    -------
    >>> builder = get_layout_builder("horizontal")
    """
    if layout_mode not in LAYOUTS:
        raise ValueError(
            f"Unknown layout_mode: '{layout_mode}'. "
            f"Available layouts: {list(LAYOUTS.keys())}"
        )
    return LAYOUTS[layout_mode]


def register_layout(name: str, builder: LayoutBuilder) -> None:
    """Register a new layout strategy.

    This allows extending the system with new layouts without modifying
    existing code (Open/Closed Principle).

    Parameters
    ----------
    name
        Name to register the layout under.
    builder
        The LayoutBuilder instance to register.

    Example
    -------
    >>> register_layout("compact", CompactLayout())
    >>> viz = EelbrainPlotly2DViz(layout_mode="compact")
    """
    LAYOUTS[name] = builder


# =============================================================================
class LayoutBuilderHelper:
    """Helper responsible for arranging UI components.

    This helper has a single responsibility: layout composition. It delegates
    the actual layout construction to LayoutBuilder strategies, following
    the Strategy pattern and Open/Closed Principle.

    The helper provides:
    - _setup_layout(): Delegates to the appropriate LayoutBuilder
    - _get_layout_config(): Returns layout configuration for callbacks
    - _estimate_jupyter_iframe_height(): Calculates Jupyter display height
    - _get_brain_width_for_views(): Calculates brain view widths

    Users can extend the layout system by:
    1. Creating a custom LayoutBuilder subclass
    2. Registering it with register_layout()
    3. Using the custom layout_mode in EelbrainPlotly2DViz
    """

    # Declare expected attributes from the main class
    app: Any  # dash.Dash
    layout_mode: str
    display_mode: str
    is_jupyter_mode: bool
    brain_views: List[str]
    realtime_mode_default: List[str]
    cmap: Any
    global_vmin: float
    global_vmax: float
    _current_layout_config: Optional[Dict[str, Any]]

    def __init__(self, viz: Any):
        """Initialize the layout builder helper.

        Parameters
        ----------
        viz
            The EelbrainPlotly2DViz instance this helper operates on.
        """
        self._viz = viz

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to the parent visualization instance."""
        return getattr(self._viz, name)

    def __setattr__(self, name: str, value: Any) -> None:
        """Delegate state changes to the parent visualization instance."""
        if name == "_viz":
            super().__setattr__(name, value)
        else:
            setattr(self._viz, name, value)

    def _setup_layout(self) -> None:
        """Setup the Dash app layout based on layout_mode.

        This method delegates to the appropriate LayoutBuilder strategy
        from the LAYOUTS registry.
        """
        # Get layout builder from registry
        builder = get_layout_builder(self.layout_mode)
        # Delegate layout construction to the builder using the parent viz
        builder.build(self._viz)

    def _get_layout_config(self) -> Dict[str, Any]:
        """Get layout configuration based on layout_mode, display_mode and environment.

        Returns
        -------
        Dict[str, Any]
            Configuration dictionary with layout parameters.
        """
        num_views = len(self.brain_views)

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
                "butterfly_width": "30%",
                "brain_width": self._get_brain_width_for_views(num_views, "horizontal"),
                "brain_margin": {"jupyter": "0px", "browser": "0px"},
                "plot_height": {"jupyter": "200px", "browser": "350px"},
                "butterfly_height": {"jupyter": "200px", "browser": "350px"},
                "container_padding": {"jupyter": "5px", "browser": "10px"},
                "arrangement": "horizontal",
            },
        }

        base_config = layout_configs.get(self.layout_mode, layout_configs["vertical"])
        env = "jupyter" if self.is_jupyter_mode else "browser"

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

        # Special adjustments for 4-view modes
        if self.display_mode in ["lzry", "lyrz"] and num_views == 4:
            if self.layout_mode == "vertical":
                config["brain_margin"] = "0.5%"
            else:
                config["brain_margin"] = "0px"
                config["butterfly_width"] = "25%"

        return config

    def _estimate_jupyter_iframe_height(self) -> Optional[int]:
        """Estimate iframe height so plots fill the cell without stretching."""
        if not self.is_jupyter_mode:
            return None

        config = getattr(self, "_current_layout_config", None)
        if not config:
            return None

        def _to_pixels(value: Any) -> Optional[int]:
            if value is None:
                return None
            if isinstance(value, (int, float)):
                return int(value)
            if isinstance(value, str) and value.endswith("px"):
                try:
                    return int(float(value[:-2]))
                except ValueError:
                    return None
            return None

        butterfly_height = _to_pixels(config.get("butterfly_height"))
        brain_height = _to_pixels(config.get("plot_height"))
        arrangement = config.get("arrangement", "vertical")

        if arrangement == "vertical":
            dynamic_height = (butterfly_height or 0) + (brain_height or 0)
            static_offset = 102
            total_height = dynamic_height + static_offset
        else:
            colorbar_row_height = 120
            main_content_height = max(butterfly_height or 0, brain_height or 0)
            container_padding_total = 10
            total_height = (
                colorbar_row_height + main_content_height + container_padding_total
            )

        return max(total_height, 200)

    def _get_brain_width_for_views(
        self, num_views: int, layout_mode: str
    ) -> Dict[str, str]:
        """Calculate brain view width based on number of views and layout mode."""
        if layout_mode == "vertical":
            if num_views == 1:
                return {"jupyter": "98%", "browser": "98%"}
            elif num_views == 2:
                return {"jupyter": "48%", "browser": "48%"}
            elif num_views == 3:
                return {"jupyter": "30%", "browser": "32%"}
            else:
                return {"jupyter": "24%", "browser": "24%"}
        else:
            butterfly_width = 30
            available_for_brains = 100 - butterfly_width
            brain_width = available_for_brains / num_views
            brain_width_str = f"{brain_width:.2f}%"
            return {"jupyter": brain_width_str, "browser": brain_width_str}
