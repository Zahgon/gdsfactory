from __future__ import annotations

__all__ = ["gear"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["mems"])
def gear(
    n_teeth: int = 20,
    module_size: float = 2.0,
    pressure_angle: float = 20.0,
    hub_radius: float | None = None,
    hub_hole_radius: float = 0.0,
    layer: LayerSpec = "WG",
) -> Component:
    pass


if __name__ == "__main__":
    c = gear()
    c.show()
