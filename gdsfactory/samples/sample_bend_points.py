
from __future__ import annotations

import numpy as np

import gdsfactory as gf

gf.gpdk.PDK.activate()


if __name__ == "__main__":
    radius = 5.0
    target_spacing_um = 1.0  # 1 um between points
    angular_step = target_spacing_um / radius * (180 / np.pi)

    c = gf.Component()

    b1 = c << gf.components.bend_circular(
        radius=radius, angle=90, angular_step=angular_step
    )

    b2 = c << gf.components.bend_euler(
        radius=radius, angle=90, angular_step=angular_step
    )
    b2.movex(20)

    c.show()
