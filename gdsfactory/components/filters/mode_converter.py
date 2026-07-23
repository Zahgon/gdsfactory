from __future__ import annotations

__all__ = ["mode_converter"]

from functools import partial

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

from .._schematic import ckt_schematic
from ..bends.bend_s import bend_s


@gf.cell_with_module_name(schematic_function=ckt_schematic, tags=["filters"])
def mode_converter(
    gap: float = 0.3,
    length: float = 10,
    coupler_straight_asymmetric: ComponentSpec = "coupler_straight_asymmetric",
    bend: ComponentSpec = partial(bend_s, size=(25, 3)),
    taper: ComponentSpec = "taper",
    mm_width: float = 1.2,
    mc_mm_width: float = 1,
    sm_width: float = 0.5,
    taper_length: float = 25,
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass
