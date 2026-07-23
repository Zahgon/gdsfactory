__all__ = ["die_with_pads"]

import warnings

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec, LayerSpec, Size


@gf.cell_with_module_name(tags=["dies"])
def die_with_pads(
    size: Size = (11470.0, 4900.0),
    ngratings: int = 14,
    npads: int = 31,
    grating_pitch: float = 250.0,
    pad_pitch: float = 300.0,
    grating_coupler: ComponentSpec | None = "grating_coupler_te",
    cross_section: CrossSectionSpec = "strip",
    pad: ComponentSpec = "pad",
    layer_floorplan: LayerSpec = "FLOORPLAN",
    edge_to_pad_distance: float = 150.0,
    edge_to_grating_distance: float = 150.0,
    with_loopback: bool = True,
    loopback_radius: float | None = None,
    pad_port_name_top: str = "e4",
    pad_port_name_bot: str = "e2",
) -> Component:
    pass
