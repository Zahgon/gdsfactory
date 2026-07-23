
from __future__ import annotations

import gdsfactory as gf

gf.gpdk.PDK.activate()


if __name__ == "__main__":
    PDK = gf.get_active_pdk()
    radius = 10.0

    PDK.bend_points_distance = 0.1
    b = gf.components.bend_euler(radius=radius, angle=90)
    first_layer = next(iter(b.get_polygons()))
    n = b.get_polygons()[first_layer][0].num_points()
    print(f"bend_points_distance=100nm: {n} polygon points")

    PDK.bend_points_distance = 20e-3

    b.show()
