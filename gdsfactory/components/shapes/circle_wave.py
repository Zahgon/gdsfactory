from __future__ import annotations

__all__ = ["circle_wave"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["shapes"])
def circle_wave(
    radius: float = 10.0,
    amplitude: float = 1.0,
    n_oscillations: int = 8,
    angle_resolution: float = 1.0,
    layer: LayerSpec = "WG",
) -> Component:
    pass


if __name__ == "__main__":
    c = circle_wave()
    c.show()
