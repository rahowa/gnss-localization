from typing import Optional
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.collections import PatchCollection
from matplotlib.figure import Figure
from functools import partial
from matplotlib.animation import FuncAnimation, Animation


def animate_projections(
    gnss_coordinates: np.ndarray,
    i: int = -1,
    fig: Optional[Figure] = None,
    gnss_path_line: Optional[Line2D] = None,
    ghss_head_scatter: Optional[PatchCollection] = None,
    gnss_route_line: Optional[Line2D] = None,
) -> Animation:
    """Build animation of GNSS module movement

    Args:
        gnss_coordinates (np.ndarray): Coordinates of GNSS module
        i (int, optional): Index of current animation frame. Defaults to -1.
        fig (Optional[Figure], optional): Matplotlib  figure. Defaults to None.
        gnss_path_line (Optional[Line2D], optional): Matplotlib line for GNSS path. Defaults to None.
        ghss_head_scatter (Optional[PatchCollection], optional): Matplotlib scatter fot GNSS head. Defaults to None.
        gnss_route_line (Optional[Line2D], optional): Matplotlib line for GNSS route. Defaults to None.

    Returns:
        Animation: Animation of GNSS module movement
    """
    if i < 0:
        fig = plt.figure()

        (gnss_path_line,) = plt.plot([], [], lw=2, c="c", linestyle="dashed")
        ghss_head_scatter = plt.scatter([], [], c="k", marker="o", s=45)
        (gnss_route_line,) = plt.plot([], [], lw=1, c="k")

        plt.title("GNSS movement over time")
        plt.xlabel("$X$")
        plt.ylabel("$Y$")
        plt.xlim((gnss_coordinates[:, 0].min() - 1, gnss_coordinates[:, 0].max() + 1))
        plt.ylim((gnss_coordinates[:, 1].min() - 1, gnss_coordinates[:, 1].max() + 1))

        gnss_path_line.set_data(gnss_coordinates[:, 0], gnss_coordinates[:, 1])
        return FuncAnimation(
            fig=fig,
            func=partial(
                animate_projections,
                gnss_coordinates,
                fig=fig,
                gnss_path_line=gnss_path_line,
                ghss_head_scatter=ghss_head_scatter,
                gnss_route_line=gnss_route_line,
            ),
            interval=33 * 2,
            blit=True,
            frames=len(gnss_coordinates),
        )
    else:
        x_center = (gnss_coordinates[:, 0].max() + gnss_coordinates[:, 0].min()) // 2
        y_center = (gnss_coordinates[:, 1].max() + gnss_coordinates[:, 1].min()) // 2
        ghss_head_scatter.set_offsets(gnss_coordinates[i, :2])  # update the data.
        gnss_route_line.set_data(
            [x_center, gnss_coordinates[i, 0]], [y_center, gnss_coordinates[i, 1]]
        )
        return (gnss_path_line, ghss_head_scatter, gnss_route_line)  # type: ignore


def plot_headings(
    vehicle_coordinates: np.ndarray, headings: np.ndarray, res_multiplier: float = 5.0
) -> Figure:
    """Plot heading angle for each point and route deviations

    Args:
        vehicle_coordinates (np.ndarray): Coordinates of vehicle
        headings (np.ndarray): Heading angles for each point
        res_multiplier (float, optional): Multiplier for deviations. Defaults to 5.0.

    Returns:
        Figure: Plot of heading angle for each point and route deviations
    """

    vehicle_coordinates = vehicle_coordinates[1:]
    x_perfect = np.linspace(
        vehicle_coordinates[0, 0], vehicle_coordinates[-1, 0], len(vehicle_coordinates)
    )
    y_perfect = np.linspace(
        vehicle_coordinates[0, 1], vehicle_coordinates[-1, 1], len(vehicle_coordinates)
    )
    diff_x = x_perfect - vehicle_coordinates[:, 0]
    diff_y = y_perfect - vehicle_coordinates[:, 1]

    fig, ax1 = plt.subplots()
    ax1.plot(
        vehicle_coordinates[:, 0],
        vehicle_coordinates[:, 1],
        lw=2,
        label="Vehicle coordinates",
    )
    ax1.plot(
        x_perfect - diff_x * res_multiplier,
        y_perfect + diff_y * res_multiplier,
        lw=1,
        linestyle="--",
        label=f"Residuals x{res_multiplier}",
    )
    ax1.arrow(
        vehicle_coordinates[0, 0],
        vehicle_coordinates[0, 1],
        vehicle_coordinates[-1, 0] - vehicle_coordinates[0, 0],
        vehicle_coordinates[-1, 1] - vehicle_coordinates[0, 1],
        # head_width=150,
        # head_length=300,
        fc="k",
        ec="k",
        linestyle="dotted",
        label="North vector",
    )
    ax1.set_xlabel("$X$ coordinate")
    ax1.set_ylabel("$Y$ coordinate")
    ax1.tick_params(axis="y")
    ax2 = ax1.twinx()
    ax2.plot(
        vehicle_coordinates[:, 0], headings, label="Heading angle", c="r", alpha=0.4
    )
    ax2.set_ylabel("$Heading$ angle")
    ax2.tick_params(axis="y")
    fig.tight_layout()
    ax1.legend(loc="best")
    ax2.legend(loc="best")
    ax1.set_title("Global heading")
    return fig
