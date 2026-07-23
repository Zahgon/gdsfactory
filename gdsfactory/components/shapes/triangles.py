from __future__ import annotations

__all__ = [
    "triangle",
    "triangle2",
    "triangle2_thin",
    "triangle4",
    "triangle4_thin",
    "triangle_thin",
]

from functools import partial
from typing import Any

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["shapes"])
def triangle(
    x: float = 10,
    xtop: float = 0,
    y: float = 20,
    ybot: float = 0,
    layer: LayerSpec = "WG",
) -> Component:
    pass


@gf.cell_with_module_name(tags=["shapes"])
def triangle2(spacing: float = 3, **kwargs: Any) -> Component:
    pass


@gf.cell_with_module_name(tags=["shapes"])
def triangle4(**kwargs: Any) -> Component:
    pass


triangle_thin = partial(triangle, xtop=0.2, x=2, y=5)
triangle2_thin = partial(triangle2, xtop=0.2, x=2, y=5)
triangle4_thin = partial(triangle4, xtop=0.2, x=2, y=5)
