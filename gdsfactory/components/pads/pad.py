from __future__ import annotations

__all__ = [
    "pad",
    "pad_array",
    "pad_array0",
    "pad_array90",
    "pad_array180",
    "pad_array270",
    "pad_rectangular",
    "pad_small",
]

from functools import partial
from typing import Any

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.config import valid_port_orientations
from gdsfactory.typings import (
    AngleInDegrees,
    ComponentSpec,
    Float2,
    Ints,
    LayerSpec,
    Size,
)

from .._schematic import pad_schematic


@gf.cell_with_module_name(schematic_function=pad_schematic, tags=["pads"])
def pad(
    size: Size | str = (100.0, 100.0),
    layer: LayerSpec = "MTOP",
    bbox_layers: tuple[LayerSpec, ...] | None = None,
    bbox_offsets: tuple[float, ...] | None = None,
    port_inclusion: float = 0,
    port_orientation: AngleInDegrees | None = 0,
    port_orientations: Ints | None = (180, 90, 0, -90),
    port_type: str = "pad",
) -> Component:
    """Returns rectangular pad with ports.

    Args:
        size: x, y size.
        layer: pad layer.
        bbox_layers: list of layers.
        bbox_offsets: Optional offsets for each layer with respect to size.
            positive grows, negative shrinks the size.
        port_inclusion: from edge.
        port_orientation: in degrees for the center port.
        port_orientations: list of port_orientations to add. None does not add ports.
        port_type: port type for pad port.
    """
    c = Component()
    layer = gf.get_layer(layer)
    size_ = gf.get_constant(size)
    rect = gf.c.compass(
        size=size_,
        layer=layer,
        port_inclusion=port_inclusion,
        port_type="electrical",
        port_orientations=port_orientations,
    )
    c_ref = c.add_ref(rect)
    c.add_ports(c_ref.ports)
    c.info["size"] = size_
    c.info["xsize"] = size_[0]
    c.info["ysize"] = size_[1]

    if port_orientation is not None and port_orientation not in valid_port_orientations:
        raise ValueError(f"{port_orientation=} must be in {valid_port_orientations}")

    width = size_[1] if port_orientation in {0, 180} else size_[0]

    if port_orientation is not None:
        c.add_port(
            name="pad",
            port_type=port_type,
            layer=layer,
            center=(0, 0),
            orientation=port_orientation,
            width=width,
        )

    if bbox_layers and bbox_offsets:
        sizes: list[Size] = []
        for cladding_offset in bbox_offsets:
            size_new = (size_[0] + 2 * cladding_offset, size_[1] + 2 * cladding_offset)
            sizes.append(size_new)

        for layer, size_new in zip(bbox_layers, sizes, strict=False):
            c.add_ref(
                gf.c.compass(
                    size=size_new,
                    layer=layer,
                )
            )
    c.flatten()
    elec = [p for p in c.ports if p.port_type in {"electrical", "pad"}]
    if elec:
        c.create_pin(ports=elec, name="pad")
    return c


pad_rectangular = partial(pad, size="pad_size")
pad_small = partial(pad, size=(80, 80))


@gf.cell_with_module_name(schematic_function=pad_schematic, tags=["pads"])
def pad_array(
    pad: ComponentSpec = "pad",
    columns: int = 6,
    rows: int = 1,
    column_pitch: float = 150.0,
    row_pitch: float = 150.0,
    port_orientation: AngleInDegrees = 0,
    size: Float2 | None = None,
    layer: LayerSpec | None = "MTOP",
    centered_ports: bool = False,
    auto_rename_ports: bool = False,
) -> Component:
    pass


pad_array90 = partial(pad_array, port_orientation=90)
pad_array270 = partial(pad_array, port_orientation=270)

pad_array0 = partial(pad_array, port_orientation=0, columns=1, rows=3)
pad_array180 = partial(pad_array, port_orientation=180, columns=1, rows=3)
