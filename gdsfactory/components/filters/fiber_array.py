from __future__ import annotations

__all__ = ["fiber_array"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec

from ..shapes.circle import circle


@gf.cell_with_module_name(tags=["filters"])
def fiber_array(
    n: int = 8,
    pitch: float = 127.0,
    core_diameter: float = 10,
    cladding_diameter: float = 125,
    layer_core: LayerSpec = "WG",
    layer_cladding: LayerSpec = "WGCLAD",
) -> Component:
    pass
