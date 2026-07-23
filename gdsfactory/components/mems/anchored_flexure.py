from __future__ import annotations

__all__ = ["anchored_flexure"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["mems"])
def anchored_flexure(
    hinge_width: float = 0.3,
    hinge_length: float = 5.0,
    pad_width: float = 10.0,
    pad_length: float = 10.0,
    layer: LayerSpec = "WG",
    port_type: str = "electrical",
) -> Component:
    pass


if __name__ == "__main__":
    c = anchored_flexure()
    c.show()
