from __future__ import annotations

__all__ = ["folded_spring"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["mems"])
def folded_spring(
    beam_width: float = 0.5,
    beam_length: float = 20.0,
    n_folds: int = 4,
    fold_gap: float = 1.0,
    anchor_width: float = 5.0,
    anchor_length: float = 3.0,
    layer: LayerSpec = "WG",
    port_type: str = "electrical",
) -> Component:
    pass


if __name__ == "__main__":
    c = folded_spring()
    c.show()
