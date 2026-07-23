from __future__ import annotations

__all__ = ["cross"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["shapes"])
def cross(
    length: float = 10.0,
    width: float = 3.0,
    layer: LayerSpec = "WG",
    port_type: str | None = None,
) -> Component:
    pass
