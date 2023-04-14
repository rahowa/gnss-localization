import numpy as np
from typing import List, Union
from gnss_localization.projection_matrix import build_projection_matrix


class GNSSProjectionEstimator:
    def __init__(self, offset_x: float, offset_y: float, offset_z: float) -> None:
        """Calculates the projection of GNSS module on moving plane.

        Args:
            offset_x (float): Offset of the origin of GNSS module in X direction from
            the centre of moving plane
            offset_y (float): Offset of the origin of GNSS module in Y direction from
            the centre of moving plane
            offset_z (float): Offset of the origin of GNSS module in Z direction from
            the centre of moving plane (height)
        """
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.offset_z = offset_z

        self.gnss_vector = np.array([offset_x, offset_y, offset_z]).reshape(-1, 1)

    def predict(self, inputs: Union[np.ndarray, List[float]]) -> np.ndarray:
        """Predict GNSS position for certain point/array of points

        Args:
            inputs (Union[np.ndarray, List[float]]): Single data point in format
            (x, y, z, roll, pitch, yaw) or array of these points

        Raises:
            AssertionError: If input schema unsupported
            ValueError: Wrong input type

        Returns:
            np.ndarray: Array of (x, y, z) coordinates of GNSS module
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

        gnss_coordinates = np.asanyarray(
            [
                build_projection_matrix(roll, pitch, yaw) @ self.gnss_vector
                for _, _, _, roll, pitch, yaw in inputs
            ]
        ).reshape(-1, 3)
        return gnss_coordinates
