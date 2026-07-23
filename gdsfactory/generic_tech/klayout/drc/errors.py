from __future__ import annotations

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import Float2, Layer

layer = (1, 0)
nm = 1e-3


@gf.cell
def _width_min(size: Float2 = (0.1, 0.1)) -> Component:
    pass


@gf.cell
def _area_min() -> Component:
    pass


@gf.cell
def _gap_min(gap: float = 0.1) -> Component:
    pass


@gf.cell
def _separation(
    gap: float = 0.1, layer1: Layer = (47, 0), layer2: Layer = (41, 0)
) -> Component:
    pass


@gf.cell
def _enclosing(
    enclosing: float = 0.1, layer1: Layer = (40, 0), layer2: Layer = (41, 0)
) -> Component:
    pass


@gf.cell
def _snapping_error(gap: float = 1e-3) -> Component:
    pass


@gf.cell
def _not_inside(layer: Layer = (40, 0), not_inside: Layer = (24, 0)) -> Component:
    pass


@gf.cell
def errors() -> Component:
    pass
