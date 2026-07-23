
from __future__ import annotations

__all__ = ["ytron_round"]

import numpy as np
from numpy import cos, pi, sin

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["superconductors"])
def ytron_round(
    rho: float = 1,
    arm_lengths: tuple[float, float] = (500, 300),
    source_length: float = 500,
    arm_widths: tuple[float, float] = (200, 200),
    theta: float = 2.5,
    theta_resolution: float = 10,
    layer: LayerSpec = "WG",
) -> Component:
    pass


if __name__ == "__main__":
    c = ytron_round()
    c.show()
