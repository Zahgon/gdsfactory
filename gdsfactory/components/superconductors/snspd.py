from __future__ import annotations

__all__ = ["snspd"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec, Port, Size

from ..superconductors.optimal_hairpin import optimal_hairpin


@gf.cell_with_module_name(tags=["superconductors"])
def snspd(
    wire_width: float = 0.2,
    wire_pitch: float = 0.6,
    size: Size = (10, 8),
    num_squares: int | None = None,
    turn_ratio: float = 4,
    terminals_same_side: bool = False,
    layer: LayerSpec = (1, 0),
    port_type: str = "electrical",
) -> Component:
    pass
