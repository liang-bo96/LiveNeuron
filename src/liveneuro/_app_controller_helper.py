"""
App Controller Helper - Responsible for user interaction logic.

This helper's single responsibility is controlling application behavior -
handling callbacks, hover/click events, and export functionality.
"""

import random
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import dash
import numpy as np
import plotly.graph_objects as go
from dash import Input, Output, State, html

if TYPE_CHECKING:
    from ._liveneuro import LiveNeuro


# Check if we're running in a Jupyter environment
def _is_jupyter_environment():
    """Check if we're running in a Jupyter notebook environment."""
    try:
        from IPython import get_ipython

        return get_ipython() is not None
    except ImportError:
        return False


JUPYTER_AVAILABLE = _is_jupyter_environment()


class AppControllerHelper:
    """Helper responsible for user interaction and application control.

    This helper has a single responsibility: controlling application behavior.
    It handles:
    - Registering and managing Dash callbacks
    - Processing hover and click events on plots
    - Exporting visualizations as image files
    - Running the Dash application server
    """

    def __init__(self, viz: "LiveNeuro"):
        """Initialize the app controller helper.

        Parameters
        ----------
        viz
            The LiveNeuro instance this helper operates on.
        """
        self._viz = viz

    def setup_callbacks(self) -> None:
        """Setup all Dash callbacks."""

        @self._viz.app.callback(
            Output("butterfly-plot", "figure"), Input("selected-time-idx", "data")
        )
        def update_butterfly(time_idx: int) -> go.Figure:
            if time_idx is None:
                time_idx = 0
            # Get butterfly height from current config
            config = self._viz.current_layout_config
            butterfly_height = None
            if config and "butterfly_height" in config:
                butterfly_height_str = config["butterfly_height"]
                if isinstance(
                    butterfly_height_str, str
                ) and butterfly_height_str.endswith("px"):
                    try:
                        butterfly_height = int(float(butterfly_height_str[:-2]))
                    except ValueError:
                        pass
            return self._viz._plot_factory.create_butterfly_plot(
                selected_time_idx=time_idx, figure_height=butterfly_height
            )

        # Dynamic brain plot outputs based on display_mode
        brain_outputs = [
            Output(f"brain-{view_name}-plot", "figure")
            for view_name in self._viz.brain_views
        ]

        @self._viz.app.callback(
            brain_outputs,
            Input("selected-time-idx", "data"),
            Input("selected-source-idx", "data"),
        )
        def update_brain_projections(time_idx: int, source_idx: int):
            if time_idx is None:
                time_idx = 0

            try:
                brain_plots = (
                    self._viz._plot_factory.create_2d_brain_projections_plotly(
                        time_idx=time_idx, source_idx=source_idx
                    )
                )
                return tuple(
                    brain_plots[view_name] for view_name in self._viz.brain_views
                )
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
                return tuple(empty_fig for _ in self._viz.brain_views)

        @self._viz.app.callback(
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
            """Handle user interaction with butterfly plot.

            Uses hoverData with spikesnap="cursor" for precise time selection.
            The spike follows the mouse cursor (not just data points), giving
            direct access to mouse x-coordinate.

            - Real-time mode: Updates on hover (dynamic)
            - Normal mode: Updates on click (explicit selection)
            """
            ctx = dash.callback_context
            if not ctx.triggered or self._viz.time_values is None:
                return dash.no_update, dash.no_update, dash.no_update

            triggered_id = ctx.triggered[0]["prop_id"]
            is_realtime = realtime_value and "realtime" in realtime_value

            # Handle hover events in real-time mode
            # With spikesnap="cursor", point["x"] is the actual mouse x-coordinate
            if "hoverData" in triggered_id and is_realtime:
                if not hover_data:
                    return dash.no_update, dash.no_update, dash.no_update

                try:
                    point = hover_data["points"][0]
                    hover_time = point["x"]  # Direct mouse x-coordinate from cursor
                    time_idx = np.argmin(np.abs(self._viz.time_values - hover_time))
                    # Do not update source index on hover to avoid frantic updates
                    return time_idx, dash.no_update, dash.no_update
                except (KeyError, IndexError, TypeError):
                    return dash.no_update, dash.no_update, dash.no_update

            # Handle click events in normal mode
            if "clickData" in triggered_id:
                if not click_data:
                    return dash.no_update, dash.no_update, dash.no_update

                try:
                    point = click_data["points"][0]
                    clicked_time = point["x"]  # Time from clicked data point
                    time_idx = np.argmin(np.abs(self._viz.time_values - clicked_time))
                    source_idx = point.get("customdata", None)

                    # If in real-time mode, a click will select the time and disable
                    # real-time mode for focused inspection
                    new_realtime_value = [] if is_realtime else dash.no_update

                    return time_idx, source_idx, new_realtime_value
                except (KeyError, IndexError, TypeError):
                    return dash.no_update, dash.no_update, dash.no_update

            return dash.no_update, dash.no_update, dash.no_update

        @self._viz.app.callback(
            Output("info-panel", "children"),
            Input("selected-time-idx", "data"),
            Input("selected-source-idx", "data"),
        )
        def update_info(time_idx: int, source_idx: int) -> html.P:
            info = []

            if (
                self._viz.time_values is not None
                and time_idx is not None
                and 0 <= time_idx < len(self._viz.time_values)
            ):
                info.append(
                    f"Time: {self._viz.time_values[time_idx]:.3f} s (index {time_idx})"
                )

            if (
                source_idx is not None
                and self._viz.source_coords is not None
                and 0 <= source_idx < len(self._viz.source_coords)
            ):
                coord = self._viz.source_coords[source_idx]
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

    def run(
        self,
        port: Optional[int] = None,
        debug: bool = False,
        mode: Optional[str] = None,
    ) -> None:
        """Run the Dash app with Jupyter integration support.

        Parameters
        ----------
        port
            Port number for the server. If None, uses random port.
        debug
            Enable debug mode. Default is False for cleaner UI.
        mode
            Display mode. Options:
            - 'inline': Embed directly in Jupyter notebook (default in Jupyter)
            - 'jupyterlab': Open in JupyterLab tab (modern Dash)
            - 'external': Open in separate browser window (default outside Jupyter)
            If None, automatically selects 'inline' in Jupyter, 'external' otherwise.
        """
        if port is None:
            port = random.randint(8001, 9001)

        # Auto-detect mode based on environment
        if mode is None:
            mode = "inline" if JUPYTER_AVAILABLE else "external"

        if JUPYTER_AVAILABLE and mode in ["inline", "jupyterlab"]:
            # Prepare visualization for Jupyter (layout + sizing)
            self._viz.prepare_for_jupyter()

            # Auto-calculate height
            iframe_height = self._viz._layout_helper.estimate_jupyter_iframe_height()
            if iframe_height is None:
                iframe_height = 900  # Fallback default

            print(
                "\nStarting 2D Brain Visualization with modern Dash Jupyter integration..."
            )
            print(f"Mode: {mode}, Auto height: {iframe_height}px")

            # Use modern Dash Jupyter integration
            self._viz.app.run(
                debug=debug, port=port, jupyter_mode=mode, jupyter_height=iframe_height
            )
        else:
            print(f"\nStarting 2D Brain Visualization Dash app on port {port}...")
            print(f"Open http://127.0.0.1:{port}/ in your browser")
            if not JUPYTER_AVAILABLE and mode != "external":
                print(
                    "Note: Jupyter environment not detected, using external browser mode"
                )
            print()

            self._viz.app.run(debug=debug, port=port)

    def show_in_jupyter(self, debug: bool = False) -> None:
        """Convenience method to display the visualization inline in Jupyter notebooks.

        Parameters
        ----------
        debug
            Enable debug mode. Default is False for cleaner output.
        """
        if not JUPYTER_AVAILABLE:
            print("Warning: Jupyter environment not detected.")
            print("Falling back to external browser mode...")
            self.run(debug=debug)
            return

        # Prepare visualization for Jupyter (layout + sizing)
        self._viz.prepare_for_jupyter()

        self.run(mode="inline", debug=debug)

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
            butterfly_fig = self._viz._plot_factory.create_butterfly_plot(
                selected_time_idx=time_idx
            )
            butterfly_path = os.path.join(
                output_dir, f"butterfly_plot_{timestamp}.{format}"
            )
            butterfly_fig.write_image(butterfly_path, width=1200, height=600)
            exported_files["butterfly_plot"] = butterfly_path

            # Export brain projections
            brain_plots = self._viz._plot_factory.create_2d_brain_projections_plotly(
                time_idx=time_idx
            )

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
