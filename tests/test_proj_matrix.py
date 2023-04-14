import pytest
import numpy as np

from gnss_localization.projection_matrix import build_projection_matrix


@pytest.fixture
def data_samples():
    return [
        [9521, -35074, 1000, 3.92, -1.35, 0],
        [0, -34970, 1500, 3.93, -1.22, 100],
        [9365, 34853, 0, 3.85, -1.24, 1],
        [-9291, 0, -1000, 3.85, -1.12, -1],
    ]


def from_rotations(z, angle_x, angle_y):
    x_coord = z * np.cos(np.deg2rad(90 - angle_x))  # rotate around Y axis
    z_proj = z * np.sin(
        np.deg2rad(-90 - angle_x)
    )  # porjection on Z axis after rotation around Y
    y_coord = z_proj * np.cos(
        np.deg2rad(-90 - angle_y)
    )  # rotate projection a round X axis
    return [x_coord, y_coord]


@pytest.mark.parametrize(
    "coords",
    [
        [0, 0, 0],
        [0, 1, 2],
        [-1, 2, -3],
        [1, -1, 1],
    ],
)
def test_matrix_projection(coords, data_samples):
    A = np.array([0, 0, coords[2]]).reshape(-1, 1)
    coords_from_triangles = np.asanyarray(
        [from_rotations(coords[2], p, r) for _, _, _, r, p, _ in data_samples]
    )
    coords_from_matrix = np.asanyarray(
        [
            build_projection_matrix(np.deg2rad(r), np.deg2rad(p), 0) @ A
            for _, _, _, r, p, _ in data_samples
        ]
    ).reshape(-1, 3)
    assert np.mean(coords_from_matrix[:, :2] - coords_from_triangles) < 1e-8
