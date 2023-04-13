import numpy as np
from typing import List, Tuple, Union

from projection_estimator import GNSSProjectionEstimator


class GNSSHeadingEstimator:
    def __init__(
        self,
        offset_x: float,
        offset_y: float,
        offset_z: float,
        north_direction: Tuple[float, float, float],
    ) -> None:
        """Calculates the heading of body using data from GNSS module.

        Args:
            offset_x (float): Offset of the origin of GNSS module in X direction from 
            the centre of moving plane
            offset_y (float): Offset of the origin of GNSS module in Y direction from
            the centre of moving plane
            offset_z (float): Offset of the origin of GNSS module in Z direction from
            the centre of moving plane (height)
            north_direction (Tuple[float, float, float]): Basis vector of north direction
        """
        
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.offset_z = offset_z
        self.notrh_vector = north_direction
        self.proj_estimator = GNSSProjectionEstimator(offset_x, offset_y, offset_z)

    def predict(self, inputs: Union[np.ndarray, List[float]]) -> np.ndarray:
        pass
