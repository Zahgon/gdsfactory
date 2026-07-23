from __future__ import annotations

__all__ = ["litho_calipers"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec, Size


@gf.cell_with_module_name(tags=["pcms"])
def litho_calipers(
    notch_size: Size = (2.0, 5.0),
    notch_spacing: float = 2.0,
    num_notches: int = 11,
    offset_per_notch: float = 0.1,
    row_spacing: float = 0.0,
    layer1: LayerSpec = "WG",
    layer2: LayerSpec = "SLAB150",
) -> Component:
    pass


if __name__ == "__main__":
    c = litho_calipers()
    c.show()
