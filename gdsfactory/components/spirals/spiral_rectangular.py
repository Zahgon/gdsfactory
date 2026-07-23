from __future__ import annotations

__all__ = ["spiral_rectangular"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["spirals"])
def spiral_rectangular(
    n_turns: int = 4,
    width: float = 1.0,
    start_length: float = 10.0,
    pitch: float = 3.0,
    layer: LayerSpec = "WG",
) -> Component:
    pass


if __name__ == "__main__":
    c = spiral_rectangular()
    c.show()
