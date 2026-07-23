from __future__ import annotations

__all__ = [
    "grating_coupler_elliptical_arbitrary",
    "grating_coupler_elliptical_uniform",
]

from typing import Any

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.functions import DEG2RAD
from gdsfactory.typings import CrossSectionSpec, Floats, LayerSpec

from .._schematic import grating_coupler_schematic
from ..grating_couplers.functions import (
    grating_taper_points,
    grating_tooth_points,
)

_gaps = (0.1,) * 10
_widths = (0.5,) * 10


@gf.cell_with_module_name(
    schematic_function=grating_coupler_schematic, tags=["grating_couplers"]
)
def grating_coupler_elliptical_arbitrary(
    gaps: Floats = _gaps,
    widths: Floats = _widths,
    taper_length: float = 16.6,
    taper_angle: float = 60.0,
    wavelength: float = 1.554,
    fiber_angle: float = 15.0,
    nclad: float = 1.443,
    layer_slab: LayerSpec | None = "SLAB150",
    layer_grating: LayerSpec | None = None,
    taper_to_slab_offset: float = -3.0,
    polarization: str = "te",
    spiked: bool = True,
    bias_gap: float = 0,
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass


@gf.cell_with_module_name(
    schematic_function=grating_coupler_schematic, tags=["grating_couplers"]
)
def grating_coupler_elliptical_uniform(
    n_periods: int = 20,
    period: float = 0.75,
    fill_factor: float = 0.5,
    **kwargs: Any,
) -> Component:
    pass
