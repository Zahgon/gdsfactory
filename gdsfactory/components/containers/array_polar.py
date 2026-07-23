from __future__ import annotations

__all__ = ["array_polar"]

import numpy as np
from kfactory.conf import CheckInstances

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec


@gf.cell(
    with_module_name=True,
    check_instances=CheckInstances.IGNORE,
    tags=["containers"],
)
def array_polar(
    component: ComponentSpec = "C",
    n_items: int = 6,
    radius: float = 50.0,
    start_angle: float = 0.0,
    end_angle: float = 360.0,
    rotate_items: bool = True,
    add_ports: bool = True,
) -> Component:
    pass


if __name__ == "__main__":
    c = array_polar()
    c.show()
