from __future__ import annotations

__all__ = ["nxn"]

from typing import Any

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["shapes"])
def nxn(
    west: int = 1,
    east: int = 4,
    north: int = 0,
    south: int = 0,
    xsize: float = 8.0,
    ysize: float = 8.0,
    wg_width: float = 0.5,
    layer: LayerSpec = "WG",
    wg_margin: float = 1.0,
    **kwargs: Any,
) -> Component:
    pass
