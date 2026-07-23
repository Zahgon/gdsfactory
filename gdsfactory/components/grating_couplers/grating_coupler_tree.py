from __future__ import annotations

__all__ = ["grating_coupler_tree"]

from typing import Any

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec


@gf.cell_with_module_name(tags=["grating_couplers"])
def grating_coupler_tree(
    n: int = 4,
    straight_spacing: float = 4.0,
    grating_coupler: ComponentSpec = "grating_coupler_elliptical_te",
    with_loopback: bool = False,
    bend: ComponentSpec = "bend_euler",
    fanout_length: float = 0.0,
    cross_section: CrossSectionSpec = "strip",
    **kwargs: Any,
) -> Component:
    pass
