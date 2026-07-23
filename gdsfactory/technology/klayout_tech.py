
import pathlib
import xml.etree.ElementTree as ET
from collections.abc import Sequence
from typing import Any

import aenum
import klayout.db as db
from pydantic import BaseModel, ConfigDict, field_validator

from gdsfactory.technology import LayerStack, LayerViews
from gdsfactory.technology.xml_utils import make_pretty_xml
from gdsfactory.typings import ConnectivitySpec, PathType

prefix_d25 = """<?xml version="1.0" encoding="utf-8"?>
<klayout-macro>
 <description/>
 <version/>
 <category>d25</category>
 <prolog/>
 <epilog/>
 <doc/>
 <autorun>false</autorun>
 <autorun-early>false</autorun-early>
 <priority>0</priority>
 <shortcut/>
 <show-in-menu>true</show-in-menu>
 <group-name>d25_scripts</group-name>
 <menu-path>tools_menu.d25.end</menu-path>
 <interpreter>dsl</interpreter>
 <dsl-interpreter-name>d25-dsl-xml</dsl-interpreter-name>
 <text>

"""
suffix_d25 = """
</text>
</klayout-macro>
"""


class KLayoutTechnology(BaseModel):

    name: str
    layer_map: dict[str, tuple[int, int]]
    layer_views: LayerViews | None = None
    layer_stack: LayerStack | None = None
    connectivity: Sequence[ConnectivitySpec] | None = None

    @field_validator("layer_map", mode="before")
    @classmethod
    def check_layer_map(cls, layer_map: Any) -> Any:
        pass

    def write_tech(
        self,
        tech_dir: PathType,
        lyp_filename: str = "layers.lyp",
        lyt_filename: str = "tech.lyt",
        d25_filename: str | None = None,
        mebes_config: dict[str, Any] | None = None,
    ) -> None:
        pass

    def _define_connections(self, root: ET.Element) -> None:
        pass

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
