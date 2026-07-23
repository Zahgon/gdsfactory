from __future__ import annotations

__all__ = ["bbox", "bbox_to_points"]

import gdsfactory as gf
from gdsfactory.component import ComponentReference
from gdsfactory.typings import LayerSpec


def bbox_to_points(
    bbox: gf.kdb.DBox,
    top: float = 0,
    bottom: float = 0,
    left: float = 0,
    right: float = 0,
) -> list[tuple[float, float]]:
    pass


@gf.cell_with_module_name(tags=["shapes"])
def bbox(
    component: gf.Component | ComponentReference,
    layer: LayerSpec,
    top: float = 0,
    bottom: float = 0,
    left: float = 0,
    right: float = 0,
) -> gf.Component:
    """Returns bounding box rectangle from coordinates.

    Args:
        component: component or instance to get bbox from.
        layer: for bbox.
        top: north offset.
        bottom: south offset.
        left: west offset.
        right: east offset.
    """
    c = gf.Component()
    if not isinstance(component, ComponentReference):
        component = gf.get_component(component)

    bbox = component.dbbox()
    xmin, ymin, xmax, ymax = bbox.left, bbox.bottom, bbox.right, bbox.top
    points = [
        (xmin - left, ymin - bottom),
        (xmax + right, ymin - bottom),
        (xmax + right, ymax + top),
        (xmin - left, ymax + top),
    ]
    c.add_polygon(points, layer=layer)
    return c
