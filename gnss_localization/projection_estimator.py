import numpy as np
from typing import List, Union


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

    def predict(self, inputs: Union[np.ndarray, List[float]]) -> np.ndarray:
        pass
