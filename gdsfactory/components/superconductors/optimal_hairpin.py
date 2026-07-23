from __future__ import annotations

__all__ = ["optimal_hairpin"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.snap import snap_to_grid
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["superconductors"])
def optimal_hairpin(
    width: float = 0.2,
    pitch: float = 0.6,
    length: float = 10,
    turn_ratio: float = 4,
    num_pts: int = 50,
    layer: LayerSpec = (1, 0),
) -> Component:
    pass
