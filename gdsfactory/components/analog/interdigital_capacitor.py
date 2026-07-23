from __future__ import annotations

__all__ = ["interdigital_capacitor"]

from itertools import chain
from math import ceil, floor

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec

from .._schematic import capacitor_schematic


@gf.cell_with_module_name(schematic_function=capacitor_schematic, tags=["analog"])
def interdigital_capacitor(
    fingers: int = 4,
    finger_length: float | int = 20.0,
    finger_gap: float | int = 2.0,
    thickness: float | int = 5.0,
    layer: LayerSpec = "WG",
) -> Component:
    pass
