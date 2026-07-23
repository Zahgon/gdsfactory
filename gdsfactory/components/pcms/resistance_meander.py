from __future__ import annotations

__all__ = ["resistance_meander"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec, Size


@gf.cell_with_module_name(tags=["pcms"])
def resistance_meander(
    name: str = "net",
    pad_size: Size = (50.0, 50.0),
    num_squares: int = 1000,
    width: float = 1.0,
    res_layer: LayerSpec = "MTOP",
    pad_layer: LayerSpec = "MTOP",
) -> Component:
    pass
