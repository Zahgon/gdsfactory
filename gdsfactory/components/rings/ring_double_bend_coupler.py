from __future__ import annotations

__all__ = ["ring_double_bend_coupler"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentAllAngleFactory, CrossSectionSpec

from .._schematic import ring_double_schematic
from ..bends.bend_circular import bend_circular_all_angle


@gf.cell_with_module_name(schematic_function=ring_double_schematic, tags=["rings"])
def ring_double_bend_coupler(
    radius: float = 5.0,
    gap: float = 0.2,
    coupling_angle_coverage: float = 70.0,
    bend: ComponentAllAngleFactory = bend_circular_all_angle,
    length_x: float = 0.6,
    length_y: float = 0.6,
    cross_section_inner: CrossSectionSpec = "strip",
    cross_section_outer: CrossSectionSpec = "strip",
) -> Component:
    pass
