from __future__ import annotations

__all__ = ["hline"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["superconductors"])
def hline(
    length: float = 10.0,
    width: float = 0.5,
    layer: LayerSpec = "WG",
    port_type: str = "optical",
) -> Component:
    pass
