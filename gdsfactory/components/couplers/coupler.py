from __future__ import annotations

__all__ = ["coupler", "coupler_straight", "coupler_symmetric"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec, Delta

from .._schematic import coupler_schematic


@gf.cell_with_module_name(tags=["couplers"])
def coupler_symmetric(
    bend: ComponentSpec = "bend_s",
    gap: float = 0.234,
    dy: Delta = 4.0,
    dx: Delta = 10.0,
    cross_section: CrossSectionSpec = "strip",
    allow_min_radius_violation: bool = False,
) -> Component:
    pass


@gf.cell_with_module_name(schematic_function=coupler_schematic, tags=["couplers"])
def coupler_straight(
    length: float = 10.0,
    gap: float = 0.27,
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass


@gf.cell_with_module_name(schematic_function=coupler_schematic, tags=["couplers"])
def coupler(
    gap: float = 0.236,
    length: float = 20.0,
    dy: Delta = 4.0,
    dx: Delta = 10.0,
    cross_section: CrossSectionSpec = "strip",
    allow_min_radius_violation: bool = False,
    bend: ComponentSpec = "bend_s",
) -> Component:
    pass
