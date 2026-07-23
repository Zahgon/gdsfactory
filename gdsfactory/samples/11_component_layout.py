
from __future__ import annotations

import gdsfactory as gf
from gdsfactory.component import Component

gf.gpdk.PDK.activate()


@gf.cell
def crossing_arm(
    wg_width: float = 0.5,
    r1: float = 3.0,
    r2: float = 1.1,
    taper_width: float = 1.2,
    taper_length: float = 3.4,
) -> Component:
    pass


if __name__ == "__main__":
    c = crossing_arm()
    c.show()
