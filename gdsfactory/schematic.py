import json
import pathlib
from pathlib import Path
from typing import Any, Self

import networkx as nx
import yaml
from graphviz import Digraph
from pydantic import BaseModel, ConfigDict, Field, model_validator

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.config import PATH
from gdsfactory.typings import Anchor, Delta, Port, Ports
from gdsfactory.utils import is_component_spec


class OrthogonalGridArray(BaseModel):

    columns: int = 1
    rows: int = 1
    column_pitch: float = 0
    row_pitch: float = 0


class GridArray(BaseModel):

    num_a: int = 1
    num_b: int = 1
    pitch_a: tuple[float, float] = (1.0, 0.0)
    pitch_b: tuple[float, float] = (0.0, 1.0)


type Array = OrthogonalGridArray | GridArray


class Instance(BaseModel):

    component: str
    settings: dict[str, Any] = Field(default_factory=dict)
    info: dict[str, Any] = Field(default_factory=dict, exclude=True)
    array: Array | None = None
    virtual: bool = False

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="before")
    @classmethod
    def update_settings_and_info(cls, values: dict[str, Any]) -> dict[str, Any]:
        pass

    @model_validator(mode="after")
    def validate_array(self) -> Self:
        pass


class Placement(BaseModel):
    x: str | float | None = None
    y: str | float | None = None
    xmin: str | float | None = None
    ymin: str | float | None = None
    xmax: str | float | None = None
    ymax: str | float | None = None
    dx: Delta = 0
    dy: Delta = 0
    port: str | Anchor | None = None
    rotation: float = 0
    mirror: bool | str | float = False

    def __getitem__(self, key: str) -> Any:
        """Allows to access the placement attributes as a dictionary."""
        return getattr(self, key, 0)

    model_config = ConfigDict(extra="forbid")


class Bundle(BaseModel):
    links: dict[str, str]
    settings: dict[str, Any] = Field(default_factory=dict)
    routing_strategy: str = "route_bundle"

    model_config = ConfigDict(extra="forbid")


class Net(BaseModel):

    p1: str
    p2: str
    settings: dict[str, Any] = Field(default_factory=dict)
    name: str | None = None

    def __init__(self, **data: Any) -> None:
        """Initialize the net."""
        global _route_counter
        super().__init__(**data)
        if self.name is None:
            self.name = f"route_{_route_counter}"
            _route_counter += 1


class Netlist(BaseModel):

    pdk: str = ""
    instances: dict[str, Instance] = Field(default_factory=dict)
    placements: dict[str, Placement] = Field(default_factory=dict)
    connections: dict[str, str] = Field(default_factory=dict)
    routes: dict[str, Bundle] = Field(default_factory=dict)
    name: str | None = None
    info: dict[str, Any] = Field(default_factory=dict)
    ports: dict[str, str] = Field(default_factory=dict)
    settings: dict[str, Any] = Field(default_factory=dict, exclude=True)
    nets: list[Net] = Field(default_factory=list)
    warnings: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_instance_names(self) -> Self:
        pass


_route_counter = 0


def to_yaml_graph_networkx(
    netlist: Netlist, nets: list[Net]
) -> tuple[nx.Graph, dict[str, str], dict[str, tuple[float, float]]]:
    pass


def to_graphviz(
    instances: dict[str, Instance],
    placements: dict[str, Placement],
    nets: list[Net],
    show_ports: bool = True,
) -> Digraph:
    pass


class Link(BaseModel):

    instance1: str
    instance2: str
    port1: str
    port2: str


class Schematic(BaseModel):

    netlist: Netlist = Field(default_factory=Netlist)
    nets: list[Net] = Field(default_factory=list)
    placements: dict[str, Placement] = Field(default_factory=dict)
    links: list[Link] = Field(default_factory=list)

    def add_instance(
        self, name: str, instance: Instance, placement: Placement | None = None
    ) -> None:
        pass

    def add_placement(
        self,
        instance_name: str,
        placement: Placement,
    ) -> None:
        pass

    def from_component(self, component: Component) -> None:
        raise NotImplementedError

    def add_net(self, net: Net) -> None:
        pass

    def to_graphviz(self, show_ports: bool = True) -> Digraph:
        pass

    def to_yaml_graph_networkx(
        self,
    ) -> tuple[nx.Graph, dict[str, str], dict[str, tuple[float, float]]]:
        pass

    def plot_graphviz(self, interactive: bool = False, splines: str = "ortho") -> None:
        pass

    def write_netlist(
        self, netlist: dict[str, Any], filepath: str | pathlib.Path | None = None
    ) -> str:
        pass


def plot_graphviz(
    graph: Digraph, interactive: bool = False, splines: str = "ortho"
) -> None:
    pass


def write_schema(
    model: type[BaseModel] = Netlist, schema_path_json: Path = PATH.schema_netlist
) -> None:
    pass


def _validate_instance_name(name: str) -> str:
    pass
