from __future__ import annotations

__all__ = ["optimal_90deg"]

from typing import Any

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["superconductors"])
def optimal_90deg(
    width: float = 100,
    num_pts: int = 15,
    length_adjust: float = 1,
    layer: LayerSpec = (1, 0),
) -> Component:
    pass
