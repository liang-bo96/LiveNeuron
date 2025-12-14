"""
Plot Factory Helper - Responsible for constructing all visualization figures.

This helper's single responsibility is to build plots - whether butterfly plots
or brain projection heatmaps, they all fall under the unified goal of figure
creation.
"""

import base64
import io
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
from scipy.stats import binned_statistic_2d

if TYPE_CHECKING:
    from ._liveneuro import LiveNeuro


class PlotFactoryHelper:
    """Helper responsible for creating all visualization figures.

    This helper has a single responsibility: figure creation. It handles:
    - Creating butterfly plots (time series visualization)
    - Creating 2D brain projections (heatmaps with arrows)
    - Creating colorbars for horizontal layout
    - Converting matplotlib figures to base64 for display

    All plot creation methods are encapsulated here, ensuring that the
    visualization logic is separate from data loading and layout concerns.
    """

    def __init__(self, viz: "LiveNeuro"):
        """Initialize the plot factory helper.

        Parameters
        ----------
        viz
            The LiveNeuro instance this helper operates on.
        """
        self._viz = viz

    def _calculate_view_ranges(
        self, source_coords: Optional[np.ndarray], brain_views: List[str]
    ) -> Dict[str, Dict[str, List[float]]]:
        """Calculate fixed axis ranges for each brain view to prevent size changes."""
        if source_coords is None:
            return {}

        coords = source_coords
        view_ranges: Dict[str, Dict[str, List[float]]] = {}

        for view_name in brain_views:
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
            elif view_name == "left_hemisphere":  # Left hemisphere (Y vs Z)
                # Calculate range using ALL coordinates (no masking) so left/right align
                x_coords = -coords[:, 1]  # Flipped Y (all points)
                y_coords = coords[:, 2]  # Z (all points)
            elif view_name == "right_hemisphere":  # Right hemisphere (Y vs Z)
                # Calculate range using ALL coordinates (no masking) so left/right align
                x_coords = coords[:, 1]  # Y (all points)
                y_coords = coords[:, 2]  # Z (all points)
            else:
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

            view_ranges[view_name] = {
                "x": [x_min - x_padding, x_max + x_padding],
                "y": [y_min - y_padding, y_max + y_padding],
            }

        return view_ranges

    def _calculate_global_colormap_range(
        self, glass_brain_data: Optional[np.ndarray], user_vmax: Optional[float]
    ) -> Tuple[float, float]:
        """Calculate global min/max activity across all time points for fixed colormap."""
        data_max = 1.0

        if glass_brain_data is not None:
            if glass_brain_data.ndim == 3:  # Vector data (n_sources, 3, n_times)
                all_magnitudes = np.linalg.norm(glass_brain_data, axis=1)
            else:  # Scalar data (n_sources, n_times)
                all_magnitudes = glass_brain_data

            data_max = float(np.max(all_magnitudes))

        global_vmin = 0.0
        global_vmax = data_max if user_vmax is None else float(user_vmax)

        # Ensure we have a valid range (avoid zero range)
        if global_vmax - global_vmin < 1e-10:
            global_vmax = global_vmin + 1.0

        return global_vmin, global_vmax

    def _create_butterfly_plot(
        self, selected_time_idx: int = 0, figure_height: Optional[int] = None
    ) -> go.Figure:
        """Create butterfly plot figure (internal method).

        Parameters
        ----------
        selected_time_idx
            Time index to highlight with vertical line.
        figure_height
            Optional figure height in pixels. If None, uses default based on mode.
        """
        fig = go.Figure()

        if self._viz.butterfly_data is None or self._viz.time_values is None:
            fig.add_annotation(
                text="No data loaded",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )
            return fig

        n_sources, n_times = self._viz.butterfly_data.shape

        # Auto-scale data for visibility
        data_to_plot = self._viz.butterfly_data.copy()
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

        # Add individual source traces only if show_max_only is False
        if not self._viz.show_max_only:
            # Plot subset of traces for performance
            max_traces = 20
            step = max(1, n_sources // max_traces)
            indices_to_plot = list(range(0, n_sources, step))

            # Add individual traces
            for idx, i in enumerate(indices_to_plot[:10]):
                trace_data = data_to_plot[i, :]

                fig.add_trace(
                    go.Scatter(
                        x=self._viz.time_values,
                        y=trace_data,
                        mode="lines",
                        name=f"Source {i}",
                        customdata=[i] * n_times,
                        showlegend=(idx < 3) and self._viz.show_labels,
                        opacity=0.6,
                        line=dict(width=1),
                        hoverinfo="skip",  # Don't show in hover
                    )
                )

        # Add mean trace (always shown)
        mean_activity = np.mean(data_to_plot, axis=0)
        fig.add_trace(
            go.Scatter(
                x=self._viz.time_values,
                y=mean_activity,
                mode="lines",
                name="Mean Activity",
                line=dict(color="red", width=3),
                showlegend=self._viz.show_labels,
                hovertemplate="Mean: %{y:.2f}" + unit_suffix + "<extra></extra>",
            )
        )

        # Add max trace (always shown)
        max_activity = np.max(data_to_plot, axis=0)
        fig.add_trace(
            go.Scatter(
                x=self._viz.time_values,
                y=max_activity,
                mode="lines",
                name="Max Activity",
                line=dict(color="darkblue", width=3),
                showlegend=self._viz.show_labels,
                hovertemplate="Max: %{y:.2f}" + unit_suffix + "<extra></extra>",
            )
        )

        # Add vertical line for selected time
        if 0 <= selected_time_idx < len(self._viz.time_values):
            selected_time = self._viz.time_values[selected_time_idx]
            fig.add_vline(
                x=selected_time, line_width=2, line_dash="dash", line_color="blue"
            )

        # Update title based on display mode and show_labels
        if self._viz.show_labels:
            if self._viz.show_max_only:
                title_text = (
                    f"Source Activity Time Series - Mean & Max ({n_sources} sources)"
                )
            else:
                title_text = (
                    f"Source Activity Time Series (subset of {n_sources} sources)"
                )
            xaxis_title = "Time (s)"
            yaxis_title = f"Activity{unit_suffix}"
        else:
            title_text = None
            xaxis_title = None
            yaxis_title = None

        # Adjust layout based on mode
        if figure_height is not None:
            # Use provided height
            height = figure_height
        else:
            # Try to get height from current layout config
            config = self._viz._current_layout_config
            if config and "butterfly_height" in config:
                butterfly_height_str = config["butterfly_height"]
                if isinstance(
                    butterfly_height_str, str
                ) and butterfly_height_str.endswith("px"):
                    try:
                        height = int(float(butterfly_height_str[:-2]))
                    except ValueError:
                        # Fall back to mode-based defaults
                        height = 200 if self._viz.is_jupyter_mode else 350
                else:
                    height = 200 if self._viz.is_jupyter_mode else 350
            else:
                # Fall back to mode-based defaults
                height = 200 if self._viz.is_jupyter_mode else 350

        if self._viz.is_jupyter_mode:
            margin = dict(l=0, r=0, t=0, b=0)  # Tight margins for maximum space
        else:
            margin = dict(l=40, r=20, t=10, b=40)  # Moderate margins for browser

        fig.update_layout(
            title=title_text,
            xaxis_title=xaxis_title,
            yaxis_title=yaxis_title,
            autosize=True,  # Enable autosize to fill container
            xaxis=dict(
                range=[self._viz.time_values[0], self._viz.time_values[-1]],
                showspikes=True,  # Show vertical spike line at cursor
                spikemode="across",  # Spike goes across the plot
                spikesnap="cursor",  # Spike follows cursor, not data points
            ),
            yaxis=dict(range=[y_min - y_margin, y_max + y_margin]),
            hovermode="x unified",  # Unified hover on x-axis
            hoverdistance=-1,  # Allow hover without nearby data points
            height=height,
            margin=margin,
            showlegend=self._viz.show_labels,  # Only show legend if show_labels is True
            # Enable clicking on the plot area
            clickmode="event+select",
        )

        return fig

    def _create_2d_brain_projections_plotly(
        self, time_idx: int = 0, source_idx: Optional[int] = None
    ) -> Dict[str, go.Figure]:
        """Create 2D brain projections using Plotly scatter plots (internal method)."""
        if (
            self._viz.glass_brain_data is None
            or self._viz.source_coords is None
            or self._viz.time_values is None
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
            return {view: placeholder_fig for view in self._viz.brain_views}

        try:
            # Get time slice of data
            if time_idx >= len(self._viz.time_values):
                time_idx = 0

            time_value = self._viz.time_values[time_idx]

            # Get activity at this time point
            if self._viz.glass_brain_data.ndim == 3:  # (n_sources, 3, n_times)
                time_activity = self._viz.glass_brain_data[
                    :, :, time_idx
                ]  # (n_sources, 3)
                activity_magnitude = np.linalg.norm(
                    time_activity, axis=1
                )  # (n_sources,)
            else:  # (n_sources, n_times)
                activity_magnitude = self._viz.glass_brain_data[:, time_idx]

            # Use global min/max for consistent colormap across all time points
            # This allows intuitive comparison of activity levels across time
            global_min = self._viz.global_vmin
            global_max = self._viz.global_vmax

            # Get figure height from current layout config
            config = self._viz._current_layout_config
            figure_height = None
            if config and "plot_height" in config:
                plot_height_str = config["plot_height"]
                if isinstance(plot_height_str, str) and plot_height_str.endswith("px"):
                    try:
                        figure_height = int(float(plot_height_str[:-2]))
                    except ValueError:
                        pass

            # Create brain projections
            brain_plots = {}
            views = self._viz.brain_views

            for i, view_name in enumerate(views):
                try:
                    # Show colorbar on last view in vertical mode, hide in horizontal mode
                    if self._viz.layout_mode == "horizontal":
                        show_colorbar = False  # Horizontal has separate colorbar
                    else:
                        show_colorbar = (
                            i == len(views) - 1
                        )  # Show on last view in vertical

                    brain_fig = self._create_plotly_brain_projection(
                        view_name,
                        self._viz.source_coords,
                        activity_magnitude,
                        time_value,
                        source_idx,
                        show_colorbar=show_colorbar,
                        zmin=global_min,
                        zmax=global_max,
                        figure_height=figure_height,
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
        figure_height: Optional[int] = None,
    ) -> go.Figure:
        """Create a Plotly plot for a specific brain view with vector arrows.

        Parameters
        ----------
        figure_height
            Optional figure height in pixels. If None, uses default based on mode.
        """
        # Show all data without filtering
        active_coords = coords
        active_activity = activity
        active_indices = np.arange(len(coords))

        # Create Plotly figure
        fig = go.Figure()

        # Get time index for vector components
        time_idx = np.argmin(np.abs(self._viz.time_values - time_value))

        # Get vector components for active sources
        if self._viz.glass_brain_data is not None and len(active_indices) > 0:
            # (n_active, 3) or (n_active, 1)
            active_vectors = self._viz.glass_brain_data[active_indices, :, time_idx]
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
            title = None
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
            title = None
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
                    colorscale=self._viz.cmap,
                    colorbar=(
                        dict(
                            title="",
                            thickness=12,  # Thinner colorbar for less space usage
                            len=0.7,  # Shorter colorbar (70% of plot height)
                            x=1.15,  # Position further outside to avoid squeezing brain plot
                            xanchor="left",  # Anchor to the left of the colorbar
                            xpad=0,  # No padding between plot and colorbar
                        )
                        if show_colorbar
                        else None
                    ),
                    showscale=show_colorbar,
                    zmin=zmin,
                    zmax=zmax,
                    hovertemplate="Activity: %{z:.3f}<extra></extra>",  # Show heatmap values
                )
            )

            # Update layout to have white background
            fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")

            # Add vector arrows if we have vector data (not scalar data)
            if has_vector_data:
                # Convert relative arrow_scale (user parameter, default=1.0) to absolute scale
                # Base scale of 0.025 provides good default visualization
                arrow_scale = self._viz.arrow_scale * 0.025

                # Calculate arrow magnitudes for filtering
                arrow_magnitudes = np.linalg.norm(active_vectors, axis=1)

                # Determine threshold for showing arrows
                if self._viz.arrow_threshold is None:
                    # Show all arrows
                    show_arrow_mask = np.ones(len(active_vectors), dtype=bool)
                elif self._viz.arrow_threshold == "auto":
                    # Use 10% of maximum magnitude as threshold
                    threshold_value = 0.1 * np.max(arrow_magnitudes)
                    show_arrow_mask = arrow_magnitudes > threshold_value
                else:
                    # Use specified threshold
                    threshold_value = float(self._viz.arrow_threshold)
                    show_arrow_mask = arrow_magnitudes > threshold_value

                # Group sources by 2D position and select the one with maximum ACTIVITY
                # (not 2D projected magnitude) for each position.
                # Multiple 3D sources can project to the same 2D position, so we need
                # to select one. We choose the source with highest activity because
                # that's what we display in the hover and heatmap.
                position_to_max_idx = {}

                # Check all source points
                for i in range(len(active_coords)):
                    # Only consider arrows that meet the threshold criteria
                    if not show_arrow_mask[i]:
                        continue

                    # Create position key (rounded to avoid floating point precision
                    # issues)
                    pos_key = (round(x_coords[i], 6), round(y_coords[i], 6))

                    # If this position hasn't been seen, or current source has larger
                    # ACTIVITY (3D magnitude), select it.
                    # This ensures the displayed arrow shows the maximum activity value
                    # for that 2D position, matching the heatmap and hover display.
                    if (
                        pos_key not in position_to_max_idx
                        or active_activity[i]
                        > active_activity[position_to_max_idx[pos_key]]
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
                    # Get the actual activity (3D magnitude) for hover display
                    arrow_activities = active_activity[selected_indices]

                    # Create all arrows using Plotly quiver plot (fastest method)
                    self._create_quiver_arrows(
                        fig,
                        arrow_x,
                        arrow_y,
                        arrow_u,
                        arrow_v,
                        arrow_scale,
                        activity_values=arrow_activities,
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

                        if self._viz.arrow_threshold is not None:
                            if self._viz.arrow_threshold == "auto":
                                threshold_value = 0.1 * np.max(
                                    np.linalg.norm(active_vectors, axis=1)
                                )
                            else:
                                threshold_value = float(self._viz.arrow_threshold)
                            show_selected_arrow = (
                                selected_arrow_magnitude > threshold_value
                            )

                        if show_selected_arrow:
                            x_start = x_coords[pos]
                            y_start = y_coords[pos]

                            # Add highlighted arrow for selected source (using quiver)
                            self._create_quiver_arrows(
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
        # Use consistent right margin for all plots to ensure uniform size
        if figure_height is not None:
            # Use provided height
            height = figure_height
        elif self._viz.is_jupyter_mode:
            height = 200
        else:
            height = 450  # Larger height for external browser mode

        if self._viz.is_jupyter_mode:
            margin = dict(l=0, r=0, t=0, b=0)  # Zero margins for maximum space
        else:
            margin = dict(l=10, r=10, t=10, b=10)  # Small margins for better layout

        # Note: Right margin is the same for all plots (with or without colorbar)
        # to ensure uniform brain plot sizes. Colorbar is positioned outside at x=1.15

        # Get fixed axis ranges for this view to prevent size changes across time
        axis_ranges = self._viz.view_ranges.get(view_name, {})
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
                domain=[0, 1],  # Use full width of plot area
                showgrid=False,
                zeroline=False,
            ),
            # Equal aspect ratio, hide labels
            yaxis=dict(
                showticklabels=False,
                title="",
                range=y_range,  # Fixed range to prevent size changes
                domain=[0, 1],  # Use full height of plot area
                showgrid=False,
                zeroline=False,
            ),
            height=height,
            width=None,  # Let width auto-adjust to container
            autosize=True,  # Enable autosize to fill container
            margin=margin,
            showlegend=False,
            # plot_bgcolor="#2b2b2b",  # Dark background for brain plots
            hoverlabel=dict(
                bgcolor="rgba(255, 255, 255, 0.7)",  # Semi-transparent white background
                font=dict(color="black", size=10),
                bordercolor="rgba(0, 0, 0, 0.2)",
            ),
        )

        return fig

    def _create_quiver_arrows(
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
        activity_values: Optional[np.ndarray] = None,
    ) -> None:
        """Create arrows using Plotly's figure_factory quiver plot.

        This method uses ff.create_quiver which provides proper arrow visualization
        with built-in Plotly optimizations.

        Note: Arrow head size scales with arrow length (Plotly default behavior).

        Parameters
        ----------
        activity_values
            Optional array of activity values (3D magnitude) to display in hover.
            If None, uses 2D projected magnitude.
        """
        if len(x_coords) == 0:
            return

        try:
            # Create quiver figure using Plotly's figure_factory
            quiver_fig = ff.create_quiver(
                x=x_coords,
                y=y_coords,
                u=u_vectors,
                v=v_vectors,
                scale=arrow_scale,  # Scale controls arrow length
                arrow_scale=size * 0.3,  # Arrow head size (relative to arrow length)
                line=dict(color=color, width=width),
                name="vectors",
            )

            # Add all traces from quiver figure to our figure
            for trace in quiver_fig.data:
                # Customize the trace
                trace.showlegend = False
                # Disable hover on arrows to show only heatmap hover
                trace.hoverinfo = "skip"

                fig.add_trace(trace)

        except Exception as e:
            print(f"Warning: Quiver plot failed ({e}), falling back to annotations")
            # Fall back to annotation method if quiver fails
            self._create_batch_arrows(
                fig,
                x_coords,
                y_coords,
                u_vectors,
                v_vectors,
                arrow_scale,
                color,
                width,
                size,
                activity_values,
            )

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
        activity_values: Optional[np.ndarray] = None,
    ) -> None:
        """Create arrows using annotation-based method (fallback for quiver).

        This is a simple, single-threaded implementation used as fallback
        when quiver plots fail. The bottleneck is in rendering (adding to figure),
        not in computation, so multi-threading doesn't help much.

        Parameters
        ----------
        activity_values
            Optional array of activity values (3D magnitude) to display in hover.
            If None, uses 2D projected magnitude.
        """

        if len(x_coords) == 0:
            return

        # Calculate all endpoints at once (vectorized)
        x_ends = x_coords + u_vectors * arrow_scale
        y_ends = y_coords + v_vectors * arrow_scale

        # Note: activity_values parameter exists for API compatibility but is not used
        # because annotations don't display hovertext (to avoid interfering with heatmap hover)

        # Create annotation objects using simple list comprehension
        # Note: No hovertext to avoid interfering with heatmap hover
        annotations_to_add = [
            dict(
                x=float(x_ends[i]),
                y=float(y_ends[i]),
                ax=float(x_coords[i]),
                ay=float(y_coords[i]),
                xref="x",
                yref="y",
                axref="x",
                ayref="y",
                text="",
                showarrow=True,
                arrowhead=2,
                arrowsize=size,
                arrowwidth=width,
                arrowcolor=color,
                # No hovertext - show only heatmap hover
            )
            for i in range(len(x_coords))
        ]

        # Batch add all annotations at once
        if annotations_to_add:
            # Get existing annotations (if any) and add new ones
            existing_annotations = (
                list(fig.layout.annotations) if fig.layout.annotations else []
            )
            all_annotations = existing_annotations + annotations_to_add

            # Update layout with all annotations in one operation
            fig.update_layout(annotations=all_annotations)

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
                    colorscale=self._viz.cmap,
                    showscale=True,
                    cmin=self._viz.global_vmin,
                    cmax=self._viz.global_vmax,
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
