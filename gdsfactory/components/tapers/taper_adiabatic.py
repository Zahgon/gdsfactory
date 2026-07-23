from __future__ import annotations

__all__ = ["taper_adiabatic"]

from collections.abc import Callable
from typing import Any

import numpy as np
import numpy.typing as npt

import gdsfactory as gf
from gdsfactory.path import transition_adiabatic
from gdsfactory.typings import CrossSectionSpec

from .._schematic import taper_schematic


def neff_TE1550SOI_220nm(w: float) -> float:
    pass


@gf.cell_with_module_name(schematic_function=taper_schematic, tags=["tapers"])
def taper_adiabatic(
    width1: float = 0.5,
    width2: float = 5.0,
    length: float = 0,
    neff_w: Callable[[float], float] = neff_TE1550SOI_220nm,
    alpha: float = 1,
    wavelength: float = 1.55,
    npoints: int = 200,
    cross_section: CrossSectionSpec = "strip",
    max_length: float = 200,
) -> gf.Component:
    pass
