from __future__ import annotations

__all__ = ["rect_taper"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["shapes"])
def rect_taper(
    rect_width: float = 1.0,
    rect_length: float = 10.0,
    taper_length: float = 5.0,
    taper_width: float = 4.0,
    layer: LayerSpec = "WG",
    port_type: str | None = "optical",
) -> Component:
    pass


if __name__ == "__main__":
    c = rect_taper()
    c.show()
