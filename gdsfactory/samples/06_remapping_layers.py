
from __future__ import annotations

import gdsfactory as gf
from gdsfactory.component import Component

gf.gpdk.PDK.activate()


@gf.cell
def remap_layers() -> Component:
    pass


def test_remap_layers() -> None:
    pass


if __name__ == "__main__":
    c = remap_layers()
    c.show()
