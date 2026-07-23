from __future__ import annotations

__all__ = ["spiral_inductor"]

import gdsfactory as gf
from gdsfactory.component import Component

from .._schematic import spiral_schematic


@gf.cell_with_module_name(schematic_function=spiral_schematic, tags=["spirals"])
def spiral_inductor(
    width: float = 3.0,
    pitch: float = 3.0,
    turns: int = 16,
    outer_diameter: float = 800,
    tail: float = 50.0,
) -> Component:
    pass


if __name__ == "__main__":
    import math

    from gdsfactory.gpdk import PDK

    PDK.activate()

    c = spiral_inductor()
    print(c.info["length"])

    area = c.area(layer=(1, 0))
    length = area / 3.0
    print(length)

    c.show()
    assert math.isclose(c.info["length"], length, rel_tol=1e-3), (
        f"{c.info['length']} != {length}"
    )
