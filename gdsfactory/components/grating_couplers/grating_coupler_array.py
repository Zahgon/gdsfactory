from __future__ import annotations

__all__ = ["grating_coupler_array"]

import kfactory as kf

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.routing.auto_taper import add_auto_tapers
from gdsfactory.typings import ComponentSpec, CrossSectionSpec


@gf.cell_with_module_name(tags=["grating_couplers"])
def grating_coupler_array(
    grating_coupler: ComponentSpec = "grating_coupler_elliptical",
    pitch: float = 127.0,
    n: int = 6,
    port_name: str = "o1",
    rotation: int = -90,
    with_loopback: bool = False,
    cross_section: CrossSectionSpec = "strip",
    straight_to_grating_spacing: float = 10.0,
    centered: bool = True,
    radius: float | None = None,
    bend: ComponentSpec = "bend_euler",
    mirror_grating_coupler: bool = False,
) -> Component:
    pass


def _get_routing_radius(bend: Component, cross_section: CrossSectionSpec) -> float:
    pass
