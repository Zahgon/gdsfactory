from __future__ import annotations

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

gf.gpdk.PDK.activate()


@gf.cell
def ring_single_sample(
    gap: float = 0.2,
    radius: float = 10.0,
    length_x: float = 4.0,
    length_y: float = 0.010,
    coupler_ring: ComponentSpec = "coupler_ring",
    straight: ComponentSpec = "straight",
    bend: ComponentSpec = "bend_euler",
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass


def test_ring_single_sample() -> None:
    pass


if __name__ == "__main__":
    c = ring_single_sample()
    c.pprint_ports()
    c.show()
