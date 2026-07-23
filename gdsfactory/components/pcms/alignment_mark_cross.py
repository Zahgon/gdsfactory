from __future__ import annotations

__all__ = ["alignment_mark_cross"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["pcms"])
def alignment_mark_cross(
    arm_width: float = 2.0,
    arm_length: float = 20.0,
    layer: LayerSpec = "WG",
    port_type: str | None = None,
) -> Component:
    pass


if __name__ == "__main__":
    c = alignment_mark_cross()
    c.show()
