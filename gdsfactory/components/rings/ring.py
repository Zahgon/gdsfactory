from __future__ import annotations

__all__ = ["ring"]

import numpy as np
from numpy import cos, pi, sin

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["rings"])
def ring(
    radius: float = 10.0,
    width: float = 0.5,
    angle_resolution: float = 2.5,
    layer: LayerSpec = "WG",
    angle: float = 360,
    distance_resolution: float | None = None,
) -> Component:
    pass
