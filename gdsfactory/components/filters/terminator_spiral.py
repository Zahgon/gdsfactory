from __future__ import annotations

__all__ = ["terminator_spiral"]

import gdsfactory as gf
from gdsfactory.path import extrude_transition, spiral_archimedean, transition
from gdsfactory.typings import CrossSectionSpec

from .._schematic import terminator_schematic


@gf.cell_with_module_name(schematic_function=terminator_schematic, tags=["filters"])
def terminator_spiral(
    separation: float = 3.0,
    width_tip: float = 0.2,
    number_of_loops: float = 1,
    npoints: int = 1000,
    min_bend_radius: float | None = None,
    cross_section: CrossSectionSpec = "strip",
) -> gf.Component:
    pass
