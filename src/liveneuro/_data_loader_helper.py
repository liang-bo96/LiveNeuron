"""
Data Loader Helper - Responsible for all data ingestion logic.

This helper's single responsibility is to handle data loading - reading NDVar
or sample data and normalizing it into a consistent internal format.
Loading and normalization are both part of one cohesive responsibility:
preparing data for visualization.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

import numpy as np
from eelbrain import NDVar, datasets

if TYPE_CHECKING:
    from ._viz_2d import LiveNeuro


@dataclass
class BrainData:
    """Container for brain data and basic metadata."""

    glass_brain_data: np.ndarray  # Always (n_sources, 3, n_times)
    butterfly_data: np.ndarray  # Always (n_sources, n_times)
    source_coords: np.ndarray  # (n_sources, 3)
    time_values: np.ndarray  # (n_times,)
    source_space: Any
    parcellation: Optional[Any]


class DataLoaderHelper:
    """Helper responsible for data ingestion and normalization.

    This helper has a single responsibility: preparing data for visualization.
    It handles:
    - Loading NDVar data directly
    - Loading MNE sample data
    - Normalizing data into a consistent internal format
    - Computing derived data (butterfly data from vector norms)
    - Parsing display modes and calculating view ranges
    """

    def _load_source_data(self) -> BrainData:
        """Load MNE sample data and prepare for 2D brain visualization.

        Returns
        -------
        BrainData
            Loaded brain data and metadata.
        """
        # Load MNE sample data
        data_ds = datasets.get_mne_sample(src="vol", ori="vector")

        # Average over trials/cases
        src_ndvar = data_ds["src"].mean("case")

        # Extract coordinates and data
        glass_brain_data = src_ndvar.get_data(("source", "space", "time"))
        source_coords = src_ndvar.source.coordinates  # (n_sources, 3)
        time_values = src_ndvar.time.times

        # Source space and parcellation
        source_space = src_ndvar.source
        parcellation = getattr(source_space, "parc", None)

        # Compute norm for butterfly plot
        butterfly_data = np.linalg.norm(glass_brain_data, axis=1)

        return BrainData(
            glass_brain_data=glass_brain_data,
            butterfly_data=butterfly_data,
            source_coords=source_coords,
            time_values=time_values,
            source_space=source_space,
            parcellation=parcellation,
        )

    def _load_ndvar_data(self, y: NDVar) -> BrainData:
        """Load data from NDVar directly.

        Parameters
        ----------
        y
            Data with dimensions ([case,] time, source[, space]).
        Returns
        -------
        BrainData
            Loaded brain data and metadata.
        """
        if y.has_case:
            y = y.mean("case")

        # Extract source dimension info
        source = y.get_dim("source")
        source_coords = source.coordinates
        time_values = y.time.times

        # Source space and parcellation
        source_space = source
        parcellation = getattr(source_space, "parc", None)

        # Handle space dimension (vector data vs scalar data)
        if y.has_dim("space"):
            # Extract 3D vector data (n_sources, 3, n_times)
            glass_brain_data = y.get_data(("source", "space", "time"))
            # Compute norm for butterfly plot (n_sources, n_times)
            butterfly_data = np.linalg.norm(glass_brain_data, axis=1)
        else:
            # Scalar data - no space dimension
            data_2d = y.get_data(("source", "time"))  # (n_sources, n_times)
            butterfly_data = data_2d.copy()
            # Expand to 3D for consistency (assuming scalar represents magnitude)
            glass_brain_data = data_2d[:, np.newaxis, :]  # (n_sources, 1, n_times)

        return BrainData(
            glass_brain_data=glass_brain_data,
            butterfly_data=butterfly_data,
            source_coords=source_coords,
            time_values=time_values,
            source_space=source_space,
            parcellation=parcellation,
        )

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

    def _calculate_view_ranges(
        self, source_coords: Optional[np.ndarray], brain_views: List[str]
    ) -> Dict[str, Dict[str, List[float]]]:
        """Calculate fixed axis ranges for each brain view to prevent size changes.

        This ensures that brain plots maintain consistent size across all time points.
        """
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

            view_ranges[view_name] = {
                "x": [x_min - x_padding, x_max + x_padding],
                "y": [y_min - y_padding, y_max + y_padding],
            }

        return view_ranges

    def _unify_view_sizes_for_jupyter(
        self, view_ranges: Dict[str, Dict[str, List[float]]]
    ) -> Dict[str, Dict[str, List[float]]]:
        """Unify view sizes for Jupyter mode to ensure consistent display.

        This method adjusts all brain view ranges to have the same width and height,
        making them appear uniform in size when displayed in Jupyter notebooks.
        Only called when using show_in_jupyter().
        """
        if not view_ranges:
            return {}

        # Calculate the maximum width and height across all views
        max_x_width = max(r["x"][1] - r["x"][0] for r in view_ranges.values())
        max_y_width = max(r["y"][1] - r["y"][0] for r in view_ranges.values())

        # Use the larger of the two to ensure square-ish plots with equal sizing
        max_width = max(max_x_width, max_y_width)

        # Update all views to use the unified maximum range
        unified_ranges: Dict[str, Dict[str, List[float]]] = {}

        for view_name, ranges in view_ranges.items():
            # Get current center
            x_center = (ranges["x"][0] + ranges["x"][1]) / 2
            y_center = (ranges["y"][0] + ranges["y"][1]) / 2

            # Set new range centered around the same point with max width
            unified_ranges[view_name] = {
                "x": [x_center - max_width / 2, x_center + max_width / 2],
                "y": [y_center - max_width / 2, y_center + max_width / 2],
            }

        return unified_ranges

    def _calculate_global_colormap_range(
        self, glass_brain_data: Optional[np.ndarray], user_vmax: Optional[float]
    ) -> Tuple[float, float]:
        """Calculate global min/max activity across all time points for fixed colormap.

        This ensures consistent color mapping across time, making it easier to
        compare activity levels at different time points.
        """
        data_max = 1.0

        if glass_brain_data is not None:
            # Calculate activity magnitude across all time points
            if glass_brain_data.ndim == 3:  # Vector data (n_sources, 3, n_times)
                # Compute norm for each source at each time point
                all_magnitudes = np.linalg.norm(
                    glass_brain_data, axis=1
                )  # (n_sources, n_times)
            else:  # Scalar data (n_sources, n_times)
                all_magnitudes = glass_brain_data

            data_max = float(np.max(all_magnitudes))

        # Apply user overrides if provided
        global_vmin = 0.0
        global_vmax = data_max if user_vmax is None else float(user_vmax)

        # Ensure we have a valid range (avoid zero range)
        if global_vmax - global_vmin < 1e-10:
            global_vmax = global_vmin + 1.0

        return global_vmin, global_vmax
