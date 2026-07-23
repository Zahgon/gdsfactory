
from __future__ import annotations

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components import (
    bend_circular,
    component_sequence,
    straight,
    straight_pn,
)

gf.gpdk.PDK.activate()


@gf.cell
def cutback_pn() -> Component:
    pass


def test_cutback_pn() -> None:
    pass


if __name__ == "__main__":
    c = cutback_pn()
    c.show()
