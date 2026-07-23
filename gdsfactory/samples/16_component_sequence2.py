from __future__ import annotations

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components import component_sequence, straight, taper_strip_to_ridge

gf.gpdk.PDK.activate()


@gf.cell
def cutback_phase(
    straight_length: float = 100.0, bend_radius: float = 12.0, n: int = 2
) -> Component:
    pass


def test_cutback_phase() -> None:
    pass


if __name__ == "__main__":
    c = cutback_phase(n=1)
    c.show()
