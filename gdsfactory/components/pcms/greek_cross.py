
__all__ = ["greek_cross", "greek_cross_with_pads"]

import gdsfactory as gf
from gdsfactory.cross_section import metal1
from gdsfactory.typings import ComponentSpec, CrossSectionSpec, Floats, LayerSpecs


@gf.cell_with_module_name(tags=["pcms"])
def greek_cross(
    length: float = 30,
    layers: LayerSpecs = ("WG", "N"),
    widths: Floats = (2.0, 3.0),
    offsets: Floats | None = None,
    via_stack: ComponentSpec = "via_stack_npp_m1",
    layer_index: int = 0,
) -> gf.Component:
    pass


@gf.cell_with_module_name(tags=["pcms"])
def greek_cross_with_pads(
    pad: ComponentSpec = "pad",
    pad_pitch: float = 150.0,
    greek_cross_component: ComponentSpec = "greek_cross",
    pad_via: ComponentSpec = "via_stack_m1_mtop",
    cross_section: CrossSectionSpec = metal1,
    pad_port_name: str = "e4",
) -> gf.Component:
    pass
