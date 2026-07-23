from __future__ import annotations

__all__ = ["polarization_splitter_rotator"]

from typing import Any

import numpy as np
import numpy.typing as npt

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import CrossSectionSpec, Delta, Float2, Float3

from ..bends.bend_s import bezier


@gf.cell_with_module_name(tags=["filters"])
def polarization_splitter_rotator(
    width_taper_in: Float3 = (0.54, 0.69, 0.83),
    length_taper_in: Float2 | Float3 = (4.0, 44.0),
    width_coupler: Float2 = (0.9, 0.404),
    length_coupler: float = 7.0,
    gap: float = 0.15,
    width_out: float = 0.54,
    length_out: float = 14.33,
    dy: Delta = 5.0,
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass
