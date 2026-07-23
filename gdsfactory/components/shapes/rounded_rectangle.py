from __future__ import annotations

__all__ = ["rounded_rectangle"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["shapes"])
def rounded_rectangle(
    width: float = 20.0,
    height: float = 10.0,
    corner_radius_x: float = 3.0,
    corner_radius_y: float | None = None,
    n_corner_points: int = 20,
    layer: LayerSpec = "WG",
    port_type: str | None = None,
) -> Component:
    pass


if __name__ == "__main__":
    c = rounded_rectangle()
    c.show()
