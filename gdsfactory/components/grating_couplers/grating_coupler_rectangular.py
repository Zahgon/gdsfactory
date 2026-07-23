from __future__ import annotations

__all__ = ["grating_coupler_rectangular"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec, LayerSpec

from .._schematic import grating_coupler_schematic


@gf.cell_with_module_name(
    schematic_function=grating_coupler_schematic, tags=["grating_couplers"]
)
def grating_coupler_rectangular(
    n_periods: int = 20,
    period: float = 0.75,
    fill_factor: float = 0.5,
    width_grating: float = 11.0,
    length_taper: float = 150.0,
    polarization: str = "te",
    wavelength: float = 1.55,
    taper: ComponentSpec = "taper",
    layer_slab: LayerSpec | None = "SLAB150",
    layer_grating: LayerSpec | None = None,
    fiber_angle: float = 15,
    slab_xmin: float = -1.0,
    slab_offset: float = 1.0,
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass
