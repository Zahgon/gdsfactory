from __future__ import annotations

__all__ = ["coupler_ring"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

from .._schematic import coupler_ring_schematic
from ..couplers.coupler import coupler_straight
from ..couplers.coupler90 import coupler90


@gf.cell_with_module_name(schematic_function=coupler_ring_schematic, tags=["couplers"])
def coupler_ring(
    gap: float = 0.2,
    radius: float | None = None,
    length_x: float = 4.0,
    bend: ComponentSpec = "bend_euler",
    straight: ComponentSpec = "straight",
    cross_section: CrossSectionSpec = "strip",
    cross_section_bend: CrossSectionSpec | None = None,
    length_extension: float | None = None,
) -> Component:
    pass
