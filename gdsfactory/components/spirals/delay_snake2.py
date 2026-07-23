from __future__ import annotations

__all__ = ["delay_snake2"]

import warnings

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

from .._schematic import spiral_schematic
from ..containers.component_sequence import component_sequence

diagram = """
       | length0 | length1 |

                 >---------|
                           | bend180.length
       |-------------------|
       |
       |------------------->------- |
                            length2
       |   delta_length    |        |
"""


@gf.cell_with_module_name(schematic_function=spiral_schematic, tags=["spirals"])
def delay_snake2(
    length: float = 1600.0,
    length0: float = 0.0,
    length2: float = 0.0,
    n: int = 2,
    bend180: ComponentSpec = "bend_euler180",
    cross_section: CrossSectionSpec = "strip",
    width: float | None = None,
) -> Component:
    pass
