from __future__ import annotations

__all__ = ["wafer"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec

_cols_200mm_wafer = (2, 6, 6, 8, 8, 6, 6, 2)


@gf.cell_with_module_name(tags=["dies"])
def wafer(
    reticle: ComponentSpec = "die",
    cols: tuple[int, ...] = _cols_200mm_wafer,
    xspacing: float | None = None,
    yspacing: float | None = None,
    die_name_col_row: bool = False,
) -> Component:
    pass
