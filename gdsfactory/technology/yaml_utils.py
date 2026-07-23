from collections.abc import Iterable
from typing import Any

import yaml
import yaml.representer as yaml_representer
from pydantic_extra_types.color import Color

from gdsfactory.technology.color_utils import ensure_six_digit_hex_color


class TechnologyDumper(yaml.SafeDumper):
    pass


def add_color_yaml_representer(prefer_named_color: bool = True) -> None:
    """Add a custom YAML presenter for Color objects."""

    def _color_presenter(
        dumper: yaml_representer.SafeRepresenter, data: Color
    ) -> yaml.Node:
        pass

    TechnologyDumper.add_representer(Color, _color_presenter)


def add_tuple_yaml_representer() -> None:
    """Add a custom YAML presenter for tuple objects."""

    def _tuple_presenter(
        dumper: yaml_representer.SafeRepresenter, data: Iterable[Any]
    ) -> yaml.Node:
        pass

    TechnologyDumper.add_representer(tuple, _tuple_presenter)


def add_multiline_str_yaml_representer() -> None:
    """Add a custom YAML presenter for multiline strings."""

    def _str_presenter(
        dumper: yaml_representer.SafeRepresenter, data: str
    ) -> yaml.Node:
        pass

    TechnologyDumper.add_representer(str, _str_presenter)


add_color_yaml_representer()
add_tuple_yaml_representer()
add_multiline_str_yaml_representer()
