import numpy as np
import gnss_localization as gnssl

gnss_coordinates = [
    [1621693264.0155628, 9521, -35074, 3.92, -1.35],
    [1621693264.1979840, 9450, -34970, 3.93, -1.22],
    [1621693264.4237902, 9365, -34853, 3.85, -1.24],
    [1621693264.6384845, 9291, -34759, 3.85, -1.12],
]

estimator = gnssl.GNSSProjectionEstimator(
    offset_x=0.0,
    offset_y=0.0,
    offset_z=1500.0,
)

projection = [
    estimator.predict([x, y, 0, pitch, roll, 0])
    for (_, x, y, roll, pitch) in gnss_coordinates
]
print(projection)  # [[], [] ... ]


coord_estimator = gnssl.GNSSVehicleCoordinatesEstimator(
    offset_x=0.0,
    offset_y=0.0,
    offset_z=1500.0,
)
vehicle_coordinates = [
    coord_estimator.predict([x, y, 0, pitch, roll, 0])
    for (_, x, y, roll, pitch) in gnss_coordinates
]
print(vehicle_coordinates)

estimator = gnssl.GNSSHeadingEstimator(
    offset_x=0.0, offset_y=0.0, offset_z=1500.0, north_direction=(0, 1, 0)
)
heading = estimator.predict(np.asanyarray(vehicle_coordinates).reshape(-1, 3))
print(heading) [43.02760911 55.47551315 50.60675111]
