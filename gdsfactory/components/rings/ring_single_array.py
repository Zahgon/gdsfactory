from __future__ import annotations

__all__ = ["ring_single_array"]

from typing import Any

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

_list_of_dicts: tuple[dict[str, Any], ...] = (
    dict(length_x=10.0, radius=5.0),
    dict(length_x=20.0, radius=10.0),
)


@gf.cell_with_module_name(tags=["rings"])
def ring_single_array(
    ring: ComponentSpec = "ring_single",
    spacing: float = 15.0,
    list_of_dicts: tuple[dict[str, Any], ...] | None = None,
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass
