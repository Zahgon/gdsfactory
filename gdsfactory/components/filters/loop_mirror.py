
from __future__ import annotations

__all__ = ["loop_mirror"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec


@gf.cell_with_module_name(tags=["filters"])
def loop_mirror(
    component: ComponentSpec = "mmi1x2",
    bend90: ComponentSpec = "bend_euler",
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass
