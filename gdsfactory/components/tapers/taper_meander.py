
from __future__ import annotations

__all__ = ["taper_meander"]

from math import pi

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec

from .._schematic import taper_schematic


@gf.cell_with_module_name(schematic_function=taper_schematic, tags=["tapers"])
def taper_meander(
    x_taper: tuple[float, ...] | None = None,
    w_taper: tuple[float, ...] | None = None,
    meander_length: float = 1000,
    spacing_factor: float = 3,
    min_spacing: float = 0.5,
    layer: LayerSpec = "WG",
) -> Component:
    pass


if __name__ == "__main__":
    x_taper = (1, 10, 20, 30, 40, 50)
    w_taper = (1, 5, 10, 5, 2, 1)
    c = taper_meander(x_taper=x_taper, w_taper=w_taper)
    c.show()
