
from __future__ import annotations

import warnings
from collections.abc import Sequence
from functools import partial

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.port import Port, read_port_markers, sort_ports_clockwise
from gdsfactory.snap import snap_to_grid
from gdsfactory.typings import AngleInDegrees, LayerSpec


def _should_skip_marker(
    dx: float,
    dy: float,
    min_pin_area_um2: float | None,
    max_pin_area_um2: float | None,
    skip_square_ports: bool,
    debug: bool = False,
) -> bool:
    """Return True if a pin marker should be skipped based on area or shape.

    Args:
        dx: marker width.
        dy: marker height.
        min_pin_area_um2: minimum pin area in um^2.
        max_pin_area_um2: maximum pin area in um^2.
        skip_square_ports: whether to skip square markers.
        debug: if True, print skip reasons.
    """
    area = dx * dy
    if min_pin_area_um2 and area < min_pin_area_um2:
        if debug:
            print(f"skipping port at ({dx}, {dy}) with min_pin_area_um2 {area}")
        return True
    if max_pin_area_um2 and area > max_pin_area_um2:
        return True
    if skip_square_ports and snap_to_grid(dx) == snap_to_grid(dy):
        if debug:
            print(f"skipping square port at ({dx}, {dy})")
        return True
    return False


def _infer_port_direction(
    x: float,
    y: float,
    dx: float,
    dy: float,
    pxmin: float,
    pymin: float,
    pxmax: float,
    pymax: float,
    xc: float,
    yc: float,
    dxmin: float,
    dymin: float,
    dxmax: float,
    dymax: float,
    tol: float,
    ports_on_short_side: bool = False,
) -> tuple[float, float, float, float]:
    """Infer port orientation, width, and center position from marker geometry.

    Returns:
        Tuple of (orientation, width, x, y) where orientation is in degrees
        (0=east, 90=north, 180=west, 270=south) and x, y are the center
        coordinates (unchanged from input for non-inside mode).
    """
    boundaries = [
        (0.0, dy, dxmax - pxmax),  # East
        (180.0, dy, pxmin - dxmin),  # West
        (90.0, dx, dymax - pymax),  # North
        (270.0, dx, pymin - dymin),  # South
    ]

    flush = [b for b in boundaries if abs(b[2]) < tol]
    if len(flush) == 1:
        orientation, width, _ = flush[0]
        return orientation, width, x, y

    is_horizontal = (dy < dx) if ports_on_short_side else (dx < dy)
    is_vertical = (dy > dx) if ports_on_short_side else (dx > dy)

    if is_horizontal:
        return (0.0 if x > xc else 180.0), dy, x, y
    if is_vertical:
        return (90.0 if y > yc else 270.0), dx, x, y

    for orientation, width, distance in boundaries:
        if abs(distance) < tol:
            return orientation, width, x, y

    return (0.0 if pxmax > xc else 180.0), dy, x, y


def _apply_inside_position(
    orientation: float,
    x: float,
    y: float,
    pxmin: float,
    pymin: float,
    pxmax: float,
    pymax: float,
    inside: bool,
    use_opposite_side: bool = False,
) -> tuple[float, float]:
    """Adjust port position for inside or opposite-side placement."""
    if not inside:
        return x, y

    port_mapping = {
        0.0: (True, pxmax, pxmin),  # East adjusts X
        180.0: (True, pxmin, pxmax),  # West adjusts X
        90.0: (False, pymax, pymin),  # North adjusts Y
        270.0: (False, pymin, pymax),  # South adjusts Y
    }

    if orientation not in port_mapping:
        return x, y

    modifies_x, default_val, opp_val = port_mapping[orientation]
    new_val = opp_val if use_opposite_side else default_val
    return (new_val, y) if modifies_x else (x, new_val)


def _snap_port_width(width: float, pin_extra_width: float) -> float:
    """Calculate and snap port width to the nearest 2 nm (0.002 µm).

    Args:
        width: raw port width.
        pin_extra_width: extra width offset to subtract.
    """
    return float(np.round((width - pin_extra_width) / 0.002) * 0.002)


def _auto_detect_port_layer(
    component: Component,
    x: float,
    y: float,
    width: float,
    dbu: float,
    default_layer_idx: int,
    pin_layer: int,
) -> int:
    pass


def _register_ports(
    component: Component,
    ports: list[Port],
    auto_rename_ports: bool,
    allow_none_names: bool = False,
) -> Component:
    """Sort, deduplicate, and add ports to a component.

    Args:
        component: target component.
        ports: list of ports to add.
        auto_rename_ports: if True, auto-rename ports after adding.
        allow_none_names: if True, skip ports with None names instead of raising.
    """
    ports = sort_ports_clockwise(ports)

    for port in ports:
        _port_name = port.name
        if allow_none_names and _port_name is None:
            continue
        if (
            _port_name is not None and _port_name in component.ports
        ) or port in component.ports:
            component_ports = [p.name for p in component.ports]
            raise ValueError(
                f"port {_port_name!r} already in {component_ports}. "
                "You can pass a port_name_prefix to add it with a different name."
            )
        component.add_port(name=_port_name, port=port)

    if auto_rename_ports:
        component.auto_rename_ports()
    return component


def add_ports_from_markers_square(
    component: Component,
    pin_layer: LayerSpec = "DEVREC",
    port_layer: LayerSpec | None = None,
    orientation: AngleInDegrees = 90,
    min_pin_area_um2: float = 0,
    max_pin_area_um2: float | None = 150 * 150,
    pin_extra_width: float = 0.0,
    port_names: Sequence[str] | None = None,
    port_name_prefix: str | None = None,
    port_type: str = "optical",
) -> Component:
    pass


def add_ports_from_markers_center(
    component: Component,
    pin_layer: LayerSpec,
    port_layer: LayerSpec | None = None,
    inside: bool = False,
    tol: float = 0.1,
    pin_extra_width: float = 0.0,
    min_pin_area_um2: float | None = None,
    max_pin_area_um2: float | None = None,
    skip_square_ports: bool = False,
    xcenter: float | None = None,
    ycenter: float | None = None,
    port_name_prefix: str | None = None,
    port_type: str = "optical",
    ports_on_short_side: bool = False,
    auto_rename_ports: bool = True,
    auto_detect_port_layer: bool = False,
    debug: bool = False,
) -> Component:
    pass


def add_ports_from_boxes(
    component: Component,
    pin_layer: LayerSpec,
    port_layer: LayerSpec | None = None,
    inside: bool = False,
    use_opposite_side: bool = False,
    tol: float = 0.1,
    pin_extra_width: float = 0.0,
    min_pin_area_um2: float | None = None,
    max_pin_area_um2: float | None = 150.0 * 150.0,
    skip_square_ports: bool = False,
    xcenter: float | None = None,
    ycenter: float | None = None,
    port_name_prefix: str | None = None,
    port_type: str = "optical",
    ports_on_short_side: bool = False,
    auto_rename_ports: bool = True,
    debug: bool = False,
) -> Component:
    pass


add_ports_from_markers_inside = partial(add_ports_from_markers_center, inside=True)


def add_ports_from_labels(
    component: Component,
    port_width: float,
    port_layer: LayerSpec,
    xcenter: float | None = None,
    port_name_prefix: str | None = None,
    port_type: str = "optical",
    get_name_from_label: bool = False,
    layer_label: LayerSpec | None = None,
    fail_on_duplicates: bool = False,
    port_orientation: AngleInDegrees = 0,
    guess_port_orientation: bool = True,
    port_filter_prefix: str | None = None,
    skip_duplicates: bool = False,
) -> Component:
    """Add ports from labels.

    Assumes that all ports have a label at the port center.
    because labels do not have width, you have to manually specify the ports width

    Args:
        component: to read polygons from and to write ports to.
        port_width: for ports.
        port_layer: for the new created port.
        xcenter: center of the component, for guessing port orientation.
        port_name_prefix: defaults to 'o' for optical and 'e' for electrical.
        port_type: optical, electrical.
        get_name_from_label: uses the label text as port name.
        layer_label: layer for the label.
        fail_on_duplicates: raises ValueError for duplicated port names.
            if False adds incremental suffix (1, 2 ...) to port name.
        port_orientation: None for electrical ports.
        guess_port_orientation: assumes right: 0, left: 180, top: 90, bot: 270.
        port_filter_prefix: prefix for the port name.
        skip_duplicates: if True skips ports with the same name.
    """
    port_name_prefix_default = "o" if port_type == "optical" else "e"
    port_name_prefix = port_name_prefix or port_name_prefix_default
    yc = component.y

    port_name_to_index: dict[str, int] = {}
    layer_label = layer_label or port_layer

    label_names = set()

    xc = xcenter or component.x
    for i, label in enumerate(component.get_labels(layer=layer_label)):
        dx = label.x
        dy = label.y

        if skip_duplicates and label.string in label_names:
            print("Skipping duplicate label:", label.string)
            continue

        label_names.add(label.string)

        if port_filter_prefix and not label.string.startswith(port_filter_prefix):
            continue

        if get_name_from_label:
            port_name = label.string
        else:
            port_name = f"{port_name_prefix}{i + 1}" if port_name_prefix else str(i)

        orientation = port_orientation

        if guess_port_orientation:
            if dx > xc:  # east
                orientation = 0
            elif dx < xc:  # west
                orientation = 180
            elif dy > yc:  # north
                orientation = 90
            elif dy < yc:  # south
                orientation = 270

        if fail_on_duplicates and port_name in component.ports:
            component_ports = [port.name for port in component.ports]
            raise ValueError(
                f"port {port_name!r} already in {component_ports}. "
                "You can pass a port_name_prefix to add it with a different name."
            )
        if get_name_from_label and port_name in component.ports:
            port_name_to_index[port_name] = (
                port_name_to_index[port_name] + 1
                if port_name in port_name_to_index
                else 1
            )
            port_name = f"{port_name}{port_name_to_index[port_name]}"

        component.add_port(
            name=port_name,
            center=(dx, dy),
            width=port_width,
            orientation=orientation,
            port_type=port_type,
            layer=port_layer,
        )
    return component


def add_ports_from_siepic_pins(
    component: Component,
    pin_layer: LayerSpec = "PORT",
    port_layer: LayerSpec | None = None,
    port_type: str = "optical",
) -> Component:
    """Add ports from SiEPIC-type cells, where the pins are defined as paths.

    Looks for label, path pairs.

    Args:
        component: component.
        pin_layer: layer for optical pins.
        port_layer: layer for optical ports.
        port_type: optical, electrical.
    """
    port_layer = port_layer or pin_layer

    pin_layer = gf.get_layer(pin_layer)
    port_layer = gf.get_layer(port_layer)

    c = component
    paths = c.get_paths(pin_layer)
    port_prefix = "o" if port_type == "optical" else "e"

    for i, path in enumerate(paths):
        p1, p2 = list(path.each_point())
        v = p2 - p1
        if v.x < 0:
            orientation = 2
        elif v.x > 0:
            orientation = 0
        elif v.y > 0:
            orientation = 1
        else:
            orientation = 3

        c.create_port(
            name=f"{port_prefix}{i + 1}",
            width=round(path.width / c.kcl.dbu) * c.kcl.dbu,
            dcplx_trans=gf.kdb.DCplxTrans(
                1, orientation, False, path.bbox().center().to_v()
            ),
            layer=port_layer,
            port_type=port_type,
        )

    return c
