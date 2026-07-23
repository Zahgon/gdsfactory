from __future__ import annotations

__all__ = ["ellipse"]

import numpy as np
from numpy import cos, pi, sin, sqrt

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["shapes"])
def ellipse(
    radii: tuple[float, float] = (10.0, 5.0),
    angle_resolution: float = 2.5,
    layer: LayerSpec = "WG",
) -> Component:
    pass
