from __future__ import annotations

__all__ = ["litho_ruler"]

import gdsfactory as gf
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["pcms"])
def litho_ruler(
    height: float = 2,
    width: float = 0.5,
    spacing: float = 2.0,
    scale: tuple[float, ...] = (3, 1, 1, 1, 1, 2, 1, 1, 1, 1),
    num_marks: int = 21,
    layer: LayerSpec = "WG",
) -> gf.Component:
    pass
