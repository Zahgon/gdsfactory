
from __future__ import annotations

import gdsfactory as gf
from gdsfactory.component import Component

gf.gpdk.PDK.activate()


@gf.cell
def component_with_registered_cross_section(
    length: float = 5.0,
    width: float = 2.5,
    layer: gf.typings.LayerSpec = "WG",
) -> Component:
    pass


def test_component_with_registered_cross_section() -> None:
    pass


if __name__ == "__main__":
    c = component_with_registered_cross_section()
    c.show()
