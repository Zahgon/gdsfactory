
from __future__ import annotations

__all__ = ["cdsem_straight_density", "gaps", "widths"]

import gdsfactory as gf
from gdsfactory.component import Component, ComponentReference
from gdsfactory.typings import ComponentSpec, CrossSectionSpec, Floats

widths = 10 * (0.3,)
gaps = 10 * (0.3,)


@gf.cell_with_module_name(tags=["pcms"])
def cdsem_straight_density(
    widths: Floats = widths,
    gaps: Floats = gaps,
    length: float = 420.0,
    label: str = "",
    cross_section: CrossSectionSpec = "strip_no_ports",
    text: ComponentSpec | None = "text_rectangular",
    text_size: float = 1.0,
) -> Component:
    pass
