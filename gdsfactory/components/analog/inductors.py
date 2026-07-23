
import math

__all__ = ["inductor"]

import gdsfactory as gf
from gdsfactory import Component
from gdsfactory.typings import LayerSpec, LayerSpecs

from .._schematic import inductor_schematic


def inductor_min_diameter(width: float, space: float, turns: int, grid: float) -> float:
    pass


@gf.cell_with_module_name(schematic_function=inductor_schematic, tags=["analog"])
def inductor(
    width: float = 2.0,
    space: float = 2.1,
    diameter: float = 25.35,
    resistance: float = 0.5777,
    inductance: float = 33.303e-12,
    turns: int = 1,
    layer_metal: LayerSpec = "M3",
    layer_inductor: LayerSpec = "M1",
    layer_metal_pin: LayerSpec = "WG_PIN",
    layers_no_fill: LayerSpecs = ("DEVREC", "NO_TILE_SI"),
) -> Component:
    pass


if __name__ == "__main__":
    c = inductor()
    c.show()
