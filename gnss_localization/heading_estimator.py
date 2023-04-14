import numpy as np
from typing import List, Optional, Tuple, Union

from gnss_localization.projection_estimator import GNSSProjectionEstimator
from gnss_localization.projection_matrix import build_projection_matrix
from gnss_localization.coordinates_estimator import GNSSVehicleCoordinatesEstimator


class GNSSHeadingEstimator:
    def __init__(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        north_direction: Optional[Tuple[float, float, float]],
    ) -> None:
        """Calculates the heading of body using data from GNSS module.

        Args:
            offset_x (float): Offset of the origin of GNSS module in X direction from
            the centre of moving plane
            offset_y (float): Offset of the origin of GNSS module in Y direction from
            the centre of moving plane
            offset_z (float): Offset of the origin of GNSS module in Z direction from
            the centre of moving plane (height)
            north_direction (Optional[Tuple[float, float, float]]): Basis vector of
            north direction. If None the vector would be computed from moving plane data
        """

        self.offset_x = offset_x
        self.offset_y = offset_y
        self.offset_z = offset_z
        self.north_vector = north_direction

    def compute_north_from_data(self, data: np.ndarray) -> Tuple[float, float, float]:
        """Compute north direction from data of moving plane

        Args:
            data (np.ndarray): Vehicle movement data (at least x and y coordinates)

        Returns:
            Tuple[float, float, float]: North vector
        """
        north_vector = (data[-1, :2] - data[0, :2]).tolist() + [0]
        north_vector = np.array(north_vector)
        return tuple(north_vector.tolist())

    def predict(
        self, vehicle_coordinates: Union[np.ndarray, List[float]]
    ) -> np.ndarray:
        """Computes the heading angle for each point

        Args:
            vehicle_coordinates (Union[np.ndarray, List[float]]):
            Single data point in format (x, y, z, roll, pitch, yaw) or array of these
            points

        Raises:
            AssertionError: If input schema unsupported
            ValueError: Wrong input type

        Returns:
            np.ndarray: Heading for each point
        """
        if isinstance(vehicle_coordinates, (list, tuple)):
            assert (
                len(vehicle_coordinates) == 3
            ), "Input must contain 3 elements: (x, y, z)"
            vehicle_coordinates = np.array([list(vehicle_coordinates)]).reshape(-1, 6)
        elif isinstance(vehicle_coordinates, np.ndarray):
            assert (
                vehicle_coordinates.shape[1] == 3
            ), "Input must contain 3 elements: (x, y, z)"
            assert len(vehicle_coordinates.shape) == 2, "Input must have shape Nx3"
        else:
            raise ValueError(
                "Wrong input type. Possible options are list of 3 elements or numpy"
                " array of shape Nx3"
            )
        if self.north_vector is None:
            self.north_vector = self.compute_north_from_data(vehicle_coordinates)
        headings_cos = np.array(
            [
                (self.north_vector @ coordinates)
                / (np.linalg.norm(self.north_vector) * np.linalg.norm(coordinates))
                for coordinates in (vehicle_coordinates - vehicle_coordinates[0])
            ]
        )[1:]
        headings = np.arccos(headings_cos)
        headings = np.rad2deg(headings)
        return headings
