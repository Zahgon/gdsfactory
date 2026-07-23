from __future__ import annotations

__all__ = ["meander_channel"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["microfluidics"])
def meander_channel(
    channel_width: float = 1.0,
    n_turns: int = 5,
    turn_spacing: float = 5.0,
    straight_length: float = 20.0,
    reservoir_length: float = 5.0,
    reservoir_height: float = 5.0,
    layer: LayerSpec = "WG",
    port_type: str | None = "optical",
) -> Component:
    pass


if __name__ == "__main__":
    c = meander_channel()
    c.show()
