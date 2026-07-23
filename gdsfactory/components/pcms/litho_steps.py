from __future__ import annotations

__all__ = ["litho_steps"]

import gdsfactory as gf
from gdsfactory import components as pc
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["pcms"])
def litho_steps(
    line_widths: tuple[float, ...] = (1.0, 2.0, 4.0, 8.0, 16.0),
    line_spacing: float = 10.0,
    height: float = 100.0,
    layer: LayerSpec = "WG",
) -> Component:
    pass
