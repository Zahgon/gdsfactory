from __future__ import annotations

__all__ = ["grating_coupler_rectangular_arbitrary"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import CrossSectionSpec, Floats, LayerSpec

from .._schematic import grating_coupler_schematic
from ..tapers.taper import taper

_gaps = (0.2,) * 10
_widths = (0.5,) * 10


@gf.cell_with_module_name(
    schematic_function=grating_coupler_schematic, tags=["grating_couplers"]
)
def grating_coupler_rectangular_arbitrary(
    gaps: Floats = _gaps,
    widths: Floats = _widths,
    width_grating: float = 11.0,
    length_taper: float = 150.0,
    polarization: str = "te",
    wavelength: float = 1.55,
    layer_grating: LayerSpec | None = None,
    layer_slab: LayerSpec | None = None,
    slab_xmin: float = -1.0,
    slab_offset: float = 1.0,
    fiber_angle: float = 15,
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass
