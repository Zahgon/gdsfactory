from __future__ import annotations

__all__ = ["via_corner"]

from typing import Any

from numpy import floor

import gdsfactory as gf
from gdsfactory.cross_section import metal2, metal3
from gdsfactory.port import select_ports
from gdsfactory.typings import ComponentSpec, MultiCrossSectionAngleSpec


@gf.cell_with_module_name(tags=["vias"])
def via_corner(
    cross_section: MultiCrossSectionAngleSpec = (
        (metal2, (0, 180)),
        (metal3, (90, 270)),
    ),
    vias: tuple[ComponentSpec] = ("via1",),
    layers_labels: tuple[str, ...] = ("m2", "m3"),
    **kwargs: Any,
) -> gf.Component:
    pass
