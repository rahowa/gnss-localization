import numpy as np


def build_projection_matrix(roll: float, pitch: float, yaw: float) -> np.ndarray:
    """Projection matrix for provided Euler agles

    Args:
        roll (float): Rotation around X axis in radians
        pitch (float): Rotation around Y axis in radians
        yaw (float): Rotation around X axis in radians

    Returns:
        np.ndarray: Projection matrix with rotation coeffs
    """
    return (
        np.array(
            [
                [1, 0, 0],
                [0, np.cos(roll), np.sin(roll)],
                [0, -np.sin(roll), np.cos(roll)],
            ]
        )
        @ np.array(
            [
                [np.cos(pitch), 0, np.sin(pitch)],
                [0, 1, 0],
                [-np.sin(pitch), 0, np.cos(pitch)],
            ]
        )
        @ np.array(
            [
                [np.cos(yaw), np.sin(yaw), 0],
                [-np.sin(yaw), np.cos(yaw), 0],
                [0, 0, 1],
            ]
        )
    )
