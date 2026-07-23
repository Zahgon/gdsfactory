
from __future__ import annotations

import gdsfactory as gf
from gdsfactory.port import Port

gf.gpdk.PDK.activate()


@gf.cell(cache={})
def test_connect_bundle_udirect(
    dy: int = 200, orientation: int = 270, layer: tuple[int, int] = (1, 0)
) -> gf.Component:
    pass


if __name__ == "__main__":
    c = test_connect_bundle_udirect()
    c.show()
