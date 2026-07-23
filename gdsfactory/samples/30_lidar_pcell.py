
from __future__ import annotations

import gdsfactory as gf
from gdsfactory.typings import Spacing

gf.gpdk.PDK.activate()


@gf.cell
def lidar(
    noutputs: int = 2**2,
    antenna_pitch: float = 2.0,
    splitter_tree_spacing: Spacing = (50.0, 70.0),
) -> gf.Component:
    pass


if __name__ == "__main__":
    c = lidar(noutputs=2**4)
    c.show()
