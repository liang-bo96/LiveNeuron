from typing import Any, Dict, List, Optional

import plotly.graph_objects as go
from dash import dcc, html


class LayoutBuilderMixin:
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
                "butterfly_width": "30%",
                "brain_width": self._get_brain_width_for_views(num_views, "horizontal"),
                "brain_margin": {"jupyter": "0px", "browser": "0px"},
                "plot_height": {
                    "jupyter": "200px",
                    "browser": "350px",
                },  # Match brain figure height
                "butterfly_height": {
                    "jupyter": "200px",
                    "browser": "350px",
                },  # Match butterfly figure height
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

        # Keep all four views on a single row for lzry/lyrz in vertical mode
        if (
            self.layout_mode == "vertical"
            and self.display_mode in ["lzry", "lyrz"]
            and num_views == 4
        ):
            config["brain_margin"] = "0.5%"

        # Special adjustments for 4-view modes (lzry, lyrz) in horizontal layout
        if (
            self.layout_mode == "horizontal"
            and self.display_mode in ["lzry", "lyrz"]
            and num_views == 4
        ):
            config["brain_margin"] = "0px"  # No margin between brain plots
            config["butterfly_width"] = (
                "25%"  # Smaller butterfly plot: 25% + 4*16% = ~90%
            )

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

        # Calculate total height based on actual layout structure
        if self.layout_mode == "vertical":
            # Vertical layout structure:
            # - Title (H1): ~50px (text + margins)
            # - Checklist: ~50px (checkbox + margins)
            # - Butterfly plot: 300px
            # - Brain plots: 250px
            # - Container padding: ~2px
            dynamic_height = (butterfly_height or 0) + (brain_height or 0)
            static_offset = 102  # Title + Checklist + Padding
            total_height = dynamic_height + static_offset
        else:
            # Horizontal layout actual structure:
            # - Colorbar row: ~120px (80px graph + 40px container padding/margins)
            # - Main content row: 200px (butterfly and brains side-by-side)
            # - Container padding: 10px
            colorbar_row_height = 120
            main_content_height = max(butterfly_height or 0, brain_height or 0)
            container_padding_total = 10

            total_height = (
                colorbar_row_height + main_content_height + container_padding_total
            )

            # Skip the normal calculation for horizontal mode
            dynamic_height = None
            static_offset = None

        # Ensure we reserve enough space even if parsing failed
        return max(total_height, 200)

    def _get_brain_width_for_views(
        self, num_views: int, layout_mode: str
    ) -> Dict[str, str]:
        """Calculate brain view width based on number of views and layout mode.

        For horizontal mode, we pre-allocate space for butterfly plot and colorbar,
        then divide the remaining space equally among brain plots to ensure uniform size.
        """
        if layout_mode == "vertical":
            # In vertical mode, views are arranged horizontally below butterfly plot
            if num_views == 1:
                return {"jupyter": "98%", "browser": "98%"}
            elif num_views == 2:
                return {"jupyter": "48%", "browser": "48%"}
            elif num_views == 3:
                return {"jupyter": "30%", "browser": "32%"}
            else:  # 4 views (lzry / lyrz) keep all in one row
                # Tighten width so four plots + colorbar fit a single row in notebooks.
                return {"jupyter": "24%", "browser": "24%"}
        else:  # horizontal mode
            # Pre-allocate space for butterfly plot
            # Total available: 100%
            # - Butterfly plot: 25%
            # - Remaining for brain plots: 75%

            butterfly_width = 30  # Butterfly takes 30%
            available_for_brains = 100 - butterfly_width  # 75%

            # Divide remaining space equally among all brain plots
            brain_width = available_for_brains / num_views
            brain_width_str = f"{brain_width:.2f}%"

            return {"jupyter": brain_width_str, "browser": brain_width_str}

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
        # Get layout configuration first
        config = self._get_layout_config()
        self._current_layout_config = config

        # Extract butterfly height from config
        butterfly_height = None
        if "butterfly_height" in config:
            butterfly_height_str = config["butterfly_height"]
            if isinstance(butterfly_height_str, str) and butterfly_height_str.endswith(
                "px"
            ):
                try:
                    butterfly_height = int(float(butterfly_height_str[:-2]))
                except ValueError:
                    pass

        # Create initial figures with configured height
        initial_butterfly = self._create_butterfly_plot(
            0, figure_height=butterfly_height
        )
        initial_brain_plots = self._create_2d_brain_projections_plotly(0)

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

    def _create_horizontal_colorbar(self) -> go.Figure:
        """Create a standalone horizontal colorbar figure."""
        fig = go.Figure()

        # Add invisible scatter trace just for the colorbar
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker=dict(
                    colorscale=self.cmap,
                    showscale=True,
                    cmin=self.global_vmin,
                    cmax=self.global_vmax,
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

        # Minimal layout - just show the colorbar
        fig.update_layout(
            height=80,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
        )

        return fig

    def _setup_horizontal_layout(
        self, initial_butterfly, initial_brain_plots, config
    ) -> None:
        """Setup horizontal layout (butterfly left, brain views right)."""
        butterfly_graph_style = {"height": config["butterfly_height"]}
        brain_height = config["plot_height"]
        brain_width = config["brain_width"]
        brain_margin = config["brain_margin"]
        container_padding = config["container_padding"]

        # Create horizontal colorbar
        colorbar_fig = self._create_horizontal_colorbar()

        self.app.layout = html.Div(
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
                                    value=self.realtime_mode_default,
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
                        initial_brain_plots, brain_height, brain_width, brain_margin
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
