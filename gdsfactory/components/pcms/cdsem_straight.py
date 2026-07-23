
from __future__ import annotations

__all__ = ["cdsem_straight"]

from collections.abc import Sequence

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

LINE_LENGTH = 420.0


@gf.cell_with_module_name(tags=["pcms"])
def cdsem_straight(
    widths: Sequence[float] = (0.4, 0.45, 0.5, 0.6, 0.8, 1.0),
    length: float = LINE_LENGTH,
    cross_section: CrossSectionSpec = "strip_no_ports",
    text: ComponentSpec | None = "text_rectangular",
    spacing: float = 7.0,
    positions: Sequence[float | None] | None = None,
    text_size: float = 1,
) -> Component:
    pass
