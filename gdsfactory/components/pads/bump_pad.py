from __future__ import annotations

from typing import Any

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import (
    LayerSpec,
)

from ..shapes import octagon
from ..vias import via_stack

__all__ = ["bump_pad", "bump_pad_grid"]


@gf.cell_with_module_name(tags=["pads"])
def bump_pad(
    size: float = 36.244,
    layer: LayerSpec = "MTOP",
    port_width: float = 10.0,
    port_layer: LayerSpec = "M2",
    port_type: str = "pad",
    add_via: bool = True,
) -> Component:
    pass


@gf.cell_with_module_name(tags=["pads"])
def bump_pad_grid(
    columns: int = 6,
    rows: int = 6,
    column_pitch: float = 121.89,
    row_pitch: float = 132.66,
    offset: float = 66.33,
    port_width: float = 10,
    port_layer: LayerSpec = "M2",
    size: float = 36.244,
    layer: LayerSpec = "MTOP",
    auto_rename_ports: bool = False,
    skip_pads: list[tuple[int, int]] | None = None,
    add_via: bool = True,
) -> Component:
    pass
