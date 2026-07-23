from __future__ import annotations

__all__ = ["spiral_archimedes"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["spirals"])
def spiral_archimedes(
    width: float = 1.0,
    n_turns: int = 5,
    separation: float = 2.0,
    angle_resolution: float = 2.0,
    layer: LayerSpec = "WG",
) -> Component:
    pass


if __name__ == "__main__":
    c = spiral_archimedes()
    c.show()
