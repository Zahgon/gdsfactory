from __future__ import annotations

__all__ = ["torus_wave"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["shapes"])
def torus_wave(
    inner_radius: float = 5.0,
    outer_radius: float = 10.0,
    amplitude: float = 0.5,
    n_oscillations: int = 8,
    in_phase: bool = True,
    angle_resolution: float = 1.0,
    layer: LayerSpec = "WG",
) -> Component:
    pass


if __name__ == "__main__":
    c = torus_wave()
    c.show()
