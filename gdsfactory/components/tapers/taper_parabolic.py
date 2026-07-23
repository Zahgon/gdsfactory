from __future__ import annotations

__all__ = ["taper_parabolic"]

import numpy as np

import gdsfactory as gf
from gdsfactory.path import transition_exponential
from gdsfactory.typings import LayerSpec

from .._schematic import taper_schematic


@gf.cell_with_module_name(schematic_function=taper_schematic, tags=["tapers"])
def taper_parabolic(
    length: float = 20,
    width1: float = 0.5,
    width2: float = 5.0,
    exp: float = 0.5,
    npoints: int = 100,
    layer: LayerSpec = "WG",
) -> gf.Component:
    pass
