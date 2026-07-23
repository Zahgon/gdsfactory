from __future__ import annotations

__all__ = ["array_hexagonal"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec


@gf.cell_with_module_name(tags=["containers"])
def array_hexagonal(
    component: ComponentSpec = "circle",
    columns: int = 10,
    rows: int = 10,
    pitch: float = 25.0,
    centered: bool = True,
    add_ports: bool = True,
) -> Component:
    pass


if __name__ == "__main__":
    c = array_hexagonal()
    c.show()
