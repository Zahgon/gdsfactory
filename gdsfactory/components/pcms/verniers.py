from __future__ import annotations

__all__ = ["verniers"]

from typing import Any

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec, Floats, LayerSpec


@gf.cell_with_module_name(tags=["pcms"])
def verniers(
    widths: Floats = (0.1, 0.2, 0.3, 0.4, 0.5),
    gap: float = 0.1,
    xsize: float = 100.0,
    layer_label: LayerSpec = "TEXT",
    straight: ComponentSpec = "straight",
    cross_section: CrossSectionSpec = "strip_no_ports",
    **kwargs: Any,
) -> Component:
    pass
