
from __future__ import annotations

__all__ = ["die"]

import numpy as np

import gdsfactory as gf
from gdsfactory.typings import ComponentSpec, Float2, LayerSpec, Size


@gf.cell_with_module_name(tags=["dies"])
def die(
    size: Size = (10000.0, 10000.0),
    street_width: float = 100.0,
    street_length: float = 1000.0,
    die_name: str | None = "chip99",
    text_size: float = 100.0,
    text_location: str | Float2 = "SW",
    layer: LayerSpec | None = "FLOORPLAN",
    bbox_layer: LayerSpec | None = "FLOORPLAN",
    text_layer: LayerSpec = "WG",
    text: ComponentSpec = "text",
    draw_corners: bool = False,
) -> gf.Component:
    pass
