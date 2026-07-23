from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any, Literal, TypeVar

import kfactory as kf
from kfactory.layer import LayerEnum
from pydantic import BaseModel, Field, field_validator, model_validator
from rich.console import Console
from rich.table import Table

from gdsfactory.technology.layer_views import LayerViews
from gdsfactory.typings import LayerSpec

if TYPE_CHECKING:
    from gdsfactory.component import Component

T = TypeVar("T", bound="AbstractLayer")


class AbstractLayer(BaseModel):

    sizings_xoffsets: Sequence[int] = (0,)
    sizings_yoffsets: Sequence[int] = (0,)
    sizings_modes: Sequence[int] = (2,)

    def _perform_operation(
        self, other: AbstractLayer, operation: Literal["and", "or", "xor", "not"]
    ) -> DerivedLayer:
        pass

    def __and__(self, other: AbstractLayer) -> DerivedLayer:
        """Represents boolean AND (&) operation between two layers.

        Args:
            other (AbstractLayer): Another Layer object to perform AND operation.

        Returns:
            A new DerivedLayer with the AND operation logged.
        """
        return self._perform_operation(other, "and")

    def __or__(self, other: AbstractLayer) -> DerivedLayer:
        """Represents boolean OR (|) operation between two layers.

        Args:
            other (AbstractLayer): Another Layer object to perform OR operation.

        Returns:
            A new DerivedLayer with the OR operation logged.
        """
        return self._perform_operation(other, "or")

    def __add__(self, other: AbstractLayer) -> DerivedLayer:
        """Represents boolean OR (+) operation between two derived layers.

        Args:
            other (AbstractLayer): Another Layer object to perform OR operation.

        Returns:
            A new DerivedLayer with the AND operation logged.
        """
        return self._perform_operation(other, "or")

    def __xor__(self, other: AbstractLayer) -> DerivedLayer:
        """Represents boolean XOR (^) operation between two derived layers.

        Args:
            other (AbstractLayer): Another Layer object to perform XOR operation.

        Returns:
            A new DerivedLayer with the XOR operation logged.
        """
        return self._perform_operation(other, "xor")

    def __sub__(self, other: AbstractLayer) -> DerivedLayer:
        """Represents boolean NOT (-) operation on a derived layer.

        Args:
            other (AbstractLayer): Another Layer object to perform NOT operation.

        Returns:
            A new DerivedLayer with the NOT operation logged.
        """
        return self._perform_operation(other, "not")

    def sized(
        self: T,
        xoffset: int | tuple[int, ...],
        yoffset: int | tuple[int, ...] | None = None,
        mode: int | tuple[int, ...] | None = None,
    ) -> T:
        """Accumulates a list of sizing operations for the layer by the provided offset (in dbu).

        Args:
            xoffset (int | tuple): number of dbu units to buffer by. Can be a tuple for sequential sizing operations.
            yoffset (int | tuple): number of dbu units to buffer by in the y-direction. If not specified, uses xfactor. Can be a tuple for sequential sizing operations.
            mode (int | tuple): mode of the sizing operation(s). Can be a tuple for sequential sizing operations.
        """
        xoffset_list: list[int]
        if isinstance(xoffset, int):
            xoffset_list = [xoffset]
        else:
            xoffset_list = list(xoffset)
        yoffset_list: list[int]
        if isinstance(yoffset, tuple):
            if len(yoffset) != len(xoffset_list):
                raise ValueError(
                    "If yoffset is provided as a tuple, length must be equal to xoffset!"
                )
            yoffset_list = list(yoffset)
        elif yoffset is None:
            yoffset_list = xoffset_list
        else:
            yoffset_list = [yoffset] * len(xoffset_list)

        mode_list: list[int]
        if isinstance(mode, tuple):
            if len(mode) != len(xoffset_list):
                raise ValueError(
                    "If mode is provided as a tuple, length must be equal to xoffset!"
                )
            mode_list = list(mode)
        elif mode is None:
            mode_list = [2] * len(xoffset_list)
        else:
            mode_list = [mode] * len(xoffset_list)

        sizings_xoffsets = list(self.sizings_xoffsets) + xoffset_list
        sizings_yoffsets = list(self.sizings_yoffsets) + yoffset_list
        sizings_modes = list(self.sizings_modes) + mode_list

        current_layer_attributes = self.__dict__.copy()
        current_layer_attributes["sizings_xoffsets"] = sizings_xoffsets
        current_layer_attributes["sizings_yoffsets"] = sizings_yoffsets
        current_layer_attributes["sizings_modes"] = sizings_modes
        return self.__class__(**current_layer_attributes)


class LogicalLayer(AbstractLayer):

    layer: LayerSpec

    def __eq__(self, other: object) -> bool:
        """Check if two LogicalLayer instances are equal.

        This method compares the 'layer' attribute of the two LogicalLayer instances.

        Args:
            other (LogicalLayer): The other LogicalLayer instance to compare with.

        Returns:
            bool: True if the 'layer' attributes are equal, False otherwise.

        Raises:
            NotImplementedError: If 'other' is not an instance of LogicalLayer.
        """
        if not isinstance(other, type(self)):
            raise NotImplementedError(f"{other} is not a {type(self)}")
        return self.layer == other.layer

    def __hash__(self) -> int:
        """Generates a hash value for a LogicalLayer instance.

        This method allows LogicalLayer instances to be used in hash-based data structures such as sets and dictionaries.

        Returns:
            int: The hash value of the layer attribute.
        """
        return hash(self.layer)

    def get_shapes(self, component: Component) -> kf.kdb.Region:
        """Return the shapes of the component argument corresponding to this layer.

        Arguments:
            component: Component from which to extract shapes on this layer.

        Returns:
            kf.kdb.Region: A region of polygons on this layer.
        """
        from gdsfactory.pdk import get_layer

        polygons_per_layer = component.get_polygons()
        layer_index = get_layer(self.layer)
        polygons = polygons_per_layer.get(layer_index, [])
        region = kf.kdb.Region(polygons)
        if not (
            all(v == 0 for v in self.sizings_xoffsets)
            and all(v == 0 for v in self.sizings_yoffsets)
        ):
            for xoffset, yoffset, mode in zip(
                self.sizings_xoffsets,
                self.sizings_yoffsets,
                self.sizings_modes,
                strict=False,
            ):
                region = region.sized(xoffset, yoffset, mode)
        return region

    def __repr__(self) -> str:
        """Print text representation."""
        return f"{self.layer}"

    __str__ = __repr__


class DerivedLayer(AbstractLayer):

    layer1: DerivedLayer | LogicalLayer
    layer2: DerivedLayer | LogicalLayer
    operation: Literal["and", "&", "or", "|", "xor", "^", "not", "-"]

    def __hash__(self) -> int:
        """Generates a hash value for a LogicalLayer instance.

        This method allows LogicalLayer instances to be used in hash-based data structures such as sets and dictionaries.

        Returns:
            int: The hash value of the layer attribute.
        """
        return hash((self.layer1.__hash__(), self.layer2.__hash__(), self.operation))

    def __eq__(self, other: object) -> bool:
        """Check if two DerivedLayer instances are equal."""
        if not isinstance(other, DerivedLayer):
            return False
        return (
            self.layer1 == other.layer1
            and self.layer2 == other.layer2
            and self.operation == other.operation
        )

    @property
    def keyword_to_symbol(self) -> dict[str, str]:
        pass

    @property
    def symbol_to_keyword(self) -> dict[str, str]:
        pass

    def get_symbol(self) -> str:
        pass

    def get_shapes(self, component: Component) -> kf.kdb.Region:
        """Return the shapes of the component argument corresponding to this layer.

        Arguments:
            component: Component from which to extract shapes on this layer.

        Returns:
            kf.kdb.Region: A region of polygons on this layer.
        """
        from gdsfactory.component import boolean_operations

        r1 = self.layer1.get_shapes(component)
        r2 = self.layer2.get_shapes(component)
        region = boolean_operations[self.operation](r1, r2)
        if not (
            all(v == 0 for v in self.sizings_xoffsets)
            and all(v == 0 for v in self.sizings_yoffsets)
        ):
            for xoffset, yoffset, mode in zip(
                self.sizings_xoffsets,
                self.sizings_yoffsets,
                self.sizings_modes,
                strict=False,
            ):
                region = region.sized(xoffset, yoffset, mode)
        return region

    def __repr__(self) -> str:
        """Print text representation."""
        return f"({self.layer1} {self.get_symbol()} {self.layer2})"

    __str__ = __repr__


type BroadLayer = LogicalLayer | DerivedLayer | int | str | tuple[int, int] | LayerEnum


class LayerLevel(BaseModel):

    name: str | None = None
    layer: BroadLayer
    derived_layer: LogicalLayer | None = None

    thickness: float
    thickness_tolerance: float | None = None
    width_tolerance: float | None = None
    zmin: float
    zmin_tolerance: float | None = None
    sidewall_angle: float = 0.0
    sidewall_angle_tolerance: float | None = None
    width_to_z: float = 0.0
    z_to_bias: tuple[list[float], list[float]] | None = None
    bias: tuple[float, float] | float | None = None

    mesh_order: int = 3
    material: str | None = None

    info: dict[str, Any] = Field(default_factory=dict)

    @field_validator("layer")
    @classmethod
    def check_layer(cls, layer: BroadLayer) -> LogicalLayer | DerivedLayer:
        pass

    @model_validator(mode="after")
    def check_derived_layer(self) -> LayerLevel:
        pass

    @property
    def bounds(self) -> tuple[float, float]:
        pass


class LayerStack(BaseModel):

    layers: dict[str, LayerLevel] = Field(
        default_factory=dict,
        description="dict of layer_levels",
    )

    def model_copy(
        self, *, update: Mapping[str, Any] | None = None, deep: bool = False
    ) -> LayerStack:
        """Returns a copy of the LayerStack."""
        return super().model_copy(update=update, deep=True)

    def __init__(self, **data: Any) -> None:
        """Add LayerLevels automatically for subclassed LayerStacks."""
        super().__init__(**data)

        for field in self.model_dump():
            val = getattr(self, field)
            if isinstance(val, LayerLevel):
                self.layers[field] = val

    def pprint(self) -> None:
        pass

    def get_layer_to_thickness(self) -> dict[BroadLayer, float]:
        pass

    def get_component_with_derived_layers(
        self, component: Component, **kwargs: Any
    ) -> Component:
        """Returns component with derived layers."""
        return get_component_with_derived_layers(
            component=component, layer_stack=self, **kwargs
        )

    def get_layer_to_zmin(self) -> dict[BroadLayer, float]:
        pass

    def get_layer_to_material(self) -> dict[BroadLayer, str | None]:
        pass

    def get_layer_to_sidewall_angle(self) -> dict[BroadLayer, float]:
        pass

    def get_layer_to_info(self) -> dict[BroadLayer, dict[str, Any]]:
        pass

    def get_layer_to_layername(self) -> dict[BroadLayer, list[str]]:
        pass

    def get_layer_to_mesh_order(
        self,
    ) -> dict[BroadLayer, int]:
        pass

    def to_dict(self) -> dict[str, dict[str, Any]]:
        return {level_name: dict(level) for level_name, level in self.layers.items()}

    def __getitem__(self, key: str) -> LayerLevel:
        """Access layer stack elements."""
        if key not in self.layers:
            layers = list(self.layers.keys())
            raise KeyError(f"{key!r} not in {layers}")

        return self.layers[key]

    def get_klayout_3d_script(
        self,
        layer_views: LayerViews | None = None,
        dbu: float | None = 0.001,
    ) -> str:
        pass

    def filtered(self, layers: list[str]) -> LayerStack:
        pass

    def z_offset(self, dz: float) -> LayerStack:
        pass

    def invert_zaxis(self) -> LayerStack:
        pass


def get_component_with_derived_layers(
    component: Component, layer_stack: LayerStack
) -> Component:
    """Returns a component with derived layers.

    Args:
        component: Component to get derived layers for.
        layer_stack: Layer stack to get derived layers from.
    """
    from gdsfactory.component import Component
    from gdsfactory.pdk import get_layer

    component_derived = Component()

    for level in layer_stack.layers.values():
        if level.derived_layer is None:
            if isinstance(level.layer, LogicalLayer):
                derived_layer_index = get_layer(level.layer.layer)
            else:
                raise ValueError(
                    "If derived_layer is not provided, the LayerLevel layer must be a LogicalLayer"
                )
        else:
            derived_layer_index = get_layer(level.derived_layer.layer)
        if isinstance(level.layer, AbstractLayer):
            shapes = level.layer.get_shapes(component=component)
            component_derived.shapes(derived_layer_index).insert(shapes)

    component_derived.add_ports(component.ports)
    return component_derived
