from __future__ import annotations

__all__ = ["add_frame", "align_wafer"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, LayerSpec


@gf.cell_with_module_name(tags=["dies"])
def align_wafer(
    width: float = 10.0,
    spacing: float = 10.0,
    cross_length: float = 80.0,
    layer: LayerSpec = "WG",
    layer_cladding: tuple[int, int] | None = None,
    square_corner: str = "bottom_left",
) -> Component:
    pass


@gf.cell_with_module_name(tags=["dies"])
def add_frame(
    component: ComponentSpec = "rectangle",
    width: float = 10.0,
    spacing: float = 10.0,
    layer: LayerSpec = "WG",
) -> Component:
    pass
