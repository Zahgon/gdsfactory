from __future__ import annotations

__all__ = ["grating_coupler_dual_pol"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec, LayerSpec

from .._schematic import grating_coupler_schematic


def _unit_cell() -> gf.Component:
    pass


@gf.cell_with_module_name(
    schematic_function=grating_coupler_schematic, tags=["grating_couplers"]
)
def grating_coupler_dual_pol(
    unit_cell: ComponentSpec = _unit_cell,
    period_x: float = 0.58,
    period_y: float = 0.58,
    x_span: float = 11,
    y_span: float = 11,
    length_taper: float = 150.0,
    width_taper: float = 10.0,
    polarization: str = "te",
    wavelength: float = 1.55,
    taper: ComponentSpec = "taper",
    base_layer: LayerSpec = "WG",
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass
