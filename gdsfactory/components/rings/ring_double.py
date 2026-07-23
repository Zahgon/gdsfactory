from __future__ import annotations

__all__ = ["ring_double"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

from .._schematic import ring_double_schematic


@gf.cell_with_module_name(schematic_function=ring_double_schematic, tags=["rings"])
def ring_double(
    gap: float = 0.2,
    gap_top: float | None = None,
    gap_bot: float | None = None,
    radius: float | None = None,
    length_x: float = 0.01,
    length_y: float = 0.01,
    bend: ComponentSpec = "bend_euler",
    straight: ComponentSpec = "straight",
    coupler_ring: ComponentSpec = "coupler_ring",
    coupler_ring_top: ComponentSpec | None = None,
    cross_section: CrossSectionSpec = "strip",
    length_extension: float | None = None,
) -> Component:
    pass
