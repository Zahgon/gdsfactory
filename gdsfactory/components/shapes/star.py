from __future__ import annotations

__all__ = ["star"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["shapes"])
def star(
    inner_radius: float = 5.0,
    outer_radius: float = 10.0,
    n_points: int = 5,
    layer: LayerSpec = "WG",
) -> Component:
    pass


if __name__ == "__main__":
    c = star()
    c.show()
