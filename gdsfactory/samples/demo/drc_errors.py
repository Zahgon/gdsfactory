
from __future__ import annotations

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import Float2, Layer

gf.gpdk.PDK.activate()


layer = (1, 0)


@gf.cell
def width_min(size: Float2 = (0.1, 0.1)) -> Component:
    pass


@gf.cell
def area_min() -> Component:
    pass


@gf.cell
def gap_min(gap: float = 0.1) -> Component:
    pass


@gf.cell
def separation(
    gap: float = 0.1, layer1: Layer = (47, 0), layer2: Layer = (41, 0)
) -> Component:
    pass


@gf.cell
def enclosing(
    enclosing: float = 0.1, layer1: Layer = (40, 0), layer2: Layer = (41, 0)
) -> Component:
    pass


@gf.cell
def snapping_error(gap: float = 1e-3) -> Component:
    pass


@gf.cell
def errors() -> Component:
    pass


if __name__ == "__main__":

    c = errors()
    c.show()
