
from __future__ import annotations

import pathlib
from collections.abc import Callable, Generator, Sequence
from enum import IntEnum
from functools import partial
from typing import Any, Literal, ParamSpec, Protocol, TypedDict, TypeVar

import kfactory as kf
import klayout.db as kdb
import numpy as np
import numpy.typing as npt
from kfactory import DPin as Pin  # runtime re-export of a class
from kfactory import DPins as Pins  # runtime re-export of a class
from kfactory import DPort as Port  # runtime re-export of a class
from kfactory.layer import LayerEnum

STEP_DIRECTIVES = {
    "x",
    "y",
    "dx",
    "dy",
}

STEP_DIRECTIVES_ALL_ANGLE = {
    "x",
    "y",
    "dx",
    "dy",
    "ds",
    "exit_angle",
    "cross_section",
    "connector",
    "separation",
}


class Step(TypedDict, total=False):

    x: float
    y: float
    dx: Delta
    dy: Delta


class PixelBufferOptions(TypedDict, total=False):

    width: int
    height: int
    linewidth: int
    oversampling: int
    resolution: float


type Anchor = Literal[
    "ce",
    "cw",
    "nc",
    "ne",
    "nw",
    "sc",
    "se",
    "sw",
    "center",
    "cc",
]
type Axis = Literal["x", "y"]
type NSEW = Literal["N", "S", "E", "W"]
type WidthTypes = Literal["sine", "linear", "parabolic"]

type Float2 = tuple[float, float]
type Float3 = tuple[float, float, float]
type Floats = Sequence[float]
type Strs = Sequence[str]
type Int2 = tuple[int, int]
type Int3 = tuple[int, int, int]
type Ints = tuple[int, ...] | list[int]

type BoundingBox = tuple[float, float, float, float]
type BoundingBoxes = Sequence[BoundingBox]
type Size = tuple[float, float]
type Spacing = tuple[float, float]
type Position = tuple[float, float]
type Radius = float

type Delta = float
type AngleInDegrees = float

type Layer = tuple[int, int]
type Layers = Sequence[Layer]
type LayerSpec = Layer | str | int | LayerEnum
type LayerSpecs = Sequence[LayerSpec]

type Number = float | int
type Coordinate = tuple[float, float]
type Coordinates = Sequence[Coordinate]
type WayPoints = Sequence[Coordinate | kdb.DPoint]

type MaterialSpec = (
    str | float | tuple[float, float] | Callable[..., Any] | npt.NDArray[np.float64]
)

type WidthFunction = Callable[..., npt.NDArray[np.floating[Any]]]
type OffsetFunction = Callable[[float], float]

type PathType = str | pathlib.Path
type PathTypes = Sequence[PathType]
type Metadata = dict[str, int | float | str]

TPort = TypeVar("TPort", bound=Port)
type IOPorts = tuple[str, str]
type PortFactory = Callable[..., Port]
type PortsFactory = Callable[..., Sequence[Port]]
type PortSymmetries = dict[str, Sequence[str]]
type PortDict = dict[str, Port]
type Ports = kf.DPorts | Sequence[Port] | kf.DInstancePorts
type SelectPorts = Callable[..., Sequence[Port]]

type PortType = str
type PortName = str

type PortTypes = Sequence[PortType]
type PortNames = Sequence[PortName]

type PortsDict = dict[str, list[Port]]
type PortsDictGeneric[TPort: Port] = dict[str, list[TPort]]

type ConductorConductorName = tuple[str, str]
type ConductorViaConductorName = tuple[str, str, str] | ConductorConductorName
type ConnectivitySpec = ConductorConductorName | ConductorViaConductorName

type Sparameters = dict[str, npt.NDArray[np.float64]]

type Route = (
    kf.routing.generic.ManhattanRoute | kf.routing.aa.optical.OpticalAllAngleRoute
)
type RoutingStrategy = Callable[..., Sequence[Route]]
type RoutingStrategies = dict[str, RoutingStrategy]


from gdsfactory.cross_section import CrossSectionFactory, CrossSectionSpec  # noqa: E402

type MultiCrossSectionAngleSpec = Sequence[tuple[CrossSectionSpec, tuple[int, ...]]]

from gdsfactory import component  # noqa: E402

type AnyComponent = component.Component | component.ComponentAllAngle
AnyComponentT = TypeVar("AnyComponentT", bound=AnyComponent)
type AnyComponentFactory = Callable[..., AnyComponent]
type AnyComponentPostProcess = (
    Callable[[component.Component], None]
    | Callable[[component.ComponentAllAngle], None]
)

ComponentParams = ParamSpec("ComponentParams")
type ComponentFactory = Callable[..., component.Component]
type ComponentAllAngleFactory = Callable[..., component.ComponentAllAngle]
type ComponentBaseFactory = Callable[..., component.ComponentBase]
type ComponentFactoryDict = dict[str, ComponentFactory]
type ComponentFactories = Sequence[ComponentFactory]

type ComponentSpec = (
    str | ComponentFactory | dict[str, Any] | kf.DKCell | partial[component.Component]
)
type ComponentAllAngleSpec = (
    str | ComponentAllAngleFactory | dict[str, Any] | component.ComponentAllAngle
)
type ComponentSpecOrComponent = ComponentSpec | component.Component
type ComponentSpecs = Sequence[ComponentSpec]
type ComponentSpecsOrComponents = Sequence[ComponentSpecOrComponent]


class _PostProcess(Protocol):
    def __call__(self, component: component.Component, **kwargs: Any) -> Any: ...


type PostProcess = (
    _PostProcess | Callable[[component.Component], None] | partial[component.Component]
)
type PostProcesses = Sequence[PostProcess]

from gdsfactory.component import ComponentReference as Instance  # noqa: E402

type InstanceOrVInstance = component.ComponentReference | kf.VInstance
type ComponentOrPath = PathType | component.Component
type ComponentOrReference = component.Component | component.ComponentReference
type NameToFunctionDict = dict[str, ComponentFactory]


type ComponentSpecOrList = ComponentSpec | list[ComponentSpec]
type CellSpec = (
    str | ComponentFactory | dict[str, Any]  # PCell function, function name or dict
)
type CellAllAngleSpec = str | ComponentAllAngleFactory | dict[str, Any]
type ComponentSpecDict = dict[str, ComponentSpec]

type LayerTransitions = dict[
    LayerSpec | tuple[LayerEnum | Layer, LayerEnum | Layer], ComponentSpec
]


class TypedArray(np.ndarray[Any, np.dtype[Any]]):

    @classmethod
    def __get_validators__(
        cls,
    ) -> Generator[Callable[[Any, Any], npt.NDArray[np.float64]], Any, None]:
        yield cls.validate_type  # pragma: no cover

    @classmethod
    def validate_type(cls, val: Any, _info: Any) -> npt.NDArray[np.float64]:
        pass


class ArrayMeta(type):
    def __getitem__(cls, t: np.dtype[Any]) -> type[npt.NDArray[Any]]:
        return type("Array", (TypedArray,), {"inner_type": t})  # pragma: no cover


class Array(np.ndarray[Any, np.dtype[Any]], metaclass=ArrayMeta): ...


class CornerMode(IntEnum):
    diamond_limit = 0
    octagon_limit = 1
    square_limit = 2  # The GDSFactory default and klayout default
    acute_limit = 3
    no_limit = 4


__all__ = (
    "AngleInDegrees",
    "ComponentSpec",
    "Coordinate",
    "Coordinates",
    "CornerMode",
    "CrossSectionFactory",
    "CrossSectionSpec",
    "Delta",
    "Float2",
    "Float3",
    "Floats",
    "Instance",
    "Int2",
    "Int3",
    "Ints",
    "Layer",
    "LayerSpec",
    "LayerSpecs",
    "LayerTransitions",
    "Layers",
    "Number",
    "PathType",
    "PathTypes",
    "Pin",
    "Pins",
    "Port",
    "PortDict",
    "PortName",
    "PortNames",
    "PortType",
    "PortTypes",
    "Ports",
    "PortsDict",
    "PortsDictGeneric",
    "Position",
    "PostProcesses",
    "Radius",
    "RoutingStrategies",
    "SelectPorts",
    "Size",
    "Spacing",
    "Strs",
    "TPort",
    "WayPoints",
    "WidthTypes",
)
