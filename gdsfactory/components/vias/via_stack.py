from __future__ import annotations

__all__ = [
    "via_stack",
    "via_stack_corner45",
    "via_stack_corner45_extended",
    "via_stack_heater_m2",
    "via_stack_heater_m3",
    "via_stack_heater_mtop",
    "via_stack_heater_mtop_mini",
    "via_stack_m1_m3",
    "via_stack_m1_mtop",
    "via_stack_m2_m3",
    "via_stack_npp_m1",
    "via_stack_slab_m1",
    "via_stack_slab_m1_horizontal",
    "via_stack_slab_m2",
    "via_stack_slab_m3",
    "via_stack_slab_npp_m3",
]

import warnings
from collections.abc import Iterable, Sequence
from functools import partial

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component, ComponentReference
from gdsfactory.typings import ComponentSpec, Floats, Ints, LayerSpec, LayerSpecs, Size


@gf.cell_with_module_name(tags=["vias"])
def via_stack(
    size: Size = (11.0, 11.0),
    layers: LayerSpecs = ("M1", "M2", "MTOP"),
    layer_offsets: Floats | tuple[float | tuple[float, float], ...] | None = None,
    vias: Sequence[ComponentSpec | None] = ("via1", "via2", None),
    layer_to_port_orientations: dict[LayerSpec, list[int]] | None = None,
    correct_size: bool = False,
    slot_horizontal: bool = False,
    slot_vertical: bool = False,
    port_orientations: Ints | None = (180, 90, 0, -90),
) -> Component:
    """Rectangular via array stack.

    You can use it to connect different metal layers or metals to silicon.
    You can use the naming convention via_stack_layerSource_layerDestination
    contains 4 ports (e1, e2, e3, e4)

    also know as Via array
    http://www.vlsi-expert.com/2017/12/vias.html

    Args:
        size: of the layers.
        layers: layers on which to draw rectangles.
        layer_offsets: Optional offsets for each layer with respect to size.
            positive grows, negative shrinks the size. If a tuple, it is the offset in x and y.
        vias: vias to use to fill the rectangles.
        layer_to_port_orientations: dictionary of layer to port_orientations.
        correct_size: if True, if the specified dimensions are too small it increases
            them to the minimum possible to fit a via.
        slot_horizontal: if True, then vias are horizontal.
        slot_vertical: if True, then vias are vertical.
        port_orientations: list of port_orientations to add. None does not add ports.
    """
    width_m, height_m = size

    layers = layers or []
    layer_indices = [gf.get_layer(layer) for layer in layers]
    layer_offsets = layer_offsets or [0] * len(layers)
    layer_to_port_orientations_dict = layer_to_port_orientations or {
        layers[-1]: list(port_orientations or [])
    }
    resolved_port_orientations = {
        gf.get_layer(k): v for k, v in layer_to_port_orientations_dict.items()
    }

    elements = {len(layers), len(layer_offsets), len(vias)}
    if len(elements) > 1:
        warnings.warn(
            f"Got {len(layers)} layers, {len(layer_offsets)} layer_offsets, {len(vias)} vias",
            stacklevel=3,
        )

    vias_list = vias or []
    for via, offset in zip(vias_list, layer_offsets, strict=False):
        if via is not None:
            width, height = size
            if isinstance(offset, Iterable):
                offset_x = offset[0]
                offset_y = offset[1]
            else:
                offset_x = offset_y = offset
            width += 2 * offset_x
            height += 2 * offset_y

            _via = gf.get_component(via)
            if "xsize" not in _via.info:
                raise ValueError(
                    f"Component {_via.name!r} does not have a 'xsize' key in info"
                )
            if "ysize" not in _via.info:
                raise ValueError(
                    f"Component {_via.name!r} does not have a 'ysize' key in info"
                )
            if "column_pitch" not in _via.info:
                raise ValueError(
                    f"Component {_via.name!r} does not have a 'column_pitch' key in info"
                )
            if "row_pitch" not in _via.info:
                raise ValueError(
                    f"Component {_via.name!r} does not have a 'row_pitch' key in info"
                )

            w, h = _via.xsize, _via.ysize
            enclosure = _via.info["enclosure"]

            min_width = w + 2 * enclosure
            min_height = h + 2 * enclosure

            if correct_size and (min_width > width or min_height > height):
                corrected_width = max(min_width, width)
                corrected_height = max(min_height, height)
                warnings.warn(
                    f"Changing size from ({width}, {height}) to ({corrected_width}, {corrected_height}) to fit a via!",
                    stacklevel=3,
                )
                width_m = max(width_m, corrected_width - 2 * offset_x)
                height_m = max(height_m, corrected_height - 2 * offset_y)
            elif min_width > width or min_height > height:
                raise ValueError(
                    f"Enclosure cannot be satisfied: size ({width}, {height}) is too small "
                    f"to fit a {(w, h)} um via with enclosure={enclosure}. "
                    f"Minimum required size is ({min_width}, {min_height})."
                )

    c = Component()
    c.info["xsize"], c.info["ysize"] = (width_m, height_m)

    multiple_port_layers = len(resolved_port_orientations) > 1

    for layer_index, offset in zip(layer_indices, layer_offsets, strict=False):
        if isinstance(offset, Iterable):
            offset_x = offset[0]
            offset_y = offset[1]
        else:
            offset_x = offset_y = offset

        size_m = (width_m + 2 * offset_x, height_m + 2 * offset_y)

        if layer_index in resolved_port_orientations:
            ref = c << gf.c.compass(
                size=size_m,
                layer=layer_index,
                port_type="electrical",
                port_orientations=resolved_port_orientations[layer_index],
                auto_rename_ports=False,
            )
            if multiple_port_layers:
                layer_name = (
                    layer_index.name
                    if hasattr(layer_index, "name")
                    else f"{layer_index[0]}_{layer_index[1]}"
                )
                for port in ref.ports:
                    c.add_port(name=f"{port.name}_{layer_name}", port=port)
            else:
                c.add_ports(ref.ports)
        else:
            ref = c << gf.c.compass(
                size=size_m,
                layer=layer_index,
                port_type=None,
                port_orientations=port_orientations,
            )

    for via, offset in zip(vias_list, layer_offsets, strict=False):
        if via is not None:
            if isinstance(offset, Iterable):
                offset_x = offset[0]
                offset_y = offset[1]
            else:
                offset_x = offset_y = offset
            width = width_m + 2 * offset_x
            height = height_m + 2 * offset_y

            _via = gf.get_component(via)
            w, h = _via.xsize, _via.ysize
            enclosure = _via.info["enclosure"]
            pitch_y = _via.info["row_pitch"]
            pitch_x = _via.info["column_pitch"]

            if slot_horizontal:
                slot_via_width = width - 2 * enclosure
                if slot_via_width <= 0:
                    raise ValueError(
                        f"Enclosure cannot be satisfied in slot_horizontal mode: "
                        f"width={width}, enclosure={enclosure}. "
                        f"Need width > 2*enclosure, got {width} <= {2 * enclosure}"
                    )
                via = gf.get_component(via, size=(slot_via_width, h))
                nb_vias_x = 1
                nb_vias_y = max(1, (height - 2 * enclosure - h) / pitch_y + 1)
                w = slot_via_width

            elif slot_vertical:
                slot_via_height = height - 2 * enclosure
                if slot_via_height <= 0:
                    raise ValueError(
                        f"Enclosure cannot be satisfied in slot_vertical mode: "
                        f"height={height}, enclosure={enclosure}. "
                        f"Need height > 2*enclosure, got {height} <= {2 * enclosure}"
                    )
                via = gf.get_component(via, size=(w, slot_via_height))
                nb_vias_x = max(0, (width - w - 2 * enclosure) / pitch_x + 1)
                nb_vias_y = 1
                h = slot_via_height
            else:
                via = _via
                nb_vias_x = max(0, (width - w - 2 * enclosure) / pitch_x + 1)
                nb_vias_y = max(0, (height - h - 2 * enclosure) / pitch_y + 1)

            nb_vias_x = int(np.floor(nb_vias_x)) or 1
            nb_vias_y = int(np.floor(nb_vias_y)) or 1
            ref = c.add_ref(
                via,
                columns=nb_vias_x,
                rows=nb_vias_y,
                column_pitch=pitch_x,
                row_pitch=pitch_y,
            )

            a = width / 2
            b = height / 2
            cw = (width - (nb_vias_x - 1) * pitch_x - w) / 2
            ch = (height - (nb_vias_y - 1) * pitch_y - h) / 2

            tolerance = 1e-9
            if cw < enclosure - tolerance or ch < enclosure - tolerance:
                raise ValueError(
                    f"Enclosure violation: calculated margins (cw={cw:.3f}, ch={ch:.3f}) "
                    f"are less than required enclosure={enclosure}. "
                    f"Size ({width:.3f}, {height:.3f}) is too small for {nb_vias_x}x{nb_vias_y} "
                    f"vias of size ({w}, {h}) with pitch ({pitch_x}, {pitch_y})."
                )

            x0 = -a + cw + w / 2
            y0 = -b + ch + h / 2
            ref.move((x0, y0))
    elec = [p for p in c.ports if p.port_type == "electrical"]
    if elec:
        c.create_pin(ports=elec, name="pad")
    return c


@gf.cell_with_module_name(tags=["vias"])
def via_stack_corner45(
    width: float = 10,
    layers: Sequence[LayerSpec | None] = ("M1", "M2", "MTOP"),
    layer_offsets: Floats | None = None,
    vias: Sequence[ComponentSpec | None] = ("via1", "via2", None),
    layer_port: LayerSpec | None = None,
    correct_size: bool = False,
) -> Component:
    pass


@gf.cell_with_module_name(tags=["vias"])
def via_stack_corner45_extended(
    corner: ComponentSpec = "via_stack_corner45",
    via_stack: ComponentSpec = "via_stack",
    width: float = 3,
    length: float = 10,
) -> Component:
    pass


via_stack_m1_mtop = via_stack_m1_m3 = partial(
    via_stack,
    layers=("M1", "M2", "MTOP"),
    vias=("via1", "via2", None),
)
via_stack_m2_m3 = partial(
    via_stack,
    layers=("M2", "MTOP"),
    vias=("via2", None),
)
via_stack_slab_m1 = partial(
    via_stack,
    layers=("SLAB90", "M1"),
    vias=("viac", "via1"),
)
via_stack_slab_m2 = partial(
    via_stack,
    layers=("SLAB90", "M1", "M2"),
    vias=("viac", "via1", None),
)

via_stack_slab_m3 = partial(
    via_stack,
    layers=("SLAB90", "M1", "M2", "MTOP"),
    vias=("viac", "via1", "via2", None),
)
via_stack_npp_m1 = partial(
    via_stack,
    layers=("WG", "NPP", "M1"),
    vias=(None, None, "viac"),
)
via_stack_slab_npp_m3 = partial(
    via_stack,
    layers=("SLAB90", "NPP", "M1"),
    vias=(None, None, "viac"),
)
via_stack_heater_mtop = via_stack_heater_m3 = partial(
    via_stack, layers=("HEATER", "M2", "MTOP"), vias=(None, "via1", "via2")
)
via_stack_heater_mtop_mini = partial(via_stack_heater_mtop, size=(4, 4))

via_stack_heater_m2 = partial(via_stack, layers=("HEATER", "M2"), vias=(None, "via1"))

via_stack_slab_m1_horizontal = partial(via_stack_slab_m1, slot_horizontal=True)


if __name__ == "__main__":
    c = via_stack_heater_mtop_mini(size=(1, 1), correct_size=True)
    c.show()
