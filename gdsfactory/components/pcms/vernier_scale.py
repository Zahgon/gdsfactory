from __future__ import annotations

__all__ = ["vernier_scale"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["pcms"])
def vernier_scale(
    n_divisions: int = 10,
    pitch_main: float = 10.0,
    pitch_vernier: float = 9.8,
    mark_width: float = 1.0,
    mark_height_main: float = 20.0,
    mark_height_vernier: float = 15.0,
    layer_main: LayerSpec = "WG",
    layer_vernier: LayerSpec = (2, 0),
) -> Component:
    pass


if __name__ == "__main__":
    c = vernier_scale()
    c.show()
