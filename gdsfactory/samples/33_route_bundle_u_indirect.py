
from __future__ import annotations

import gdsfactory as gf
from gdsfactory.port import Port

gf.gpdk.PDK.activate()


@gf.cell
def test_connect_bundle_u_indirect(
    dy: int = -200, orientation: int = 180, layer: tuple[int, int] = (1, 0)
) -> gf.Component:
    pass


if __name__ == "__main__":
    c = test_connect_bundle_u_indirect(orientation=0)
    c.show()
