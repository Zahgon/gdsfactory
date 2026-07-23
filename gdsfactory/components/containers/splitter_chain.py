from __future__ import annotations

__all__ = ["splitter_chain"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec


@gf.cell_with_module_name(tags=["containers"])
def splitter_chain(
    splitter: ComponentSpec = "mmi1x2",
    columns: int = 3,
    bend: ComponentSpec = "bend_s",
) -> Component:
    pass
