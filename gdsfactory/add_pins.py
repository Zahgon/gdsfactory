
from __future__ import annotations

import json
import warnings
from collections.abc import Sequence
from functools import partial
from typing import Any, Protocol, cast

import kfactory as kf
import numpy as np
import numpy.typing as npt
import yaml

import gdsfactory as gf
from gdsfactory import typings
from gdsfactory.component import Component, ComponentReference, container
from gdsfactory.config import CONF
from gdsfactory.port import select_ports
from gdsfactory.typings import InstanceOrVInstance

nm = 1e-3


def _rotate(
    vector: npt.NDArray[np.floating[Any]],
    rotation_matrix: npt.NDArray[np.floating[Any]],
) -> npt.NDArray[np.floating[Any]]:
    pass


def add_bbox(
    component: Component,
    bbox_layer: typings.LayerSpec = "DEVREC",
    top: float = 0,
    bottom: float = 0,
    left: float = 0,
    right: float = 0,
) -> Component:
    """Add bbox on outline.

    Args:
        component: component to add bbox.
        bbox_layer: bbox layer.
        top: padding.
        bottom: padding.
        left: padding.
        right: padding.
    """
    from gdsfactory.pdk import get_layer

    layer = get_layer(bbox_layer)
    bbox = component.dbbox()
    dxmin, dymin, dxmax, dymax = bbox.left, bbox.bottom, bbox.right, bbox.top
    points = [
        (dxmin - left, dymin - bottom),
        (dxmax + right, dymin - bottom),
        (dxmax + right, dymax + top),
        (dxmin - left, dymax + top),
    ]
    component.add_polygon(points, layer=layer)
    return component


def add_bbox_siepic(
    component: Component,
    bbox_layer: typings.LayerSpec = "DEVREC",
    remove_layers: typings.LayerSpecs = ("PORT", "PORTE"),
) -> Component:
    pass


def get_pin_triangle_polygon_tip(
    port: typings.Port,
) -> tuple[npt.NDArray[np.floating[Any]], tuple[float, float]]:
    pass


def add_pin_triangle(
    component: Component,
    port: typings.Port,
    layer: typings.LayerSpec = "PORT",
    layer_label: typings.LayerSpec | None = "TEXT",
) -> None:
    pass


def add_pin_rectangle_inside(
    component: Component,
    port: typings.Port,
    pin_length: float = 0.1,
    layer: typings.LayerSpec = "PORT",
    layer_label: typings.LayerSpec | None = "TEXT",
) -> None:
    pass


def add_pin_rectangle(
    component: Component,
    port: typings.Port,
    pin_length: float = 0.1,
    layer: typings.LayerSpec | None = "PORT",
    layer_label: typings.LayerSpec | None = "TEXT",
    port_margin: float = 0.0,
) -> None:
    pass


class AddPinPathFunction(Protocol):
    def __call__(
        self,
        component: Component,
        port: typings.Port,
        pin_length: float = ...,
        layer: typings.LayerSpec = ...,
        layer_label: typings.LayerSpec | None = ...,
    ) -> None: ...


def add_pin_path(
    component: Component,
    port: typings.Port,
    pin_length: float = 2 * nm,
    layer: typings.LayerSpec = "PORT",
    layer_label: typings.LayerSpec | None = None,
) -> None:
    pass


def add_outline(
    component: Component,
    reference: ComponentReference | None = None,
    layer: typings.LayerSpec = "DEVREC",
    **kwargs: Any,
) -> None:
    pass


def add_pins_siepic(
    component: Component,
    function: AddPinPathFunction = add_pin_path,
    port_type: str = "optical",
    layer: typings.LayerSpec = "PORT",
    pin_length: float = 10 * nm,
    **kwargs: Any,
) -> Component:
    pass


add_pins_siepic_optical = add_pins_siepic
add_pins_siepic_electrical = partial(
    add_pins_siepic, port_type="electrical", layer="PORTE"
)


class AddPinFunction(Protocol):
    def __call__(
        self,
        component: Component,
        port: typings.Port,
        **kwargs: Any,
    ) -> Any: ...


def add_pins(
    component: Component,
    port_type: str | None = None,
    function: AddPinFunction = add_pin_rectangle_inside,  # type: ignore[assignment]
    skip_cross_sections: Sequence[str] | None = None,
    **kwargs: Any,
) -> None:
    """Add Pin port markers.

    Args:
        component: to add ports to.
        port_type: Which port type do you want to add pins to. optical, electrical, ...  If None, it will add to all.
        function: to add each pin.
        skip_cross_sections: list of cross_sections to skip.
        kwargs: add pins function settings.
    """
    from gdsfactory.pdk import get_component

    component = get_component(component)

    ports = select_ports(
        ports=cast(typings.Ports, component.ports),
        port_type=port_type,
    )
    if skip_cross_sections:
        ports = [
            port
            for port in ports
            if getattr(port.info, "cross_section", None) not in skip_cross_sections
        ]

    for port in ports:
        function(component, port, **kwargs)


add_pins_triangle = partial(add_pins, function=add_pin_triangle)  # type: ignore[arg-type]
add_pins_center = partial(add_pins, function=add_pin_rectangle)  # type: ignore[arg-type]
add_pin_inside1nm = partial(
    add_pin_rectangle_inside, pin_length=1 * nm, layer_label=None
)
add_pin_inside2um = partial(add_pin_rectangle_inside, pin_length=2, layer_label=None)
add_pins_inside1nm = partial(add_pins, function=add_pin_inside1nm)
add_pins_inside2um = partial(add_pins, function=add_pin_inside2um)


def add_settings_label(
    component: Component,
    reference: ComponentReference | None = None,
    layer_label: typings.LayerSpec = "LABEL_SETTINGS",
    with_yaml_format: bool = False,
) -> None:
    pass


def add_instance_label(
    component: Component,
    reference: InstanceOrVInstance,
    layer: typings.LayerSpec | None = None,
    instance_name: str | None = None,
) -> None:
    """Adds label to a reference in a component.

    Args:
        component: to add instance label.
        reference: to add label.
        layer: layer for the label.
        instance_name: label name.

    """
    try:
        layer = layer or gf.get_layer("LABEL_INSTANCE")
    except ValueError:
        warnings.warn(
            "Layer LABEL_INSTANCE not found in PDK.layers, using (1, 0)", stacklevel=3
        )
        layer = (1, 0)
    instance_name = (
        instance_name or f"{reference.cell.name},{int(reference.x)},{int(reference.y)}"
    )

    layer = layer or CONF.layer_label

    component.add_label(
        text=instance_name,
        position=reference.center,
        layer=layer,
    )


class AddInstanceLabelFunction(Protocol):
    def __call__(
        self, component: Component, reference: ComponentReference | None = None
    ) -> None: ...


class AddPinsFunction(Protocol):
    def __call__(
        self, component: Component, reference: ComponentReference | None = None
    ) -> None: ...


def add_pins_and_outline(
    component: Component,
    reference: ComponentReference | None = None,
    add_outline_function: AddInstanceLabelFunction | None = add_outline,
    add_pins_function: AddPinsFunction | None = add_pins,  # type: ignore[assignment]
    add_settings_function: AddInstanceLabelFunction | None = add_settings_label,
    add_instance_label_function: AddInstanceLabelFunction | None = add_settings_label,
) -> None:
    pass


add_pins_container = partial(container, function=add_pins)
add_pins_siepic_container = partial(container, function=add_pins_siepic)
