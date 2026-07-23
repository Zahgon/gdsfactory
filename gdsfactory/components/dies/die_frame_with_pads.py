__all__ = [
    "die_frame",
    "die_frame_phix",
    "die_frame_phix_dc",
    "die_frame_phix_rf",
    "die_frame_rf",
    "die_frame_with_pads",
]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec, Float2, LayerSpec, Size


@gf.cell(tags=["dies"])
def die_frame(
    size: Size = (11200.0, 5000.0),
    layer_floorplan: LayerSpec = "FLOORPLAN",
) -> gf.Component:
    pass


@gf.cell(tags=["dies"])
def die_frame_rf(
    size: Size = (10400.0, 5000.0),
    layer_floorplan: LayerSpec = "FLOORPLAN",
) -> gf.Component:
    pass


@gf.cell_with_module_name(tags=["dies"])
def die_frame_with_pads(
    die_frame: ComponentSpec = "die_frame",
    ngratings: int = 14,
    npads: int = 31,
    grating_pitch: float = 250.0,
    pad_pitch: float = 300.0,
    grating_coupler: ComponentSpec | None = "grating_coupler_te",
    cross_section: CrossSectionSpec = "strip",
    pad: ComponentSpec = "pad",
    edge_to_pad_distance: float = 150.0,
    edge_to_grating_distance: float = 150.0,
    with_loopback: bool = True,
    loopback_radius: float | None = None,
    pad_port_name_top: str = "e4",
    pad_port_name_bot: str = "e2",
) -> Component:
    pass


def die_frame_phix(
    die_frame: ComponentSpec = "die_frame",
    nfibers: int = 32,
    npads: int = 60,
    npads_rf: int = 6,
    fiber_pitch: float = 127.0,
    pad_pitch: float = 150.0,
    pad_pitch_gsg: float = 720.0,
    edge_coupler: ComponentSpec | None = "edge_coupler_silicon",
    grating_coupler: ComponentSpec | None = None,
    cross_section: CrossSectionSpec = "strip",
    pad: ComponentSpec = "pad",
    pad_gsg: ComponentSpec = "pad_gsg",
    edge_to_pad_distance: float = 200.0,
    edge_to_pad_distance_left: float | None = None,
    pad_port_name_top: str = "e4",
    pad_port_name_bot: str = "e2",
    pad_port_name_rf: str = "e2",
    layer_fiducial: LayerSpec = "M3",
    layer_ruler: LayerSpec = "WG",
    ruler_bbox_layers: tuple[LayerSpec, ...] | None = None,
    ruler_bbox_offset: float = 3.0,
    ruler_yoffset: float = 0,
    ruler_xoffset: float = 0,
    fiber_coupler_xoffset: float = 0,
    with_right_fiber_coupler: bool = True,
    with_left_fiber_coupler: bool = True,
    text_offset: Float2 = (20, 10),
    text: ComponentSpec | None = "text_rectangular",
    pad_side_distance: float = 1160.0,
    xoffset_rf_pads: float = 50,
    pad_rotation_dc_north: float = 0,
    pad_rotation_dc_south: float = 0,
    pad_rotation_rf: float = 0,
    with_loopback: bool = True,
) -> Component:
    pass


@gf.cell_with_module_name(tags=["dies"])
def die_frame_phix_dc(
    die_frame: ComponentSpec = "die_frame",
    nfibers: int = 32,
    npads: int = 59,
    npads_rf: int = 6,
    fiber_pitch: float = 127.0,
    pad_pitch: float = 150.0,
    pad_pitch_gsg: float = 720.0,
    edge_coupler: ComponentSpec | None = "edge_coupler_silicon",
    grating_coupler: ComponentSpec | None = None,
    cross_section: CrossSectionSpec = "strip",
    pad: ComponentSpec = "pad",
    pad_gsg: ComponentSpec = "pad_gsg",
    edge_to_pad_distance: float = 200.0,
    pad_port_name_top: str = "e4",
    pad_port_name_bot: str = "e2",
    layer_fiducial: LayerSpec = "M3",
    layer_ruler: LayerSpec = "WG",
    ruler_bbox_layers: tuple[LayerSpec, ...] | None = None,
    ruler_bbox_offset: float = 3.0,
    ruler_yoffset: float = 0,
    ruler_xoffset: float = 0,
    with_right_fiber_coupler: bool = True,
    with_left_fiber_coupler: bool = True,
    fiber_coupler_xoffset: float = 0,
    text_offset: Float2 = (20, 10),
    text: ComponentSpec | None = None,
    pad_rotation_dc_north: float = 0,
    pad_rotation_dc_south: float = 0,
    pad_side_distance: float = 1160.0,
) -> Component:
    pass


@gf.cell_with_module_name(tags=["dies"])
def die_frame_phix_rf(
    die_frame: ComponentSpec = "die_frame_rf",
    nfibers: int = 32,
    npads: int = 59,
    npads_rf: int = 6,
    fiber_pitch: float = 127.0,
    pad_pitch: float = 150.0,
    pad_pitch_gsg: float = 720.0,
    edge_coupler: ComponentSpec | None = "edge_coupler_silicon",
    grating_coupler: ComponentSpec | None = None,
    cross_section: CrossSectionSpec = "strip",
    pad: ComponentSpec = "pad",
    pad_gsg: ComponentSpec = "pad_gsg",
    edge_to_pad_distance: float = 200.0,
    pad_port_name_top: str = "e4",
    pad_port_name_bot: str = "e2",
    pad_port_name_rf: str = "e2",
    layer_fiducial: LayerSpec = "M3",
    layer_ruler: LayerSpec = "WG",
    ruler_bbox_layers: tuple[LayerSpec, ...] | None = None,
    ruler_bbox_offset: float = 3.0,
    ruler_yoffset: float = 0,
    ruler_xoffset: float = 0,
    with_right_fiber_coupler: bool = True,
    with_left_fiber_coupler: bool = False,
    fiber_coupler_xoffset: float = 0,
    text_offset: Float2 = (20, 10),
    text: ComponentSpec | None = None,
    pad_side_distance: float = 350.0,
    xoffset_rf_pads: float = 50,
    pad_rotation_rf: float = 0,
    pad_rotation_dc_north: float = 0,
    pad_rotation_dc_south: float = 0,
) -> Component:
    pass


if __name__ == "__main__":
    from functools import partial

    text_m3 = None
    edge_coupler = partial(gf.c.edge_coupler_silicon, length=200)
    grating_coupler = "grating_coupler_te"

    c = die_frame_phix_dc(edge_coupler=edge_coupler, text=text_m3)
    c.write_gds("/Users/j/Downloads/die_frame_phix_dc.gds")

    grating_coupler = "grating_coupler_te"
    c = die_frame_phix_dc(
        die_frame=die_frame(size=(11800, 5000)),
        edge_coupler=None,
        text=text_m3,
        grating_coupler=grating_coupler,
    )
    c.write_gds("/Users/j/Downloads/die_frame_phix_rf_grating_coupler.gds")

    c.show()
