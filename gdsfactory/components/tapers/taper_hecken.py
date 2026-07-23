
from __future__ import annotations

__all__ = ["taper_hecken"]

import numpy as np
from numpy import log

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec

from .._schematic import taper_schematic
from ..analog.microstrip import (
    _G,
    _find_microstrip_wire_width,
    _microstrip_v_with_Lk,
    _microstrip_Z_with_Lk,
)


@gf.cell_with_module_name(schematic_function=taper_schematic, tags=["tapers"])
def taper_hecken(
    length: float = 200,
    B: float = 4.0091,
    dielectric_thickness: float = 0.25,
    eps_r: float = 2,
    Lk_per_sq: float = 250e-12,
    Z1: float | None = 50,
    Z2: float | None = 100,
    width1: float | None = None,
    width2: float | None = None,
    num_pts: int = 100,
    layer: LayerSpec = "WG",
) -> Component:
    pass


if __name__ == "__main__":
    c = taper_hecken(Z1=50, Z2=100)
    c.show()
