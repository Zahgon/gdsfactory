from __future__ import annotations

__all__ = ["L"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["shapes"])
def L(
    width: int | float = 1,
    size: tuple[int, int] = (10, 20),
    layer: LayerSpec = "MTOP",
    port_type: str = "electrical",
) -> Component:
    pass
