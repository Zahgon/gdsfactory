from __future__ import annotations

__all__ = ["coupler90bend"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

from .._schematic import coupler_schematic


@gf.cell_with_module_name(schematic_function=coupler_schematic, tags=["couplers"])
def coupler90bend(
    radius: float = 10.0,
    gap: float = 0.2,
    bend: ComponentSpec = "bend_euler",
    cross_section_inner: CrossSectionSpec = "strip",
    cross_section_outer: CrossSectionSpec = "strip",
) -> Component:
    pass
