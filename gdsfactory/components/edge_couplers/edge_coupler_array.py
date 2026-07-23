from __future__ import annotations

__all__ = [
    "edge_coupler_array",
    "edge_coupler_array_with_loopback",
    "edge_coupler_silicon",
]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec, Float2

from .._schematic import taper_schematic


@gf.cell_with_module_name(schematic_function=taper_schematic, tags=["edge_couplers"])
def edge_coupler_silicon(
    length: float = 100,
    width1: float = 0.5,
    width2: float = 0.2,
    with_two_ports: bool = True,
    port_names: tuple[str, str] = ("o1", "o2"),
    port_types: tuple[str, str] = ("optical", "edge_coupler"),
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass


@gf.cell_with_module_name(tags=["edge_couplers"])
def edge_coupler_array(
    edge_coupler: ComponentSpec = "edge_coupler_silicon",
    n: int = 5,
    pitch: float = 127.0,
    x_reflection: bool = False,
    text: ComponentSpec | None = "text_rectangular",
    text_offset: Float2 = (10, 20),
    text_rotation: float = 0,
) -> Component:
    pass


@gf.cell_with_module_name(tags=["edge_couplers"])
def edge_coupler_array_with_loopback(
    edge_coupler: ComponentSpec = "edge_coupler_silicon",
    cross_section: CrossSectionSpec = "strip",
    radius: float | None = None,
    n: int = 8,
    pitch: float = 127.0,
    x_reflection: bool = False,
    text: ComponentSpec | None = "text_rectangular",
    text_offset: Float2 = (0, 10),
    text_rotation: float = 0,
) -> Component:
    pass


if __name__ == "__main__":
    c = edge_coupler_array_with_loopback(
        n=5,
        pitch=127.0,
        x_reflection=False,
        text="text_rectangular",
        text_offset=(0, 10),
        text_rotation=0,
    )
    c.pprint_ports()
    c.show()
