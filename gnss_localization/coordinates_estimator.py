import numpy as np
from typing import List, Optional, Tuple, Union

from gnss_localization.projection_estimator import GNSSProjectionEstimator
from gnss_localization.projection_matrix import build_projection_matrix


class GNSSVehicleCoordinatesEstimator:
    def __init__(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
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
        self.proj_estimator = GNSSProjectionEstimator(offset_x, offset_y, offset_z)

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

    def predict(self, inputs: Union[np.ndarray, List[float]]) -> np.ndarray:
        """Computes the vehicle coordinates for each GNSS point

        Args:
            inputs (Union[np.ndarray, List[float]]): Single data point in format
            (x, y, z, roll, pitch, yaw) or array of these points

        Raises:
            AssertionError: If input schema unsupported
            ValueError: Wrong input type

        Returns:
            np.ndarray: Vehicle coordinates
        """
        if isinstance(inputs, (list, tuple)):
            assert (
                len(inputs) == 6
            ), "Input must contain 6 elements: (x, y, z, roll, pitch, yaw)"
            inputs = np.array([list(inputs)]).reshape(-1, 6)
        elif isinstance(inputs, np.ndarray):
            assert (
                inputs.shape[1] == 6
            ), "Input must contain 6 elements: (x, y, z, roll, pitch, yaw)"
            assert len(inputs.shape) == 2, "Input must have shape Nx6"
        else:
            raise ValueError(
                "Wrong input type. Possible options are list of 6 elements or numpy"
                " array of shape Nx6"
            )
        gnss_coordinates = self.proj_estimator.predict(inputs)
        vehicle_coordinates = np.asanyarray(
            [
                build_projection_matrix(0, 0, 0) @ (plane_coordinates - gnss_coords)
                for gnss_coords, plane_coordinates in zip(
                    gnss_coordinates, inputs[:, :3]
                )
            ]
        )
        return vehicle_coordinates
