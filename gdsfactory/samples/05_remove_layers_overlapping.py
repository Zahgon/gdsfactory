
from __future__ import annotations

import gdsfactory as gf
from gdsfactory.component import Component

gf.gpdk.PDK.activate()


@gf.cell
def remove_layers_overlapping() -> Component:
    pass


if __name__ == "__main__":
    c = remove_layers_overlapping()
    c.show()
