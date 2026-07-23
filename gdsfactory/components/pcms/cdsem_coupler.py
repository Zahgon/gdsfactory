
from __future__ import annotations

__all__ = ["cdsem_coupler"]

from collections.abc import Sequence

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec


@gf.cell_with_module_name(tags=["pcms"])
def cdsem_coupler(
    length: float = 420.0,
    gaps: Sequence[float] = (0.15, 0.2, 0.25),
    cross_section: CrossSectionSpec = "strip_no_ports",
    text: ComponentSpec | None = "text_rectangular",
    spacing: float = 7.0,
    positions: Sequence[float | None] | None = None,
    width: float | None = None,
    text_size: float = 1.0,
) -> Component:
    pass
