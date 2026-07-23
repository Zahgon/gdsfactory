from __future__ import annotations

__all__ = ["hexagon", "octagon", "regular_polygon"]

from functools import partial

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["shapes"])
def regular_polygon(
    sides: int = 6,
    side_length: float = 10,
    layer: LayerSpec = "WG",
    port_width: float
    | None = None,  # port width doesn't need to be side length all the time
    port_type: str | None = "placement",
) -> Component:
    pass


hexagon = partial(regular_polygon, sides=6)
octagon = partial(regular_polygon, sides=8)
