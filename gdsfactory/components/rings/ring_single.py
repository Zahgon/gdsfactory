from __future__ import annotations

__all__ = ["ring_single"]

import gdsfactory as gf
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

from .._schematic import ring_single_schematic


@gf.cell_with_module_name(schematic_function=ring_single_schematic, tags=["rings"])
def ring_single(
    gap: float = 0.2,
    radius: float | None = None,
    length_x: float = 4.0,
    length_y: float = 0.6,
    bend: ComponentSpec = "bend_euler",
    straight: ComponentSpec = "straight",
    coupler_ring: ComponentSpec = "coupler_ring",
    cross_section: CrossSectionSpec = "strip",
    length_extension: float | None = None,
) -> gf.Component:
    pass
