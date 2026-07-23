
from __future__ import annotations

import gdsfactory as gf

gf.gpdk.PDK.activate()


@gf.cell
def sample_lidar_with_pads(
    elements: int = 2**2,
    antenna_pitch: float = 2.0,
    splitter_tree_spacing: tuple[float, float] = (50.0, 70.0),
) -> gf.Component:
    pass


if __name__ == "__main__":
    c = sample_lidar_with_pads(elements=2**4)
    c.show()
