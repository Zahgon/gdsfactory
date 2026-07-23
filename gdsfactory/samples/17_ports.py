
from __future__ import annotations

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec

gf.gpdk.PDK.activate()


@gf.cell
def component_with_port(
    length: float = 5.0, width: float = 0.5, layer: LayerSpec = "WG"
) -> Component:
    pass


def test_component_with_port() -> None:
    pass


if __name__ == "__main__":
    c = component_with_port()
    c.show()
