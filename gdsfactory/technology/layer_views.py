
from __future__ import annotations

import builtins
import pathlib
import re
import warnings
import xml.etree.ElementTree as ET
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

import numpy as np
import yaml
from kfactory import logger
from kfactory.layer import LayerEnum
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.color import ColorType
from pydantic_extra_types.color import Color

from gdsfactory.name import clean_name
from gdsfactory.technology.color_utils import ensure_six_digit_hex_color
from gdsfactory.technology.xml_utils import make_pretty_xml
from gdsfactory.technology.yaml_utils import TechnologyDumper

if TYPE_CHECKING:
    from gdsfactory.component import Component

PathLike = pathlib.Path | str
Layer = tuple[int, int]
type IncEx = (
    set[int] | set[str] | Mapping[int, "IncEx | bool"] | Mapping[str, "IncEx | bool"]
)

_klayout_line_styles = {
    "solid": "",
    "dotted": "*.",
    "dashed": "**..**",
    "dash-dotted": "***..**..***",
    "short dashed": "*..*",
    "short dash-dotted": "**.*.*",
    "long dashed": "*****..*****",
    "dash-double-dotted": "***..*.*..**",
}
_klayout_dither_patterns = {
    "solid": "*",
    "hollow": ".",
    "dotted": "*.\n.*",
    "coarsely dotted": "*...\n....\n..*.\n....",
    "left-hatched": "*...\n.*..\n..*.\n...*",
    "lightly left-hatched": "*.......\n"
    ".*......\n"
    "..*.....\n"
    "...*....\n"
    "....*...\n"
    ".....*..\n"
    "......*.\n"
    ".......*",
    "strongly left-hatched dense": "**..\n.**.\n..**\n*..*",
    "strongly left-hatched sparse": "**......\n"
    ".**.....\n"
    "..**....\n"
    "...**...\n"
    "....**..\n"
    ".....**.\n"
    "......**\n"
    "*......*",
    "right-hatched": "*...\n...*\n..*.\n.*..",
    "lightly right-hatched": "*.......\n"
    ".......*\n"
    "......*.\n"
    ".....*..\n"
    "....*...\n"
    "...*....\n"
    "..*.....\n"
    ".*......",
    "strongly right-hatched dense": "**..\n*..*\n..**\n.**.",
    "strongly right-hatched sparse": "**......\n"
    "*......*\n"
    "......**\n"
    ".....**.\n"
    "....**..\n"
    "...**...\n"
    "..**....\n"
    ".**.....",
    "cross-hatched": "*...\n.*.*\n..*.\n.*.*",
    "lightly cross-hatched": "*.......\n"
    ".*.....*\n"
    "..*...*.\n"
    "...*.*..\n"
    "....*...\n"
    "...*.*..\n"
    "..*...*.\n"
    ".*.....*",
    "checkerboard 2px": "**..\n**..\n..**\n..**",
    "strongly cross-hatched sparse": "**......\n"
    "***....*\n"
    "..**..**\n"
    "...****.\n"
    "....**..\n"
    "...****.\n"
    "..**..**\n"
    "***....*",
    "heavy checkerboard": "****....\n"
    "****....\n"
    "****....\n"
    "****....\n"
    "....****\n"
    "....****\n"
    "....****\n"
    "....****",
    "hollow bubbles": ".*...*..\n"
    "*.*.....\n"
    ".*...*..\n"
    "....*.*.\n"
    ".*...*..\n"
    "*.*.....\n"
    ".*...*..\n"
    "....*.*.",
    "solid bubbles": ".*...*..\n"
    "***.....\n"
    ".*...*..\n"
    "....***.\n"
    ".*...*..\n"
    "***.....\n"
    ".*...*..\n"
    "....***.",
    "pyramids": ".*......\n"
    "*.*.....\n"
    "****...*\n"
    "........\n"
    "....*...\n"
    "...*.*..\n"
    "..*****.\n"
    "........",
    "turned pyramids": "****...*\n"
    "*.*.....\n"
    ".*......\n"
    "........\n"
    "..*****.\n"
    "...*.*..\n"
    "....*...\n"
    "........",
    "plus": "..*...*.\n"
    "..*.....\n"
    "*****...\n"
    "..*.....\n"
    "..*...*.\n"
    "......*.\n"
    "*...****\n"
    "......*.",
    "minus": "........\n"
    "........\n"
    "*****...\n"
    "........\n"
    "........\n"
    "........\n"
    "*...****\n"
    "........",
    "22.5 degree down": "*......*\n"
    ".**.....\n"
    "...**...\n"
    ".....**.\n"
    "*......*\n"
    ".**.....\n"
    "...**...\n"
    ".....**.",
    "22.5 degree up": "*......*\n"
    ".....**.\n"
    "...**...\n"
    ".**.....\n"
    "*......*\n"
    ".....**.\n"
    "...**...\n"
    ".**.....",
    "67.5 degree down": "*...*...\n"
    ".*...*..\n"
    ".*...*..\n"
    "..*...*.\n"
    "..*...*.\n"
    "...*...*\n"
    "...*...*\n"
    "*...*...",
    "67.5 degree up": "...*...*\n"
    "..*...*.\n"
    "..*...*.\n"
    ".*...*..\n"
    ".*...*..\n"
    "*...*...\n"
    "*...*...\n"
    "...*...*",
    "22.5 degree cross hatched": "*......*\n"
    ".**..**.\n"
    "...**...\n"
    ".**..**.\n"
    "*......*\n"
    ".**..**.\n"
    "...**...\n"
    ".**..**.",
    "zig zag": "..*...*.\n"
    ".*.*.*.*\n"
    "*...*...\n"
    "........\n"
    "..*...*.\n"
    ".*.*.*.*\n"
    "*...*...\n"
    "........",
    "sine": "..***...\n"
    ".*...*..\n"
    "*.....**\n"
    "........\n"
    "..***...\n"
    ".*...*..\n"
    "*.....**\n"
    "........",
    "heavy unordered": "****.*.*\n"
    "**.****.\n"
    "*.**.***\n"
    "*****.*.\n"
    ".**.****\n"
    "**.***.*\n"
    ".****.**\n"
    "*.*.****",
    "light unordered": "....*.*.\n"
    "..*....*\n"
    ".*..*...\n"
    ".....*.*\n"
    "*..*....\n"
    "..*...*.\n"
    "*....*..\n"
    ".*.*....",
    "vertical dense": "*.\n*.\n",
    "vertical": ".*..\n.*..\n.*..\n.*..\n",
    "vertical thick": ".**.\n.**.\n.**.\n.**.\n",
    "vertical sparse": "...*....\n...*....\n...*....\n...*....\n",
    "vertical sparse, thick": "...**...\n...**...\n...**...\n...**...\n",
    "horizontal dense": "**\n..\n",
    "horizontal": "....\n****\n....\n....\n",
    "horizontal thick": "....\n****\n****\n....\n",
    "horizontal sparse": "........\n"
    "........\n"
    "........\n"
    "********\n"
    "........\n"
    "........\n"
    "........\n"
    "........\n",
    "horizontal sparse, thick": "........\n"
    "........\n"
    "........\n"
    "********\n"
    "********\n"
    "........\n"
    "........\n"
    "........\n",
    "grid dense": "**\n*.\n",
    "grid": ".*..\n****\n.*..\n.*..\n",
    "grid thick": ".**.\n****\n****\n.**.\n",
    "grid sparse": "...*....\n"
    "...*....\n"
    "...*....\n"
    "********\n"
    "...*....\n"
    "...*....\n"
    "...*....\n"
    "...*....\n",
    "grid sparse, thick": "...**...\n"
    "...**...\n"
    "...**...\n"
    "********\n"
    "********\n"
    "...**...\n"
    "...**...\n"
    "...**...\n",
}


class HatchPattern(BaseModel):

    name: str | None = Field(default=None, exclude=True)
    order: int | None = None
    custom_pattern: str | None = None

    @field_validator("custom_pattern")
    @classmethod
    def check_pattern_klayout(cls, pattern: str | None) -> str | None:
        pass

    def to_klayout_xml(self) -> ET.Element:
        pass


class LineStyle(BaseModel):

    name: str | None = Field(default=None, exclude=True)
    order: int | None = None
    custom_style: str | None = None

    @field_validator("custom_style")
    @classmethod
    def check_pattern(cls, pattern: str | None) -> str | None:
        pass

    def to_klayout_xml(self) -> ET.Element:
        pass


class LayerView(BaseModel):

    name: str | None = Field(default=None, exclude=True)
    info: str | None = Field(default=None)
    layer: Layer | None = None
    layer_in_name: bool = False
    frame_color: Color | None = None
    fill_color: Color | None = None
    frame_brightness: int = 0
    fill_brightness: int = 0
    hatch_pattern: str | HatchPattern | None = None
    line_style: str | LineStyle | None = None
    valid: bool = True
    visible: bool = True
    transparent: bool = False
    width: int | None = None
    marked: bool = False
    xfill: bool = False
    animation: int = 0
    group_members: builtins.dict[str, LayerView] = Field(default_factory=builtins.dict)

    def __init__(
        self,
        gds_layer: int | None = None,
        gds_datatype: int | None = None,
        color: ColorType | None = None,
        brightness: int | None = None,
        **data: Any,
    ) -> None:
        """Initialize LayerView object."""
        if (gds_layer is not None) and (gds_datatype is not None):
            if "layer" in data and data["layer"] is not None:
                raise KeyError(
                    "Specify either 'layer' or both 'gds_layer' and 'gds_datatype'."
                )
            data["layer"] = (gds_layer, gds_datatype)

        if color is not None:
            if "fill_color" in data or "frame_color" in data:
                raise KeyError(
                    "Specify either a single 'color' or both 'frame_color' and 'fill_color'."
                )
            data["fill_color"] = data["frame_color"] = color
        if brightness is not None:
            if "fill_brightness" in data or "frame_brightness" in data:
                raise KeyError(
                    "Specify either a single 'brightness' or both 'frame_brightness' and 'fill_brightness'."
                )
            data["fill_brightness"] = data["frame_brightness"] = brightness

        super().__init__(**data)

    def dict(
        self,
        *,
        include: IncEx | None = None,
        exclude: IncEx | None = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        simplify: bool = True,
    ) -> dict[str, Any]:
        pass

    def __str__(self) -> str:
        """Returns a formatted view of properties and their values."""
        return "LayerView:\n\t" + "\n\t".join(
            [f"{k}: {v}" for k, v in self.model_dump().items()]
        )

    def __repr__(self) -> str:
        """Returns a formatted view of properties and their values."""
        return self.__str__()

    def get_alpha(self) -> float:
        pass

    def get_color_dict(self) -> builtins.dict[str, str | None]:
        pass

    def _build_klayout_xml_element(
        self,
        tag: str,
        name: str,
        custom_hatch_patterns: builtins.dict[str, HatchPattern],
        custom_line_styles: builtins.dict[str, LineStyle],
    ) -> ET.Element:
        pass

    def to_klayout_xml(
        self,
        custom_hatch_patterns: builtins.dict[str, HatchPattern],
        custom_line_styles: builtins.dict[str, LineStyle],
    ) -> ET.Element:
        pass

    @staticmethod
    def _process_name(
        name: str, layer_pattern: str | re.Pattern[str], source: str | None = None
    ) -> tuple[str | None, bool | None]:
        """Strip layer info from name if it exists.

        Args:
            name: XML-formatted name entry.
            layer_pattern: Regex pattern to match layers with.
            source: Source field from XML that may contain layer name.
        """
        if not name and source:
            match = re.search(layer_pattern, source)
            if match:
                name = source[: match.start()].strip()
                if name:
                    return clean_name(name, remove_dots=True), False
            return None, None

        if not name:
            return None, None

        layer_in_name = False
        match = re.search(layer_pattern, name)
        if match:
            name = (name[: match.start()] + name[match.end() :]).strip()
            layer_in_name = True
        return clean_name(name, remove_dots=True), layer_in_name

    @staticmethod
    def _process_layer(
        layer: str, layer_pattern: str | re.Pattern[str]
    ) -> Layer | None:
        """Convert .lyp XML layer entry to a Layer.

        Args:
            layer: XML-formatted layer entry.
            layer_pattern: Regex pattern to match layers with.
        """
        match = re.search(layer_pattern, layer)
        if not match:
            raise OSError(f"Could not read layer {layer}!")
        v = match.group().split("/")
        return None if "*" in v else (int(v[0]), int(v[1]))

    @classmethod
    def from_xml_element(
        cls, element: ET.Element, layer_pattern: str | re.Pattern[str]
    ) -> LayerView | None:
        """Read properties from .lyp XML and generate LayerViews from them.

        Args:
            element: XML Element to iterate over.
            layer_pattern: Regex pattern to match layers with.
        """
        element_name = element.find("name")
        element_source = element.find("source")
        source_text = element_source.text if element_source is not None else None

        name, layer_in_name = cls._process_name(
            element_name.text or "" if element_name is not None else "",
            layer_pattern,
            source_text,
        )
        if name is None:
            return None

        hatch_pattern = element.find("dither-pattern").text  # type: ignore[union-attr]
        if hatch_pattern and re.match(r"I\d+", hatch_pattern):
            hatch_pattern = list(_klayout_dither_patterns.keys())[
                int(hatch_pattern[1:])
            ]

        line_style = element.find("line-style")
        if (
            line_style is not None
            and line_style.text is not None
            and re.match(r"I\d+", line_style.text)
        ):
            line_style = list(_klayout_line_styles.keys())[int(line_style.text[1:])]  # type: ignore[assignment]

        lv = LayerView(
            name=name,
            layer=cls._process_layer(element.find("source").text, layer_pattern),  # type: ignore[union-attr,arg-type]
            fill_color=getattr(element.find("fill-color"), "text", None),
            frame_color=getattr(element.find("frame-color"), "text", None),
            fill_brightness=element.find("fill-brightness").text or 0,  # type: ignore[union-attr]
            frame_brightness=element.find("frame-brightness").text or 0,  # type: ignore[union-attr]
            hatch_pattern=hatch_pattern or None,
            line_style=line_style
            if line_style is not None and len(line_style) > 0
            else None,
            valid=getattr(element.find("valid"), "text", True),
            visible=getattr(element.find("visible"), "text", True),
            transparent=getattr(element.find("transparent"), "text", False),
            width=getattr(element.find("width"), "text", None),
            marked=getattr(element.find("marked"), "text", False),
            xfill=getattr(element.find("xfill"), "text", False),
            animation=getattr(element.find("animation"), "text", False),
            layer_in_name=layer_in_name,
        )

        group_members: builtins.dict[str, LayerView] = {}
        for member in element.iterfind("group-members"):
            member_lv = cls.from_xml_element(member, layer_pattern)
            if member_lv and member_lv.name is not None:
                group_members[member_lv.name] = member_lv

        if group_members != {}:
            lv.group_members = group_members

        return lv


LayerView.model_rebuild()


class LayerViews(BaseModel):

    layer_views: dict[str, LayerView] = Field(default_factory=dict)
    custom_dither_patterns: dict[str, HatchPattern] = Field(default_factory=dict)
    custom_line_styles: dict[str, LineStyle] = Field(default_factory=dict)
    layers: type[LayerEnum] | None = None

    model_config = ConfigDict(extra="forbid", frozen=True, revalidate_instances="never")

    def __init__(
        self,
        filepath: PathLike | None = None,
        layers: type[LayerEnum] | None = None,
        **data: Any,
    ) -> None:
        """Initialize LayerViews object.

        Args:
            filepath: can be YAML or LYP.
            layers: Optional layermap.
            data: Additional data to add to the LayerViews object.
        """
        if filepath is not None:
            filepath = pathlib.Path(filepath)
            if filepath.suffix == ".lyp":
                lvs = LayerViews.from_lyp(filepath=filepath)
                logger.debug(
                    f"Importing LayerViews from KLayout layer properties file: {str(filepath)!r}."
                )
            elif filepath.suffix in {".yaml", ".yml"}:
                lvs = LayerViews.from_yaml(layer_file=filepath)
                logger.debug(f"Importing LayerViews from YAML file: {str(filepath)!r}.")
            else:
                raise ValueError(f"Unable to load LayerViews from {str(filepath)!r}.")

            data["layer_views"] = lvs.layer_views
            data["custom_line_styles"] = lvs.custom_line_styles
            data["custom_dither_patterns"] = lvs.custom_dither_patterns
        layer_names: builtins.dict[str, LayerEnum] | None = None
        if layers:
            layer_names = {layer.name: layer for layer in layers if layer is not None}  # type: ignore[attr-defined]
        else:
            layer_names = None

        cls = type(self)
        construct_data: builtins.dict[str, Any] = {
            "layer_views": data.get("layer_views", {}),
            "custom_dither_patterns": data.get("custom_dither_patterns", {}),
            "custom_line_styles": data.get("custom_line_styles", {}),
            "layers": layers,
        }
        for field_name, field_info in cls.model_fields.items():
            if field_name not in construct_data:
                construct_data[field_name] = data.get(field_name, field_info.default)
        constructed = cls.model_construct(**construct_data)
        object.__setattr__(self, "__dict__", constructed.__dict__)
        object.__setattr__(
            self, "__pydantic_fields_set__", constructed.__pydantic_fields_set__
        )

        for name in self.model_dump():
            lv = getattr(self, name)
            if isinstance(lv, LayerView):
                if type(lv) is not LayerView and not lv.group_members:
                    for field_name in type(lv).model_fields:
                        field_val = getattr(lv, field_name)
                        if isinstance(field_val, LayerView):
                            lv.group_members[field_name] = field_val
                if (
                    layers is not None
                    and layer_names is not None
                    and name in layer_names
                ):
                    lv_dict = lv.dict(exclude={"layer", "name"})
                    lv = LayerView(layer=layer_names[name], name=name, **lv_dict)
                self.add_layer_view(name=name, layer_view=lv)

    def add_layer_view(
        self, name: str, layer_view: LayerView | None = None, **kwargs: Any
    ) -> None:
        pass

    def get_layer_views(self, exclude_groups: bool = False) -> dict[str, LayerView]:
        """Return all LayerViews.

        Args:
            exclude_groups: Whether to exclude LayerViews that contain other LayerViews.
        """
        layers: dict[str, LayerView] = {}
        for name, view in self.layer_views.items():
            if view.group_members and not exclude_groups:
                layers.update(view.group_members.items())
            layers[name] = view
        return layers

    def get_layer_view_groups(self) -> dict[str, LayerView]:
        pass

    def __str__(self) -> str:
        """Prints the number of LayerView objects in the LayerViews object."""
        lvs = self.get_layer_views()
        groups = self.get_layer_view_groups()
        return (
            f"LayerViews: {len(lvs)} layers ({len(groups)} groups)\n"
            f"\tCustomDitherPatterns: {list(self.custom_dither_patterns.keys())}\n"
            f"\tCustomLineStyles: {list(self.custom_line_styles.keys())}\n"
        )

    def get(self, name: str) -> LayerView:
        """Returns Layer from name.

        Args:
            name: Name of layer.
        """
        if name not in self.layer_views:
            raise ValueError(f"Layer {name!r} not in {list(self.layer_views.keys())}")
        return self.layer_views[name]

    def __getitem__(self, val: str) -> LayerView:
        """Allows accessing to the layer names like ls['gold2'].

        Args:
            val: Layer name to access within the LayerViews.

        Returns:
            self.layers[val]: LayerView in the LayerViews.

        """
        try:
            return self.get_layer_views()[val]
        except Exception as error:
            raise KeyError(
                f"LayerView {val!r} not in LayerViews {list(self.layer_views.keys())}"
            ) from error

    def get_from_tuple(self, layer_tuple: tuple[int, int]) -> LayerView:
        """Returns LayerView from layer tuple.

        Args:
            layer_tuple: Tuple of (gds_layer, gds_datatype).

        Returns:
            LayerView.
        """
        tuple_to_name = {v.layer: k for k, v in self.get_layer_views().items()}
        if layer_tuple not in tuple_to_name:
            raise ValueError(
                f"LayerView {layer_tuple} not in {list(tuple_to_name.keys())}"
            )

        name = tuple_to_name[layer_tuple]
        return self.get_layer_views()[name]

    def get_layer_tuples(self) -> set[Layer]:
        pass

    def clear(self) -> None:
        """Deletes all layers in the LayerViews."""
        self.layer_views = {}

    def preview_layerset(
        self, size: float = 100.0, spacing: float = 100.0
    ) -> Component:
        pass

    def to_lyp(
        self, filepath: str | pathlib.Path, overwrite: bool = True
    ) -> pathlib.Path:
        pass

    @staticmethod
    def from_lyp(
        filepath: str | pathlib.Path,
        layer_pattern: str | re.Pattern[str] | None = None,
    ) -> LayerViews:
        r"""Write all layer properties to a KLayout .lyp file.

        Args:
            filepath: to write the .lyp file to (appends .lyp extension if not present).
            layer_pattern: Regex pattern to match layers with. Defaults to r'(\d+|\*)/(\d+|\*)'.
        """
        layer_pattern = re.compile(layer_pattern or r"(\d+|\*)/(\d+|\*)")

        filepath = pathlib.Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(
                f"File {str(filepath)!r} does not exist, cannot read."
            )

        tree = ET.parse(filepath)
        root = tree.getroot()
        if root.tag != "layer-properties":
            raise OSError("Layer properties file incorrectly formatted, cannot read.")

        dither_patterns: dict[str, HatchPattern] = {}
        pattern_counter = 0
        for dither_block in root.iter("custom-dither-pattern"):
            name_element = dither_block.find("name")
            name = name_element.text if name_element is not None else None
            order_element = dither_block.find("order")
            order = order_element.text if order_element is not None else None

            if order is None:
                continue

            if not name:
                name = f"custom_pattern_{pattern_counter}"
                pattern_counter += 1

            assert name is not None  # Type assertion for mypy
            pattern = "\n".join(
                [line.text for line in dither_block.find("pattern").iter()]  # type: ignore[misc,union-attr]
            )

            if name in dither_patterns:
                warnings.warn(
                    f"Dither pattern named {name!r} already exists. Keeping only the first defined.",
                    stacklevel=3,
                )
                continue

            dither_patterns[name] = HatchPattern(
                name=name,
                order=int(order),
                custom_pattern=pattern.lstrip(),
            )
        line_styles: dict[str, LineStyle] = {}
        style_counter = 0
        for line_block in root.iter("custom-line-style"):
            name_element = line_block.find("name")
            name = name_element.text if name_element is not None else None
            order_element = line_block.find("order")
            order = order_element.text if order_element is not None else None

            if order is None:
                continue

            if not name:
                name = f"custom_style_{style_counter}"
                style_counter += 1

            assert name is not None  # Type assertion for mypy
            if name in line_styles:
                warnings.warn(
                    f"Line style named {name!r} already exists. Keeping only the first defined.",
                    stacklevel=3,
                )
                continue

            pattern_element = line_block.find("pattern")
            line_pattern = pattern_element.text if pattern_element is not None else None

            line_styles[name] = LineStyle(
                name=name,
                order=int(order),
                custom_style=line_pattern,
            )

        layer_views = {}
        for properties_element in root.iter("properties"):
            lv = LayerView.from_xml_element(
                properties_element, layer_pattern=layer_pattern
            )
            if lv:
                hp = lv.hatch_pattern
                if isinstance(hp, str) and re.match(r"C\d+", hp):
                    lv.hatch_pattern = list(dither_patterns.keys())[int(hp[1:])]
                layer_views[lv.name] = lv

        return LayerViews.model_construct(
            layer_views=layer_views,
            custom_dither_patterns=dither_patterns,
            custom_line_styles=line_styles,
            layers=None,
        )

    def to_yaml(self, layer_file: str | pathlib.Path) -> None:
        pass

    @staticmethod
    def from_yaml(layer_file: str | pathlib.Path) -> LayerViews:
        """Import layer properties from two yaml files.

        Args:
            layer_file: Name of the file to read LayerViews, CustomDitherPatterns, and CustomLineStyles from.
        """
        layer_file = pathlib.Path(layer_file)

        properties = yaml.safe_load(layer_file.read_text())
        lvs = {}
        for name, lv in properties["LayerViews"].items():
            if "group_members" in lv:
                lv["group_members"] = {
                    member_name: LayerView(name=member_name, **member_view)
                    for member_name, member_view in lv["group_members"].items()
                }
            lvs[name] = LayerView(name=name, **lv)

        custom_dither_patterns = (
            {
                name: HatchPattern(name=name, **dp)
                for name, dp in properties["CustomDitherPatterns"].items()
            }
            if "CustomDitherPatterns" in properties
            else {}
        )

        custom_line_styles = (
            {
                name: LineStyle(name=name, **ls)
                for name, ls in properties["CustomLineStyles"].items()
            }
            if "CustomLineStyles" in properties
            else {}
        )

        return LayerViews.model_construct(
            layer_views=lvs,
            custom_dither_patterns=custom_dither_patterns,
            custom_line_styles=custom_line_styles,
            layers=None,
        )


def test_load_lyp() -> None:
    pass
