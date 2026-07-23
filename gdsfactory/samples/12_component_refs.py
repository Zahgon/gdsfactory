
from __future__ import annotations

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentFactory, Layer

gf.gpdk.PDK.activate()


@gf.cell
def crossing_arm(
    wg_width: float = 0.5,
    r1: float = 3.0,
    r2: float = 1.1,
    taper_width: float = 1.2,
    taper_length: float = 3.4,
    layer_wg: Layer = (1, 0),
    layer_slab: Layer = (2, 0),
) -> Component:
    pass


@gf.cell
def crossing(
    arm: ComponentFactory = crossing_arm,
    cross_section: str = "strip",
) -> Component:
    pass


if __name__ == "__main__":
    c = crossing()
    c.show()
