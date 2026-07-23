from __future__ import annotations

__all__ = ["ramp"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec

from .._schematic import taper_schematic


@gf.cell_with_module_name(schematic_function=taper_schematic, tags=["tapers"])
def ramp(
    length: float = 10.0,
    width1: float = 5.0,
    width2: float | None = 8.0,
    layer: LayerSpec = "WG",
) -> Component:
    pass
