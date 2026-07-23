
from __future__ import annotations

import csv
import functools
import warnings
from collections.abc import Callable, Sequence
from functools import partial
from typing import TYPE_CHECKING, Any, Literal, TypedDict, Unpack, cast

import kfactory as kf
import numpy as np
from kfactory import DPort as Port  # runtime re-export of a class
from rich.console import Console
from rich.table import Table

from gdsfactory import typings
from gdsfactory.typings import (
    AngleInDegrees,
    ComponentFactory,
    CrossSectionSpec,
    LayerSpec,
    LayerSpecs,
    PathType,
    PortDict,
    Ports,
    PortsDict,
    PortsDictGeneric,
    SelectPorts,
    TPort,
)

if TYPE_CHECKING:
    from gdsfactory.component import Component, ComponentReference

valid_error_types = ["error", "warn", "ignore"]


class PortNotOnGridError(ValueError):
    pass


class PortTypeError(ValueError):
    pass


class PortOrientationError(ValueError):
    pass


def get_port_definitions(ports: Ports) -> str:
    pass


def pprint_ports(ports: Ports) -> None:
    pass


def to_dict(port: kf.port.ProtoPort[Any]) -> dict[str, Any]:
    """Returns dict."""
    return {
        "name": port.name,
        "center": port.center,
        "width": port.width,
        "orientation": port.orientation,
        "layer": port.layer,
        "port_type": port.port_type,
    }


class PortKwargs(TypedDict, total=False):
    layer: int
    port_type: str
    cross_section: CrossSectionSpec
    info: dict[str, int | float | str]


def port_array(
    center: tuple[float, float] = (0.0, 0.0),
    width: float = 0.5,
    orientation: AngleInDegrees = 0,
    pitch: tuple[float, float] = (10.0, 0.0),
    n: int = 2,
    **kwargs: Unpack[PortKwargs],
) -> list[Port]:
    pass


def read_port_markers(
    component: Component, layers: LayerSpecs = ("PORT",)
) -> Component:
    """Returns extracted polygons from component layers.

    Args:
        component: Component to extract markers.
        layers: GDS layer specs.

    """
    from gdsfactory.pdk import get_layer

    layers = [get_layer(layer) for layer in layers]
    return component.extract(layers=layers)


def csv2port(csvpath: PathType) -> dict[str, list[str]]:
    pass


def sort_ports_clockwise(ports: Sequence[TPort]) -> list[TPort]:
    """Sort and return ports in the clockwise direction.

    ```text
        3   4
        |___|_
    2 -|      |- 5
       |      |
    1 -|______|- 6
        |   |
        8   7
    ```

    """
    direction_ports: PortsDictGeneric[TPort] = {x: [] for x in ["E", "N", "W", "S"]}

    for p in ports:
        angle = p.angle * 90
        if angle <= 45 or angle >= 315:
            direction_ports["E"].append(p)
        elif angle <= 135:
            direction_ports["N"].append(p)
        elif angle <= 225:
            direction_ports["W"].append(p)
        else:
            direction_ports["S"].append(p)

    east_ports = direction_ports["E"]
    east_ports.sort(key=lambda p: -p.y)  # sort north to south

    north_ports = direction_ports["N"]
    north_ports.sort(key=lambda p: +p.x)  # sort west to east

    west_ports = direction_ports["W"]
    west_ports.sort(key=lambda p: +p.y)  # sort south to north

    south_ports = direction_ports["S"]
    south_ports.sort(key=lambda p: -p.x)  # sort east to west

    ports = west_ports + north_ports + east_ports + south_ports
    return ports


def sort_ports_counter_clockwise(ports: Sequence[TPort]) -> list[TPort]:
    """Sort and return ports in the counter-clockwise direction.

    ```text
        4   3
        |___|_
    5 -|      |- 2
       |      |
    6 -|______|- 1
        |   |
        7   8
    ```

    """
    direction_ports: PortsDictGeneric[TPort] = {x: [] for x in ["E", "N", "W", "S"]}

    for p in ports:
        angle = p.angle * 90
        if angle <= 45 or angle >= 315:
            direction_ports["E"].append(p)
        elif angle <= 135:
            direction_ports["N"].append(p)
        elif angle <= 225:
            direction_ports["W"].append(p)
        else:
            direction_ports["S"].append(p)

    east_ports = direction_ports["E"]
    east_ports.sort(key=lambda p: +p.y)  # sort south to north

    north_ports = direction_ports["N"]
    north_ports.sort(key=lambda p: -p.x)  # sort east to west

    west_ports = direction_ports["W"]
    west_ports.sort(key=lambda p: -p.y)  # sort north to south

    south_ports = direction_ports["S"]
    south_ports.sort(key=lambda p: +p.x)  # sort west to east

    ports = east_ports + north_ports + west_ports + south_ports
    return list(ports)


def select_ports(
    ports: Ports | ComponentReference,
    layer: LayerSpec | None = None,
    prefix: str | None = None,
    suffix: str | None = None,
    orientation: AngleInDegrees | None = None,
    width: float | None = None,
    layers_excluded: Sequence[tuple[int, int]] | None = None,
    port_type: str | None = None,
    names: Sequence[str] | None = None,
    clockwise: bool = True,
    sort_ports: bool = False,
) -> list[typings.Port]:
    """Returns a list of ports from a list of ports.

    Args:
        ports: port list.
        layer: select ports with port GDS layer.
        prefix: select ports with port name prefix.
        suffix: select ports with port name suffix.
        orientation: select ports with orientation in degrees.
        width: select ports with port width.
        layers_excluded: List of layers to exclude.
        port_type: select ports with port type (optical, electrical, vertical_te).
        names: select ports with port names.
        clockwise: if True, sort ports clockwise, False: counter-clockwise.
        sort_ports: if True, sort ports.

    Returns:
        List containing the selected ports.

    """
    from gdsfactory.component import ComponentReference

    if isinstance(ports, ComponentReference):
        ports_ = list(ports.ports)
    else:
        ports_ = list(ports)

    from gdsfactory.pdk import get_layer

    if layer is not None:
        layer_index = get_layer(layer)
        ports_ = [p for p in ports_ if p.layer == layer_index]
    else:
        ports_ = list(ports_)

    if prefix:
        ports_ = [p for p in ports_ if p.name and p.name.startswith(prefix)]
    if suffix:
        ports_ = [p for p in ports_ if p.name and p.name.endswith(suffix)]
    if orientation is not None:
        ports_ = [p for p in ports_ if np.isclose(p.orientation, orientation)]

    if layers_excluded:
        excluded_layers = {get_layer(layer) for layer in layers_excluded}
        ports_ = [p for p in ports_ if p.layer not in excluded_layers]
    if width:
        ports_ = [p for p in ports_ if p.width == width]
    if port_type:
        ports_ = [p for p in ports_ if p.port_type == port_type]
    if names:
        ports_ = [p for p in ports_ if p.name in names]

    if sort_ports:
        if clockwise:
            ports_ = list(sort_ports_clockwise(ports_))
        else:
            ports_ = list(sort_ports_counter_clockwise(ports_))
    return ports_


select_ports_optical = partial(select_ports, port_type="optical")
select_ports_electrical = partial(select_ports, port_type="electrical")
select_ports_placement = partial(select_ports, port_type="placement")


def select_ports_list(
    ports: Ports | Ports | ComponentReference, **kwargs: Any
) -> Ports:
    pass


get_ports_list = select_ports_list


def flipped(port: typings.Port) -> typings.Port:
    p = port.copy()
    p.trans *= kf.kdb.Trans.R180
    return p


def move_copy(port: typings.Port, x: int = 0, y: int = 0) -> typings.Port:
    pass


def get_ports_facing(
    ports: Sequence[typings.Port], direction: str = "W"
) -> list[typings.Port]:
    pass


def deco_rename_ports(component_factory: ComponentFactory) -> ComponentFactory:
    pass


def _rename_ports_facing_side(
    direction_ports: dict[str, list[Port]], prefix: str = ""
) -> None:
    pass


def _rename_ports_facing_side_ccw(
    direction_ports: dict[str, list[Port]], prefix: str = ""
) -> None:
    pass


def _rename_ports_counter_clockwise(
    direction_ports: dict[Literal["N", "E", "S", "W"], list[Port]],
    prefix: str = "",
) -> None:
    pass


def _rename_ports_clockwise(direction_ports: PortsDict, prefix: str = "") -> None:
    pass


def _rename_ports_clockwise_top_right(
    direction_ports: PortsDict, prefix: str = ""
) -> None:
    pass


def rename_ports_by_orientation(
    component: Component,
    layers_excluded: LayerSpecs | None = None,
    select_ports: SelectPorts = select_ports,
    function: Callable[..., None] = _rename_ports_facing_side,
    prefix: str = "o",
    **kwargs: Any,
) -> Component:
    """Returns Component with port names based on port orientation (E, N, W, S).

    Args:
        component: to rename ports.
        layers_excluded: to exclude.
        select_ports: function to select_ports.
        function: to rename ports.
        prefix: to add on each port name.
        kwargs: select_ports settings.

             N0  N1
             |___|_
        W1 -|      |- E1
            |      |
        W0 -|______|- E0
             |   |
            S0   S1

    """
    layers_excluded = layers_excluded or []
    direction_ports: PortsDict = {x: [] for x in ["E", "N", "W", "S"]}

    ports = list(select_ports(component.ports, **kwargs))

    ports_on_layer = [p for p in ports if p.layer not in layers_excluded]

    for p in ports_on_layer:
        angle = p.orientation % 360
        if angle <= 45 or angle >= 315:
            direction_ports["E"].append(p)
        elif angle <= 135:
            direction_ports["N"].append(p)
        elif angle <= 225:
            direction_ports["W"].append(p)
        else:
            direction_ports["S"].append(p)

    function(direction_ports, prefix=prefix)
    return component


def auto_rename_ports(
    component: Component,
    function: Callable[..., None] = _rename_ports_clockwise,
    select_ports_optical: Callable[..., list[typings.Port]]
    | None = select_ports_optical,
    select_ports_electrical: Callable[..., list[typings.Port]]
    | None = select_ports_electrical,
    select_ports_placement: Callable[..., list[typings.Port]]
    | None = select_ports_placement,
    prefix: str = "",
    prefix_optical: str = "o",
    prefix_electrical: str = "e",
    prefix_placement: str = "p",
    port_type: str | None = None,
    **kwargs: Any,
) -> Component:
    """Adds prefix for optical and electrical.

    Args:
        component: to auto_rename_ports.
        function: to rename ports.
        select_ports_optical: to select optical ports.
        select_ports_electrical: to select electrical ports.
        select_ports_placement: to select placement ports.
        prefix_optical: prefix of optical ports.
        prefix_electrical: prefix of electrical ports.
        prefix_placement: prefix of electrical ports.
        port_type: select ports with port type (optical, electrical, vertical_te).
        kwargs: select_ports settings.

    Keyword Args:
        prefix: select ports with port name prefix.
        suffix: select ports with port name suffix.
        orientation: select ports with orientation in degrees.
        width: select ports with port width.
        layers_excluded: List of layers to exclude.
        clockwise: if True, sort ports clockwise, False: counter-clockwise.

    """
    if port_type is None:
        if select_ports_optical:
            rename_ports_by_orientation(
                component=component,
                select_ports=select_ports_optical,
                prefix=prefix_optical,
                function=function,
                **kwargs,
            )
        if select_ports_electrical:
            rename_ports_by_orientation(
                component=component,
                select_ports=select_ports_electrical,
                prefix=prefix_electrical,
                function=function,
                **kwargs,
            )
        if select_ports_placement:
            rename_ports_by_orientation(
                component=component,
                select_ports=select_ports_placement,
                prefix=prefix_placement,
                function=function,
                **kwargs,
            )
    else:
        rename_ports_by_orientation(
            component=component,
            select_ports=select_ports,
            prefix=prefix,
            function=function,
            port_type=port_type,
            **kwargs,
        )
    return component


auto_rename_ports_counter_clockwise = partial(
    auto_rename_ports, function=_rename_ports_counter_clockwise
)
auto_rename_ports_orientation = partial(
    auto_rename_ports, function=_rename_ports_facing_side
)

auto_rename_ports_electrical = partial(auto_rename_ports, select_ports_optical=None)


def map_ports_layer_to_orientation(
    ports: PortDict,
    function: Callable[..., None] = _rename_ports_facing_side,
    **kwargs: Any,
) -> dict[str, str]:
    pass


def map_ports_to_orientation_cw(
    ports: PortDict,
    function: Callable[..., None] = _rename_ports_facing_side,
    **kwargs: Any,
) -> dict[str, str]:
    pass


map_ports_to_orientation_ccw = partial(
    map_ports_to_orientation_cw, function=_rename_ports_facing_side_ccw
)


def auto_rename_ports_layer_orientation(
    component: Component,
    function: Callable[..., None] = _rename_ports_facing_side,
) -> None:
    pass


__all__ = [
    "Port",
    "auto_rename_ports",
    "auto_rename_ports_counter_clockwise",
    "auto_rename_ports_orientation",
    "csv2port",
    "deco_rename_ports",
    "flipped",
    "get_ports_facing",
    "map_ports_layer_to_orientation",
    "move_copy",
    "port_array",
    "read_port_markers",
    "rename_ports_by_orientation",
    "select_ports",
    "select_ports_list",
]
