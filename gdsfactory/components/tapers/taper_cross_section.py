from __future__ import annotations

__all__ = [
    "taper_cross_section",
    "taper_cross_section_linear",
    "taper_cross_section_parabolic",
    "taper_cross_section_sine",
]

from functools import partial

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import CrossSectionSpec, LayerSpec, LayerSpecs

from .._schematic import transition_schematic


@gf.cell_with_module_name(schematic_function=transition_schematic, tags=["tapers"])
def taper_cross_section(
    cross_section1: CrossSectionSpec = "strip_rib_tip",
    cross_section2: CrossSectionSpec = "rib2",
    length: float = 10,
    npoints: int = 100,
    linear: bool = False,
    width_type: str = "sine",
    exclude_layers: LayerSpecs | None = None,
) -> Component:
    pass


taper_cross_section_linear = partial(taper_cross_section, linear=True, npoints=2)
taper_cross_section_sine = partial(taper_cross_section, linear=False, npoints=101)
taper_cross_section_parabolic = partial(
    taper_cross_section, linear=False, width_type="parabolic", npoints=101
)
