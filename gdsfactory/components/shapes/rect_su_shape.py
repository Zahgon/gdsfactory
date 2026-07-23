from __future__ import annotations

__all__ = ["rect_su_shape"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["shapes"])
def rect_su_shape(
    L1: float = 10.0,
    L2: float = 10.0,
    L3: float = 20.0,
    width: float = 1.0,
    layer: LayerSpec = "WG",
    port_type: str | None = "electrical",
) -> Component:
    pass


if __name__ == "__main__":
    c = rect_su_shape()
    c.show()
