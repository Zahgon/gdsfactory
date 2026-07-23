from __future__ import annotations

__all__ = [
    "grating_coupler_elliptical",
    "grating_coupler_elliptical_te",
    "grating_coupler_elliptical_tm",
]

from functools import partial

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.functions import DEG2RAD
from gdsfactory.typings import CrossSectionSpec, LayerSpec

from .._schematic import grating_coupler_schematic
from ..grating_couplers.functions import (
    grating_taper_points,
    grating_tooth_points,
)


@gf.cell_with_module_name(
    schematic_function=grating_coupler_schematic, tags=["grating_couplers"]
)
def grating_coupler_elliptical(
    polarization: str = "te",
    taper_length: float = 16.6,
    taper_angle: float = 40.0,
    wavelength: float = 1.554,
    fiber_angle: float = 15.0,
    grating_line_width: float = 0.343,
    neff: float = 2.638,  # tooth effective index
    nclad: float = 1.443,
    n_periods: int = 30,
    big_last_tooth: bool = False,
    layer_slab: LayerSpec | None = "SLAB150",
    slab_xmin: float = -1.0,
    slab_offset: float = 2.0,
    spiked: bool = True,
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass


grating_coupler_elliptical_tm = partial(
    grating_coupler_elliptical,
    grating_line_width=0.707,
    polarization="tm",
    taper_length=30,
    slab_xmin=-2,
    neff=1.8,
    n_periods=16,
)


grating_coupler_elliptical_te = grating_coupler_elliptical
