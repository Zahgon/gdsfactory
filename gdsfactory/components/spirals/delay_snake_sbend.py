from __future__ import annotations

__all__ = ["delay_snake_sbend"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

from .._schematic import spiral_schematic
from ..waveguides.straight import straight

diagram = r"""

                         length1
         <----------------------------
               length2    spacing    |
                _______              |
               |        \            |
               |          \          | bend1 radius
               |            \sbend   |
          bend2|              \      |
               |                \    |
               |                  \__|
               |
               ---------------------->----------->
                   length3              length4
"""


@gf.cell_with_module_name(schematic_function=spiral_schematic, tags=["spirals"])
def delay_snake_sbend(
    length: float = 100.0,
    length1: float = 0.0,
    length4: float = 0.0,
    radius: float = 5.0,
    waveguide_spacing: float = 5.0,
    bend: ComponentSpec = "bend_euler",
    sbend: ComponentSpec = "bend_s",
    sbend_xsize: float = 100.0,
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass


if __name__ == "__main__":
    import math

    c = delay_snake_sbend()
    print(c.info["length"])

    area = c.area(layer=(1, 0))
    length = area / 0.5
    print(length)

    assert math.isclose(c.info["length"], length, rel_tol=1e-3), (
        f"{c.info['length']} != {length}"
    )
    c.show()
