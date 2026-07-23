from __future__ import annotations

__all__ = ["ruler"]

import gdsfactory as gf
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["pcms"])
def ruler(
    height_long: float = 55,
    height_short: float = 5,
    height_numbered: float = 10,
    width: float = 2,
    spacing: float = 5.0,
    marks: tuple[float | None, ...] = (
        -100,
        None,
        -90,
        None,
        -80,
        None,
        -70,
        None,
        -60,
        None,
        -50,
        None,
        -40,
        None,
        -30,
        None,
        -20,
        None,
        -10,
        None,
        0,
    ),
    layer: LayerSpec = "WG",
    bbox_layers: tuple[LayerSpec, ...] | None = None,
    bbox_offset: float = 3.0,
    long_marks: tuple[float, ...] = (-50, 0),
    text_size: float = 3.5,
) -> gf.Component:
    pass
