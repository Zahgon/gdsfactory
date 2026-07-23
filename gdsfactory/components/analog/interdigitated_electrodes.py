from __future__ import annotations

__all__ = ["interdigitated_electrodes"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["analog"])
def interdigitated_electrodes(
    n_fingers: int = 10,
    finger_width: float = 0.5,
    finger_length: float = 10.0,
    finger_gap: float = 0.5,
    bus_width: float = 2.0,
    bus_length: float | None = None,
    layer: LayerSpec = "MTOP",
    port_type: str = "electrical",
) -> Component:
    pass


if __name__ == "__main__":
    c = interdigitated_electrodes()
    c.show()
