from __future__ import annotations

__all__ = ["cavity"]

from typing import Any

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec


@gf.cell_with_module_name(tags=["pcms"])
def cavity(
    component: ComponentSpec = "dbr",
    coupler: ComponentSpec = "coupler",
    length: float = 0.1,
    gap: float = 0.2,
    **kwargs: Any,
) -> Component:
    pass
