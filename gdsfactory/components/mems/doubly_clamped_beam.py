from __future__ import annotations

__all__ = ["doubly_clamped_beam"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["mems"])
def doubly_clamped_beam(
    beam_width: float = 1.0,
    beam_length: float = 30.0,
    anchor_width: float = 5.0,
    anchor_length: float = 5.0,
    layer: LayerSpec = "WG",
    port_type: str = "electrical",
) -> Component:
    pass


if __name__ == "__main__":
    c = doubly_clamped_beam()
    c.show()
