from __future__ import annotations

__all__ = ["spiral_double"]

import gdsfactory as gf
from gdsfactory.path import spiral_archimedean
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

from .._schematic import spiral_schematic


@gf.cell_with_module_name(schematic_function=spiral_schematic, tags=["spirals"])
def spiral_double(
    min_bend_radius: float = 10.0,
    separation: float = 2.0,
    number_of_loops: float = 3,
    npoints: int = 1000,
    cross_section: CrossSectionSpec = "strip",
    bend: ComponentSpec = "bend_circular",
) -> gf.Component:
    pass
