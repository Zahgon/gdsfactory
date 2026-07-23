from __future__ import annotations

__all__ = ["comb_drive"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["mems"])
def comb_drive(
    finger_width: float = 0.5,
    finger_length: float = 10.0,
    finger_gap: float = 0.5,
    n_fingers: int = 20,
    finger_overlap: float = 5.0,
    shuttle_width: float = 5.0,
    shuttle_length: float = 30.0,
    spring_width: float = 0.5,
    spring_length: float = 20.0,
    n_spring_folds: int = 4,
    anchor_size: float = 10.0,
    layer: LayerSpec = "WG",
) -> Component:
    pass


if __name__ == "__main__":
    c = comb_drive()
    c.show()
