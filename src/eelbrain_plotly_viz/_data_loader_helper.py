"""
Data Loader Helper - Responsible for all data ingestion logic.

This helper's single responsibility is to handle data loading - reading NDVar
or sample data and normalizing it into a consistent internal format.
Loading and normalization are both part of one cohesive responsibility:
preparing data for visualization.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional

import numpy as np
from eelbrain import set_parc, NDVar, datasets

if TYPE_CHECKING:
    from ._viz_2d import EelbrainPlotly2DViz


class DataLoaderHelper:
    """Helper responsible for data ingestion and normalization.

    This helper has a single responsibility: preparing data for visualization.
    It handles:
    - Loading NDVar data directly
    - Loading MNE sample data with optional region filtering
    - Normalizing data into a consistent internal format
    - Computing derived data (butterfly data from vector norms)
    - Parsing display modes and calculating view ranges
    """

    def __init__(self, viz: "EelbrainPlotly2DViz"):
        """Initialize the data loader helper.

        Parameters
        ----------
        viz
            The EelbrainPlotly2DViz instance this helper operates on.
        """
        self._viz = viz

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
                self._viz.region_of_brain = region
            except Exception as e:
                print(f"Failed to apply parcellation {region}: {e}")
                print("Using full brain data instead")
                self._viz.region_of_brain = "Full Brain"
        else:
            self._viz.region_of_brain = "Full Brain"

        # Average over trials/cases
        src_ndvar = data_ds["src"].mean("case")

        # Extract coordinates and data
        self._viz.glass_brain_data = src_ndvar.get_data(("source", "space", "time"))
        self._viz.source_coords = src_ndvar.source.coordinates  # (n_sources, 3)
        self._viz.time_values = src_ndvar.time.times

        # Store source space info
        self._viz.source_space = src_ndvar.source
        if hasattr(self._viz.source_space, "parc"):
            self._viz.parcellation = self._viz.source_space.parc
        else:
            self._viz.parcellation = None

        # Compute norm for butterfly plot
        self._viz.butterfly_data = np.linalg.norm(self._viz.glass_brain_data, axis=1)

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
        self._viz.source_coords = source.coordinates
        self._viz.time_values = y.time.times

        # Store source space info
        self._viz.source_space = source
        if hasattr(self._viz.source_space, "parc"):
            self._viz.parcellation = self._viz.source_space.parc
            self._viz.region_of_brain = str(self._viz.parcellation)
        else:
            self._viz.parcellation = None
            self._viz.region_of_brain = "Full Brain"

        # Handle space dimension (vector data)
        if y.has_dim("space"):
            # Extract 3D vector data
            self._viz.glass_brain_data = y.get_data(
                ("source", "space", "time")
            )  # (n_sources, 3, n_times)
            # Compute norm for butterfly plot
            self._viz.butterfly_data = np.linalg.norm(self._viz.glass_brain_data, axis=1)
        else:
            # Scalar data - no space dimension
            self._viz.glass_brain_data = y.get_data(
                ("source", "time")
            )  # (n_sources, n_times)
            self._viz.butterfly_data = self._viz.glass_brain_data.copy()
            # Expand to 3D for consistency (assuming scalar represents magnitude)
            # (n_sources, 1, n_times)
            self._viz.glass_brain_data = self._viz.glass_brain_data[:, np.newaxis, :]

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
        if self._viz.source_coords is None:
            self._viz.view_ranges = {}
            return

        coords = self._viz.source_coords
        self._viz.view_ranges = {}

        for view_name in self._viz.brain_views:
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
                # Calculate range using ALL coordinates (no masking)
                # This ensures left and right hemisphere views are aligned
                x_coords = -coords[:, 1]  # Flipped Y (all points)
                y_coords = coords[:, 2]  # Z (all points)
            elif view_name == "right_hemisphere":  # Right hemisphere (Y vs Z, X >= 0)
                # Calculate range using ALL coordinates (no masking)
                # This ensures left and right hemisphere views are aligned
                x_coords = coords[:, 1]  # Y (all points)
                y_coords = coords[:, 2]  # Z (all points)
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

            self._viz.view_ranges[view_name] = {
                "x": [x_min - x_padding, x_max + x_padding],
                "y": [y_min - y_padding, y_max + y_padding],
            }

    def _unify_view_sizes_for_jupyter(self) -> None:
        """Unify view sizes for Jupyter mode to ensure consistent display.

        This method adjusts all brain view ranges to have the same width and height,
        making them appear uniform in size when displayed in Jupyter notebooks.
        Only called when using show_in_jupyter().
        """
        if not self._viz.view_ranges:
            return

        # Calculate the maximum width and height across all views
        max_x_width = max(
            ranges["x"][1] - ranges["x"][0] for ranges in self._viz.view_ranges.values()
        )
        max_y_width = max(
            ranges["y"][1] - ranges["y"][0] for ranges in self._viz.view_ranges.values()
        )

        # Use the larger of the two to ensure square-ish plots with equal sizing
        max_width = max(max_x_width, max_y_width)

        # Update all views to use the unified maximum range
        for view_name in self._viz.view_ranges:
            # Get current center
            x_center = (
                self._viz.view_ranges[view_name]["x"][0]
                + self._viz.view_ranges[view_name]["x"][1]
            ) / 2
            y_center = (
                self._viz.view_ranges[view_name]["y"][0]
                + self._viz.view_ranges[view_name]["y"][1]
            ) / 2

            # Set new range centered around the same point with max width
            self._viz.view_ranges[view_name]["x"] = [
                x_center - max_width / 2,
                x_center + max_width / 2,
            ]
            self._viz.view_ranges[view_name]["y"] = [
                y_center - max_width / 2,
                y_center + max_width / 2,
            ]

    def _calculate_global_colormap_range(self) -> None:
        """Calculate global min/max activity across all time points for fixed colormap.

        This ensures consistent color mapping across time, making it easier to
        compare activity levels at different time points.
        """
        data_max = 1.0

        if self._viz.glass_brain_data is not None:
            # Calculate activity magnitude across all time points
            if self._viz.glass_brain_data.ndim == 3:  # Vector data (n_sources, 3, n_times)
                # Compute norm for each source at each time point
                all_magnitudes = np.linalg.norm(
                    self._viz.glass_brain_data, axis=1
                )  # (n_sources, n_times)
            else:  # Scalar data (n_sources, n_times)
                all_magnitudes = self._viz.glass_brain_data

            data_max = float(np.max(all_magnitudes))

        # Apply user overrides if provided
        self._viz.global_vmin = 0.0
        self._viz.global_vmax = data_max if self._viz.user_vmax is None else self._viz.user_vmax

        # Ensure we have a valid range (avoid zero range)
        if self._viz.global_vmax - self._viz.global_vmin < 1e-10:
            self._viz.global_vmax = self._viz.global_vmin + 1.0
