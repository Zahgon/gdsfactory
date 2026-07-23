from __future__ import annotations

__all__ = ["circle"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["shapes"])
def circle(
    radius: float = 10.0,
    angle_resolution: float = 2.5,
    layer: LayerSpec = "WG",
) -> Component:
    pass
