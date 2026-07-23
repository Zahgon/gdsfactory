from __future__ import annotations

__all__ = ["spiral_logarithmic"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["spirals"])
def spiral_logarithmic(
    width: float = 0.5,
    n_turns: int = 4,
    a: float = 1.0,
    b: float = 0.1,
    angle_resolution: float = 2.0,
    layer: LayerSpec = "WG",
) -> Component:
    pass


if __name__ == "__main__":
    c = spiral_logarithmic()
    c.show()
