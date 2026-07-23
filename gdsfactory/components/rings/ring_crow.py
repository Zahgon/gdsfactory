from __future__ import annotations

__all__ = ["ring_asymmetric", "ring_crow"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

from .._schematic import ring_double_schematic


@gf.cell_with_module_name(schematic_function=ring_double_schematic, tags=["rings"])
def ring_crow(
    gaps: tuple[float, ...] = (0.2, 0.2, 0.2, 0.2),
    radius: tuple[float, ...] = (10.0, 10.0, 10.0),
    bends: tuple[ComponentSpec, ...] | None = None,
    ring_cross_sections: tuple[CrossSectionSpec, ...] = ("strip", "strip", "strip"),
    length_x: float = 0,
    lengths_y: tuple[float, ...] = (0, 0, 0),
    input_straight_cross_section: CrossSectionSpec | None = None,
    output_straight_cross_section: CrossSectionSpec | None = None,
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass


@gf.cell_with_module_name(tags=["rings"])
def ring_asymmetric(
    radius: float = 10.0,
    length_x: float = 2.0,
    length_y: float = 4.0,
    straight: ComponentSpec = "straight",
    bend: ComponentSpec = "bend_circular",
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass
