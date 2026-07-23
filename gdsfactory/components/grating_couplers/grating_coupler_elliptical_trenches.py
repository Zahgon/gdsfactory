from __future__ import annotations

__all__ = [
    "grating_coupler_elliptical_trenches",
    "grating_coupler_te",
    "grating_coupler_tm",
]

from functools import partial

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.functions import DEG2RAD
from gdsfactory.typings import ComponentSpec, CrossSectionSpec, LayerSpec

from .._schematic import grating_coupler_schematic
from ..grating_couplers.functions import grating_tooth_points


@gf.cell_with_module_name(
    schematic_function=grating_coupler_schematic, tags=["grating_couplers"]
)
def grating_coupler_elliptical_trenches(
    polarization: str = "te",
    taper_length: float = 16.6,
    taper_angle: float = 30.0,
    trenches_extra_angle: float = 9.0,
    wavelength: float = 1.53,
    fiber_angle: float = 15.0,
    grating_line_width: float = 0.343,
    neff: float = 2.638,  # tooth effective index
    ncladding: float = 1.443,  # cladding index
    layer_trench: LayerSpec = "SHALLOW_ETCH",
    p_start: int = 26,
    n_periods: int = 30,
    end_straight_length: float = 0.2,
    taper: ComponentSpec = "taper",
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass


grating_coupler_te = partial(
    grating_coupler_elliptical_trenches, polarization="te", taper_angle=35
)

grating_coupler_tm = partial(
    grating_coupler_elliptical_trenches,
    polarization="tm",
    neff=1.8,
    grating_line_width=0.6,
)


if __name__ == "__main__":
    c = grating_coupler_elliptical_trenches()
    s = c.to_3d()
    s.show()
