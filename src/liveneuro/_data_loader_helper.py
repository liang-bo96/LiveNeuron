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
    from ._liveneuro import LiveNeuro


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
