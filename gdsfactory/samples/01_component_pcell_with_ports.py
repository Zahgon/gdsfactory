
from __future__ import annotations

import gdsfactory as gf
from gdsfactory.typings import LayerSpec

gf.gpdk.PDK.activate()


@gf.cell
def straight_narrow(
    length: float = 5.0, width: float = 0.3, layer: LayerSpec = (1, 0)
) -> gf.Component:
    pass


if __name__ == "__main__":
    c = straight_narrow()
    c.show()
