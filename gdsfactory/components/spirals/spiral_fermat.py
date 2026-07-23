from __future__ import annotations

__all__ = ["spiral_fermat"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["spirals"])
def spiral_fermat(
    width: float = 1.0,
    n_turns: int = 5,
    a: float = 5.0,
    angle_resolution: float = 2.0,
    layer: LayerSpec = "WG",
) -> Component:
    pass


if __name__ == "__main__":
    c = spiral_fermat()
    c.show()
