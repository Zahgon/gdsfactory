from __future__ import annotations

__all__ = ["C"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec, Size


@gf.cell_with_module_name(tags=["shapes"])
def C(
    width: float = 1.0,
    size: Size = (10.0, 20.0),
    layer: LayerSpec = "WG",
    port_type: str = "electrical",
) -> Component:
    pass
