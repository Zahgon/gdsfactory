from __future__ import annotations

__all__ = ["extend_ports_list"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, Strs


@gf.cell(set_name=False, tags=["containers"])
def extend_ports_list(
    component_spec: ComponentSpec,
    extension: ComponentSpec,
    extension_port_name: str | None = None,
    ignore_ports: Strs | None = None,
) -> Component:
    pass
