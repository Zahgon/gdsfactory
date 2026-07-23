
from __future__ import annotations

__all__ = ["cdsem_bend180"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

LINE_LENGTH = 420.0


@gf.cell_with_module_name(tags=["pcms"])
def cdsem_bend180(
    width: float = 0.5,
    radius: float = 10.0,
    wg_length: float | None = LINE_LENGTH,
    straight: ComponentSpec = "straight",
    bend90: ComponentSpec = "bend_circular",
    cross_section: CrossSectionSpec = "strip",
    text: ComponentSpec = "text_rectangular",
    text_size: float = 1.0,
) -> Component:
    pass
