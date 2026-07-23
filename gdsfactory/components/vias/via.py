from __future__ import annotations

__all__ = ["via", "via1", "via2", "via_circular", "viac"]

from collections.abc import Sequence
from functools import partial
from typing import cast

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec, Size


@gf.cell_with_module_name(tags=["vias"])
def via(
    size: Size = (0.7, 0.7),
    enclosure: float = 1.0,
    layer: LayerSpec = "VIAC",
    bbox_layers: Sequence[LayerSpec] | None = None,
    bbox_offset: float = 0,
    bbox_offsets: Sequence[float] | None = None,
    pitch: float = 2,
    column_pitch: float | None = None,
    row_pitch: float | None = None,
) -> Component:
    pass


@gf.cell_with_module_name(tags=["vias"])
def via_circular(
    radius: float = 0.35,
    enclosure: float = 1.0,
    layer: LayerSpec = "VIAC",
    pitch: float | None = 2,
    column_pitch: float | None = None,
    row_pitch: float | None = None,
    angle_resolution: float = 2.5,
) -> Component:
    pass


viac = partial(via, layer="VIAC")
via1 = partial(via, layer="VIA1", enclosure=1)
via2 = partial(via, layer="VIA2")
