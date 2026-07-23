from __future__ import annotations

__all__ = ["grating_coupler_loss"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.routing.route_bundle import route_bundle
from gdsfactory.typings import ComponentSpec, CrossSectionSpec


@gf.cell_with_module_name(tags=["grating_couplers"])
def grating_coupler_loss(
    pitch: float = 127.0,
    grating_coupler: ComponentSpec = "grating_coupler_elliptical_trenches",
    cross_section: CrossSectionSpec = "strip",
    port_name: str = "o1",
    rotation: float = -90,
    nfibers: int = 10,
    grating_coupler_spacing: float = 5.0,
) -> Component:
    pass
