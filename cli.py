from pathlib import Path
from typing import Optional, Tuple
import typer
import numpy as np
import pandas as pd

from gnss_localization.heading_estimator import GNSSHeadingEstimator
from gnss_localization.projection_estimator import GNSSProjectionEstimator
from gnss_localization.coordinates_estimator import GNSSVehicleCoordinatesEstimator
from gnss_localization.visualizations import plot_headings, animate_projections

app = typer.Typer()


@app.command("proj")
def compute_projections(
    data_path: Path = typer.Option(
        Path("./data.csv"), "--data", help="Path to file with moving data"
    ),
    output_path: Optional[Path] = typer.Option(
        None, "--output", help="Path to results"
    ),
    no_x: bool = typer.Option(
        False,
        "--no-x",
        help="Creates a zero valued column for X coordinate if X is unavailable",
    ),
    no_y: bool = typer.Option(
        False,
        "--no-y",
        help="Creates a zero valued column for Y coordinate if Y is unavailable",
    ),
    no_z: bool = typer.Option(
        True,
        "--no-z",
        help="Creates a zero valued column for Z coordinate if Z is unavailable",
    ),
    no_roll: bool = typer.Option(
        False,
        "--no-roll",
        help="Creates a zero valued column for roll angle if roll is unavailable",
    ),
    no_pitch: bool = typer.Option(
        False,
        "--no-pitch",
        help="Creates a zero valued column for pitch angle if pitch is unavailable",
    ),
    no_yaw: bool = typer.Option(
        True,
        "--no-yaw",
        help="Creates a zero valued column for yaw angle if yaw is unavailable",
    ),
    offset_x: float = typer.Option(
        0,
        "--offset-x",
        help="Ofset of the GNSS modyle by X axis from the center of the vehicle",
    ),
    offset_y: float = typer.Option(
        0,
        "--offset-x",
        help="Ofset of the GNSS modyle by Y axis from the center of the vehicle",
    ),
    offset_z: float = typer.Option(
        1500,
        "--offset-x",
        help="Ofset of the GNSS modyle by Z axis from the center of the vehicle",
    ),
    visualize: bool = typer.Option(
        True, "--visualize", help="Write visualization on disk"
    ),
):
    data = pd.read_csv(str(data_path))
    if no_x:
        data["x_mm"] = np.zeros(len(data))
    if no_y:
        data["y_mm"] = np.zeros(len(data))
    if no_z:
        data["z_mm"] = np.zeros(len(data))

    if no_roll:
        data["roll_deg"] = np.zeros(len(data))
    if no_pitch:
        data["pitch_deg"] = np.zeros(len(data))
    if no_yaw:
        data["yaw_deg"] = np.zeros(len(data))

    data = data[["x_mm", "y_mm", "z_mm", "roll_deg", "pitch_deg", "yaw_deg"]]

    if data.values.mean() == 0.0:
        typer.echo("Warning! Your data is all zero! Nothign to process")
        typer.Exit(-1)

    data["roll_deg"] = np.deg2rad(data["roll_deg"])
    data["pitch_deg"] = np.deg2rad(data["pitch_deg"])
    data["yaw_deg"] = np.deg2rad(data["yaw_deg"])

    proj_estimator = GNSSProjectionEstimator(
        offset_x=offset_x, offset_y=offset_y, offset_z=offset_z
    )

    projections = proj_estimator.predict(data.values)
    projections_df = pd.DataFrame(projections, columns=["x_mm", "y_mm", "z_mm"])
    projections_df.to_csv(str(output_path or data_path.name), index=False)

    if visualize:
        animation = animate_projections(projections)
        animation.save("projections.gif")


@app.command("heading")
def compute_headings(
    data_path: Path = typer.Option(
        Path("./data.csv"), "--data", help="Path to file with moving data"
    ),
    output_path: Optional[Path] = typer.Option(
        None, "--output", help="Path to results"
    ),
    no_x: bool = typer.Option(
        False,
        "--no-x",
        help="Creates a zero valued column for X coordinate if X is unavailable",
    ),
    no_y: bool = typer.Option(
        False,
        "--no-y",
        help="Creates a zero valued column for Y coordinate if Y is unavailable",
    ),
    no_z: bool = typer.Option(
        True,
        "--no-z",
        help="Creates a zero valued column for Z coordinate if Z is unavailable",
    ),
    no_roll: bool = typer.Option(
        False,
        "--no-roll",
        help="Creates a zero valued column for roll angle if roll is unavailable",
    ),
    no_pitch: bool = typer.Option(
        False,
        "--no-pitch",
        help="Creates a zero valued column for pitch angle if pitch is unavailable",
    ),
    no_yaw: bool = typer.Option(
        True,
        "--no-yaw",
        help="Creates a zero valued column for yaw angle if yaw is unavailable",
    ),
    offset_x: float = typer.Option(
        0,
        "--offset-x",
        help="Ofset of the GNSS modyle by X axis from the center of the vehicle",
    ),
    offset_y: float = typer.Option(
        0,
        "--offset-x",
        help="Ofset of the GNSS modyle by Y axis from the center of the vehicle",
    ),
    offset_z: float = typer.Option(
        1500,
        "--offset-x",
        help="Ofset of the GNSS modyle by Z axis from the center of the vehicle",
    ),
    north_direction: Tuple[float, float, float] = typer.Option(
        (None, None, None),
        "--north",
        help="Vector of north direction. If None the north computer from vehicle"
        " main direction",
    ),
    visualize: bool = typer.Option(
        True, "--visualize", help="Write visualization on disk"
    ),
):
    data = pd.read_csv(str(data_path))
    print("HERE")
    if no_x:
        data["x_mm"] = np.zeros(len(data))
    if no_y:
        data["y_mm"] = np.zeros(len(data))
    if no_z:
        data["z_mm"] = np.zeros(len(data))

    if no_roll:
        data["roll_deg"] = np.zeros(len(data))
    if no_pitch:
        data["pitch_deg"] = np.zeros(len(data))
    if no_yaw:
        data["yaw_deg"] = np.zeros(len(data))

    data = data[["x_mm", "y_mm", "z_mm", "roll_deg", "pitch_deg", "yaw_deg"]]

    if data.values.mean() == 0.0:
        typer.echo("Warning! Your data is all zero! Nothign to process")
        typer.Exit(-1)

    data["roll_deg"] = np.deg2rad(data["roll_deg"])
    data["pitch_deg"] = np.deg2rad(data["pitch_deg"])
    data["yaw_deg"] = np.deg2rad(data["yaw_deg"])

    if any(d is None for d in north_direction):
        north_direction = None

    coord_estimator = GNSSVehicleCoordinatesEstimator(offset_x, offset_y, offset_z)
    heading_estimator = GNSSHeadingEstimator(
        offset_x=offset_x,
        offset_y=offset_y,
        offset_z=offset_z,
        north_direction=north_direction,
    )

    vehicle_coordinates = coord_estimator.predict(data.values)
    headings = heading_estimator.predict(vehicle_coordinates)
    headings_df = pd.DataFrame(headings, columns=["angle"])
    headings_df.to_csv(str(output_path or data_path.name), index=False)

    if visualize:
        fig = plot_headings(vehicle_coordinates, headings)
        fig.savefig("headings.png")


if __name__ == "__main__":
    app()
