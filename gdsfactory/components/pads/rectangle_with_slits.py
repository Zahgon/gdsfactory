from __future__ import annotations

__all__ = ["rectangle_with_slits"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec, Size


@gf.cell_with_module_name(tags=["pads"])
def rectangle_with_slits(
    size: Size = (100.0, 200.0),
    layer: LayerSpec = "WG",
    layer_slit: LayerSpec | None = None,
    centered: bool = False,
    port_type: str | None = None,
    slit_size: Size = (1.0, 1.0),
    slit_column_pitch: float = 20,
    slit_row_pitch: float = 20,
    slit_enclosure: float = 10,
) -> Component:
    pass
