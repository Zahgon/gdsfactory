from __future__ import annotations

__all__ = ["pie_arc"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["shapes"])
def pie_arc(
    radius: float = 10.0,
    radius_y: float | None = None,
    start_angle: float = 0.0,
    end_angle: float = 90.0,
    angle_resolution: float = 2.5,
    layer: LayerSpec = "WG",
) -> Component:
    pass


if __name__ == "__main__":
    c = pie_arc()
    c.show()
