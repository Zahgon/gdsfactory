from __future__ import annotations

__all__ = ["torus"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["shapes"])
def torus(
    inner_radius: float = 5.0,
    outer_radius: float = 10.0,
    start_angle: float = 0.0,
    end_angle: float = 360.0,
    angle_resolution: float = 2.5,
    layer: LayerSpec = "WG",
    port_type: str | None = None,
) -> Component:
    pass


if __name__ == "__main__":
    c = torus()
    c.show()
