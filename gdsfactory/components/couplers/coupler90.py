from __future__ import annotations

__all__ = ["coupler90", "coupler90circular"]

from functools import partial

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

from .._schematic import coupler_schematic


@gf.cell_with_module_name(schematic_function=coupler_schematic, tags=["couplers"])
def coupler90(
    gap: float = 0.2,
    radius: float | None = None,
    bend: ComponentSpec = "bend_euler",
    straight: ComponentSpec = "straight",
    cross_section: CrossSectionSpec = "strip",
    cross_section_bend: CrossSectionSpec | None = None,
    length_straight: float | None = None,
) -> Component:
    pass


coupler90circular = partial(coupler90, bend="bend_circular")
