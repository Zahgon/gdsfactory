
from __future__ import annotations

import pathlib
import warnings
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, Sequence
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Self,
    TypeAlias,
    cast,
    overload,
    override,
)

import kfactory as kf
import klayout.lay as lay
import networkx as nx
import numpy as np
import numpy.typing as npt
import yaml
from graphviz import Digraph
from kfactory import (
    DInstance,
    DPort,
    DPorts,
    VInstance,
    cell,
    kdb,
    save_layout_options,
)
from kfactory.exceptions import LockedError
from kfactory.kcell import BaseKCell, BasePin, ProtoKCell  # type: ignore[attr-defined]
from kfactory.port import ProtoPort
from kfactory.utils.fill import fill_tiled
from kfactory.utils.violations import (
    fix_spacing_tiled,
    fix_width_minkowski_tiled,
)
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pydantic import Field
from trimesh.scene.scene import Scene

from gdsfactory.config import CONF, GDSDIR_TEMP
from gdsfactory.serialization import DEFAULT_SERIALIZATION_MAX_DIGITS, clean_value_json
from gdsfactory.utils import to_kdb_dpoints


def _fix_pin_metadata(cell: kf.kcell.ProtoTKCell[Any]) -> None:
    """Rewrite pin metadata so port indices are strings, not ints.

    kfactory 2.5.1 stores pin port indices as ints in set_meta_data but
    deserializes the ports dict with string keys in get_meta_data, causing
    KeyError on GDS read. Converting indices to strings at write time avoids
    the mismatch.
    """
    pin_entries: dict[str, Any] = {}
    for meta in cell.each_meta_info():
        if meta.name.startswith("kfactory:pins"):
            pin_entries[meta.name] = meta.value
    for name, value in pin_entries.items():
        cell.remove_meta_info(name)
        value["ports"] = [str(p) for p in value["ports"]]
        cell.add_meta_info(kdb.LayoutMetaInfo(name, value, None, True))


class AddPortError(ValueError):
    pass


if TYPE_CHECKING:
    from gdsfactory.cross_section import CrossSection, CrossSectionSpec
    from gdsfactory.get_netlist import (
        ComponentNamer,
        ErrorBehavior,
        InstanceNamer,
        NetlistNamer,
        PortMatcher,
    )
    from gdsfactory.technology.layer_stack import LayerStack
    from gdsfactory.technology.layer_views import LayerViews
    from gdsfactory.typings import (
        AngleInDegrees,
        AnyComponent,
        ComponentSpec,
        Coordinates,
        CornerMode,
        Layer,
        LayerSpec,
        LayerSpecs,
        PathType,
        PixelBufferOptions,
        Port,
        Position,
    )

cell_without_validator = cell

type _PolygonPoints = "npt.NDArray[np.floating[Any]] | kdb.DPolygon | kdb.Polygon | kdb.DSimplePolygon | kdb.Region | Coordinates"


def ensure_tuple_of_tuples(points: Any) -> tuple[tuple[float, float], ...]:
    if isinstance(points, np.ndarray):
        points = tuple(map(tuple, points.tolist()))
    elif isinstance(points, list):
        if len(points) > 0 and isinstance(points[0], np.ndarray | list):
            points = tuple(tuple(point) for point in points)
    return cast("tuple[tuple[float, float], ...]", points)


def points_to_polygon(
    points: _PolygonPoints,
) -> kdb.Polygon | kdb.DPolygon | kdb.DSimplePolygon | kdb.Region:
    if isinstance(points, kdb.Polygon | kdb.DPolygon | kdb.DSimplePolygon | kdb.Region):
        return points
    points = ensure_tuple_of_tuples(points)
    return kdb.DPolygon(to_kdb_dpoints(points))


def size(region: kdb.Region, offset: float, dbu: float = 1e3) -> kdb.Region:
    return region.dup().size(int(offset * dbu))


def boolean_or(region1: kdb.Region, region2: kdb.Region) -> kdb.Region:
    pass


def boolean_not(region1: kdb.Region, region2: kdb.Region) -> kdb.Region:
    pass


def boolean_xor(region1: kdb.Region, region2: kdb.Region) -> kdb.Region:
    pass


def boolean_and(region1: kdb.Region, region2: kdb.Region) -> kdb.Region:
    pass


boolean_operations = {
    "or": boolean_or,
    "|": boolean_or,
    "not": boolean_not,
    "-": boolean_not,
    "^": boolean_xor,
    "xor": boolean_xor,
    "&": boolean_and,
    "and": boolean_and,
    "A-B": boolean_not,
}


def copy(region: kdb.Region) -> kdb.Region:
    return region.dup()


ComponentReference: TypeAlias = DInstance  # noqa: UP040


class ComponentBase(ProtoKCell[float, BaseKCell], ABC):

    @property
    def layers(self) -> list[Layer]:
        return [
            (info.layer, info.datatype)
            for info in self.kcl.layout.layer_infos()
            if not self.bbox(self.kcl.layout.layer(info)).empty()
        ]

    @abstractmethod
    def add_polygon(
        self, points: _PolygonPoints, layer: LayerSpec
    ) -> kdb.Shape | None: ...

    def bbox_np(self) -> npt.NDArray[np.float64]:
        """Returns the bounding box of the Component as a numpy array."""
        return np.array(
            [[self.xmin, self.ymin], [self.xmax, self.ymax]], dtype=np.float64
        )

    @override
    def add_port(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        name: str | None = None,
        *,
        port: ProtoPort[Any] | None = None,
        center: Position | kdb.DPoint | None = None,
        width: float | None = None,
        orientation: AngleInDegrees | None = None,
        layer: LayerSpec | None = None,
        port_type: str | None = None,
        keep_mirror: bool = False,
        cross_section: CrossSectionSpec | None = None,
        register_cross_section: bool = False,
    ) -> DPort:
        """Adds a Port to the Component.

        Args:
            name: name of the port.
            port: port to add.
            center: center of the port.
            width: width of the port.
            orientation: orientation of the port. If None and port is provided, preserves the original port's orientation. If None and port is not provided, defaults to 0.
            layer: layer spec to add port on.
            port_type: port type (optical, electrical, …). If None and port is provided, preserves the original port's type. If None and port is not provided, defaults to "optical".
            keep_mirror: if True, keeps the mirror of the port.
            cross_section: cross_section of the port.
            register_cross_section: registers the CrossSection factory
        """
        if self.locked:
            raise LockedError(self)

        from gdsfactory.pdk import get_active_pdk, get_cross_section, get_layer

        override_transformation = False
        if port:
            override_transformation = (center is not None) or (orientation is not None)
            center = center if center is not None else port.center
            width = width if width is not None else port.width
            orientation = orientation if orientation is not None else port.orientation
            layer = layer if layer is not None else port.layer
            port_type = port_type if port_type is not None else port.port_type
            name = name if name is not None else port.name
            _xs = port.info.get("cross_section")
            _xs_is_registered = (
                isinstance(_xs, str) and _xs in get_active_pdk().cross_sections
            )
            cross_section = (
                cross_section
                if cross_section is not None
                else _xs
                if _xs_is_registered
                else getattr(port, "cross_section", _xs)
            )

        xs_name = None
        if cross_section:
            xs = get_cross_section(cross_section)
            xs_name = xs.name
            if layer is None:
                layer = xs.layer
            if width is None:
                width = xs.width

        if port_type is None:
            port_type = "optical"
        if orientation is None:
            orientation = 0

        if port_type not in CONF.port_types:
            warnings.warn(
                f"Port type {port_type} not in {CONF.port_types}. "
                "Please add it to the port_types list in the config gf.CONF.port_types.",
                stacklevel=3,
            )

        if layer is None:
            raise AddPortError("Must specify layer or cross_section")
        if width is None:
            raise AddPortError("Must specify width or cross_section")
        if center is None:
            raise AddPortError("Must specify center or port")

        if not port or override_transformation:
            if isinstance(center, kdb.DPoint):
                trans = kdb.DCplxTrans(1, orientation, False, center.to_v())
            else:
                x, y = float(center[0]), float(center[1])
                trans = kdb.DCplxTrans(1, float(orientation), False, x, y)
        else:
            trans = port.dcplx_trans
            if not keep_mirror:
                trans.mirror = False

        layer = get_layer(layer)

        info = (
            port.info.model_copy(deep=True).model_dump() if port is not None else None
        )

        _port = DPorts(kcl=self.kcl, bases=self.ports.bases).create_port(
            name=name,
            width=width,
            layer=layer,
            port_type=port_type,
            dcplx_trans=trans,
            info=info,
        )

        if xs_name:
            _port.info["cross_section"] = xs_name
            if register_cross_section:
                from gdsfactory.pdk import get_active_pdk

                pdk = get_active_pdk()
                if xs_name in pdk.cross_sections:
                    xs_registered = get_cross_section(xs_name)
                    xs_new = xs
                    if xs_registered != xs_new:
                        raise KeyError(
                            f"Found a different CrossSection named {xs_name} in pdk.cross_sections, cannot register {xs_new}"
                        )
                else:
                    pdk.register_cross_sections(**{xs_name: lambda: xs})

        return _port

    def copy(self) -> Component:
        """Copy the full cell."""
        return self.dup()  # type: ignore[return-value]

    def add_label(
        self,
        text: str = "hello",
        position: Position | kf.kdb.DPoint = (0.0, 0.0),
        layer: LayerSpec = "TEXT",
    ) -> None:
        """Adds Label to the Component.

        Args:
            text: Label text.
            position: x-, y-coordinates of the Label location.
            layer: Specific layer(s) to put Label on.
        """
        from gdsfactory.pdk import get_layer

        if self.locked:
            raise LockedError(self)

        layer = get_layer(layer)
        if isinstance(position, kf.kdb.DPoint):
            x, y = position.x, position.y
        else:
            x, y = position

        trans = kdb.DTrans(0, False, x, y)
        self.shapes(layer).insert(kf.kdb.DText(text, trans))

    def get_ports_list(self, **kwargs: Any) -> list[Port]:
        """Returns list of ports.

        Args:
            kwargs: Additional kwargs.

        Keyword Args:
            layer: select ports with GDS layer.
            prefix: select ports with prefix in port name.
            suffix: select ports with port name suffix.
            orientation: select ports with orientation in degrees.
            orientation: select ports with orientation in degrees.
            width: select ports with port width.
            layers_excluded: List of layers to exclude.
            port_type: select ports with port_type (optical, electrical, vertical_te).
            clockwise: if True, sort ports clockwise, False: counter-clockwise.
        """
        from gdsfactory.port import select_ports

        return select_ports(ports=self.ports.to_dtype(), **kwargs)

    def add_route_info(
        self,
        cross_section: CrossSection | str,
        length: float,
        length_eff: float | None = None,
        taper: bool = False,
        **kwargs: Any,
    ) -> None:
        """Adds route information to a component.

        Args:
            cross_section: CrossSection or name of the cross_section.
            length: length of the route.
            length_eff: effective length of the route.
            taper: if True adds taper information.
            kwargs: extra information to add to the component.
        """
        from gdsfactory.pdk import get_active_pdk

        if self.locked:
            raise LockedError(self)

        pdk = get_active_pdk()

        length_eff = length_eff or length
        xs_name = (
            cross_section
            if isinstance(cross_section, str)
            else pdk.get_cross_section_name(cross_section)
        )

        info = self.info
        if taper:
            info[f"route_info_{xs_name}_taper_length"] = length

        info["route_info_type"] = xs_name
        info["route_info_length"] = length_eff
        info["route_info_weight"] = length_eff
        info[f"route_info_{xs_name}_length"] = length_eff
        for key, value in kwargs.items():
            info[f"route_info_{key}"] = value

    def copy_child_info(self, component: kf.ProtoTKCell[Any]) -> None:
        """Copy and settings info from child component into parent.

        Parent components can access child cells settings.
        """
        if self.locked:
            raise LockedError(self)

        info = dict(component.info)

        for k, v in info.items():
            if k not in self.info:
                self.info[k] = v

    def write_gds(
        self,
        gdspath: PathType | None = None,
        gdsdir: PathType | None = None,
        save_options: kdb.SaveLayoutOptions | None = None,
        with_metadata: bool = True,
        exclude_layers: Sequence[LayerSpec] | None = None,
        no_empty_cells: bool = False,
        deduplicate_cell_names: bool = True,
    ) -> pathlib.Path:
        """Write component to GDS and returns gdspath.

        Args:
            gdspath: GDS file path to write to.
            gdsdir: directory for the GDS file. Defaults to /tmp/randomFile/gdsfactory.
            save_options: klayout save options.
            with_metadata: if True, writes metadata (ports, settings) to the GDS file.
            exclude_layers: list of layers to exclude from the GDS file.
            no_empty_cells: if True, does not save empty cells.
            deduplicate_cell_names: if True, renames cells with identical names to
                `cell_name$1`, `cell_name$2` etc.
        """
        from gdsfactory.pdk import get_layer

        if gdspath and gdsdir:
            warnings.warn(
                "gdspath and gdsdir have both been specified. "
                "gdspath will take precedence and gdsdir will be ignored.",
                stacklevel=3,
            )
        gdsdir = gdsdir or GDSDIR_TEMP
        gdsdir = pathlib.Path(gdsdir)
        gdsdir.mkdir(parents=True, exist_ok=True)
        name = self.name or ""
        gdspath = gdspath or gdsdir / f"{name[: CONF.max_cellname_length]}.gds"
        gdspath = pathlib.Path(gdspath)

        gdspath.parent.mkdir(parents=True, exist_ok=True)

        if save_options is None:
            save_options = save_layout_options(no_empty_cells=no_empty_cells)

        exclude_layers = exclude_layers or CONF.exclude_layers

        if exclude_layers:
            save_options.deselect_all_layers()
            selected_layers = set(self.kcl.layer_indexes()) - {
                get_layer(drop_layer) for drop_layer in exclude_layers
            }
            for layer in selected_layers:
                save_options.add_layer(layer, kf.kdb.LayerInfo())

        if not with_metadata:
            save_options.write_context_info = False

        self.write(
            filename=gdspath,
            save_options=save_options,
            deduplicate_cell_names=deduplicate_cell_names,
        )
        return pathlib.Path(gdspath)

    def pprint_ports(self, **kwargs: Any) -> None:
        pass

    def write_netlist(
        self, netlist: dict[str, Any], filepath: str | pathlib.Path | None = None
    ) -> str:
        pass

    def to_dict(self, with_ports: bool = False) -> dict[str, Any]:
        """Returns a dictionary representation of the Component."""
        from gdsfactory.port import to_dict

        d = {
            "name": self.name,
            "info": self.info.model_dump(exclude_none=True),
            "settings": self.settings.model_dump(exclude_none=True),
        }

        if with_ports:
            d["ports"] = {
                port.name: to_dict(port) for port in self.ports if port.name is not None
            }
        res = clean_value_json(d)
        assert isinstance(res, dict)
        return res

    def get_netlist(
        self,
        recursive: bool = False,
        *,
        on_multi_connect: ErrorBehavior = "error",
        on_dangling_port: ErrorBehavior = "warn",
        instance_namer: InstanceNamer | None = None,
        component_namer: ComponentNamer | None = None,
        netlist_namer: NetlistNamer | None = None,
        port_matcher: PortMatcher | None = None,
        serialization_max_digits: int = DEFAULT_SERIALIZATION_MAX_DIGITS,
    ) -> dict[str, Any]:
        pass

    def add_ref_off_grid(
        self, component: AnyComponent, name: str | None = None
    ) -> VInstance:
        """Adds a component instance reference to a Component without snapping to grid.

        Args:
            component: The referenced component.
            name: Name of the reference.
        """
        if self.locked:
            raise LockedError(self)

        ref = self.create_vinst(component)
        if name:
            ref.name = name
        return ref


type Route = (
    kf.routing.generic.ManhattanRoute | kf.routing.aa.optical.OpticalAllAngleRoute
)


class Component(ComponentBase, kf.DKCell):

    routes: dict[str, Route] = Field(default_factory=dict)

    def dup(self, new_name: str | None = None) -> Self:
        """Copy the full cell.

        Overrides kfactory's dup() to fix pin port mapping during copy.
        kfactory builds port_mapping from ephemeral Port wrappers, but pin
        ports are BasePort objects — the id() values never match.
        """
        saved_pins = self._base.pins
        self._base.pins = []
        try:
            c = super().dup(new_name=new_name)
        finally:
            self._base.pins = saved_pins
        if saved_pins:
            port_mapping = {id(b): i for i, b in enumerate(self.ports._bases)}
            c._base.pins = [
                BasePin(
                    name=p.name,
                    kcl=self.kcl,
                    ports=[c.base.ports[port_mapping[id(port)]] for port in p.ports],
                    pin_type=p.pin_type,
                    info=p.info,
                )
                for p in saved_pins
            ]
        return c

    @override
    def write(
        self,
        filename: str | pathlib.Path,
        save_options: kdb.SaveLayoutOptions | None = None,
        convert_external_cells: bool = False,
        set_meta_data: bool = True,
        autoformat_from_file_extension: bool = True,
        deduplicate_cell_names: bool = True,
    ) -> None:
        """Write component to GDS, fixing pin metadata for kfactory compat."""
        if set_meta_data:
            self.insert_vinsts()
            self.kcl.set_meta_data()
            for ci in self.called_cells():
                kcell = self.kcl[ci]
                if not kcell._destroyed():
                    if convert_external_cells and kcell.is_library_cell():
                        kcell.convert_to_static(recursive=True)
                    kcell.set_meta_data()
                    _fix_pin_metadata(kcell)
            if convert_external_cells and self.is_library_cell():
                self.convert_to_static(recursive=True)
            self.set_meta_data()
            _fix_pin_metadata(self)
        super().write(
            filename,
            save_options=save_options,
            convert_external_cells=False,
            set_meta_data=False,
            autoformat_from_file_extension=autoformat_from_file_extension,
            deduplicate_cell_names=deduplicate_cell_names,
        )

    @property
    def layers(self) -> list[Layer]:
        return [
            (info.layer, info.datatype)
            for info in self.kcl.layout.layer_infos()
            if not self.bbox(self.kcl.layout.layer(info)).empty()
        ]

    def add(self, instances: Iterable[ComponentReference] | ComponentReference) -> None:
        if self.locked:
            raise LockedError(self)

        if not isinstance(instances, Iterable):
            instance_list = [instances]
        else:
            instance_list = list(instances)

        for instance in instance_list:
            self.kdb_cell.insert(instance.instance)

    def absorb(self, reference: ComponentReference) -> Self:
        pass

    def trim(
        self,
        left: float,
        bottom: float,
        right: float,
        top: float,
        flatten: bool = False,
    ) -> None:
        """Trims the Component to a bounding box.

        Args:
            left: left coordinate of the bounding box.
            bottom: bottom coordinate of the bounding box.
            right: right coordinate of the bounding box.
            top: top coordinate of the bounding box.
            flatten: if True, flattens the Component.
        """
        if self.locked:
            raise LockedError(self)

        c = self

        domain_box = kdb.DBox(left, bottom, right, top)
        if not c.dbbox().inside(domain_box):
            kdb_cell = c.kcl.layout.clip(c.kdb_cell, kdb.DBox(left, bottom, right, top))
            c.kdb_cell.clear()
            c.kdb_cell.copy_tree(kdb_cell)
            kdb_cell.delete()
            if flatten:
                c.flatten()

    def __lshift__(self, cell: kf.ProtoTKCell[Any]) -> ComponentReference:
        """Convenience function for adding instances/references to a Component.

        Args:
            cell: The cell to be added as an instance
        """
        return self.add_ref(cell)

    def add_ref(
        self,
        component: kf.ProtoTKCell[Any],
        name: str | None = None,
        columns: int = 1,
        rows: int = 1,
        column_pitch: float = 0.0,
        row_pitch: float = 0.0,
    ) -> ComponentReference:
        """Adds a component instance reference to a Component.

        Args:
            component: The referenced component.
            name: Name of the reference.
            columns: Number of columns in the array.
            rows: Number of rows in the array.
            column_pitch: column pitch.
            row_pitch: row pitch.
        """
        if isinstance(component, ComponentAllAngle):
            raise ValueError(
                f"Use Component.add_ref_off_grid() for all angle {component.name!r}"
            )
        if not isinstance(component, kf.ProtoTKCell):
            raise ValueError(f"Expected a Component, got {type(component)}")

        if self.locked:
            raise LockedError(self)

        if rows > 1 or columns > 1:
            if rows > 1 and row_pitch == 0:
                raise ValueError(f"rows = {rows} > 1 require {row_pitch=} > 0")

            if columns > 1 and column_pitch == 0:
                raise ValueError(f"columns = {columns} > 1 require {column_pitch} > 0")

            a = kf.kdb.DVector(column_pitch, 0)
            b = kf.kdb.DVector(0, row_pitch)

            inst = self.create_inst(component, na=columns, nb=rows, a=a, b=b)
        else:
            inst = self.create_inst(component)
        if name is not None:
            inst.name = name
        return ComponentReference(kcl=self.kcl, instance=inst.instance)

    def get_paths(self, layer: LayerSpec, recursive: bool = True) -> list[kf.kdb.DPath]:
        """Returns a list of paths.

        Args:
            layer: layer to get paths from.
            recursive: if True, gets paths recursively.
        """
        from gdsfactory import get_layer

        paths: list[kf.kdb.DPath] = []

        layer = get_layer(layer)

        if recursive:
            iterator = self.kdb_cell.begin_shapes_rec(layer)
            iterator.shape_flags = kdb.Shapes.SPaths
            paths.extend(
                it.shape().dpath.transformed(it.dtrans()) for it in iterator.each()
            )
        else:
            paths.extend(
                shape.dpath
                for shape in self.kdb_cell.shapes(layer).each(kdb.Shapes.SPaths)
            )
        return paths

    def get_boxes(self, layer: LayerSpec, recursive: bool = True) -> list[kf.kdb.DBox]:
        pass

    def get_labels(
        self, layer: LayerSpec, recursive: bool = True
    ) -> list[kf.kdb.DText]:
        """Returns a list of labels from the Component.

        Args:
            layer: layer to get labels from.
            recursive: if True, gets labels recursively.
        """
        from gdsfactory import get_layer

        texts: list[kf.kdb.DText] = []
        layer_enum = get_layer(layer)

        if recursive:
            iterator = self.kdb_cell.begin_shapes_rec(layer_enum)
            iterator.shape_flags = kdb.Shapes.STexts
            texts.extend(
                it.shape().dtext.transformed(it.dtrans()) for it in iterator.each()
            )
        else:
            texts.extend(
                shape.dtext
                for shape in self.kdb_cell.shapes(layer_enum).each(kdb.Shapes.STexts)
            )
        return texts

    def area(self, layer: LayerSpec) -> float:
        """Returns the area of the Component in um2."""
        from gdsfactory import get_layer

        layer_index = get_layer(layer)
        r = kdb.Region(self.kdb_cell.begin_shapes_rec(layer_index))
        r.merge()
        return float(sum(p.area2() / 2 * self.kcl.dbu**2 for p in r.each()))

    def get_polygons(
        self,
        merge: bool = False,
        by: Literal["index", "name", "tuple"] = "index",
        layers: LayerSpecs | None = None,
        smooth: float | None = None,
    ) -> dict[tuple[int, int] | str | int, list[kf.kdb.Polygon]]:
        """Returns a dict of Polygons per layer.

        Args:
            merge: if True, merges the polygons.
            by: the format of the resulting keys in the dictionary ('index', 'name', 'tuple')
            layers: list of layers to get polygons from. Defaults to all layers.
            smooth: if True, smooths the polygons.
        """
        if merge and self.locked:
            raise LockedError(self)

        from gdsfactory.functions import get_polygons

        return get_polygons(self, merge=merge, by=by, layers=layers, smooth=smooth)

    def get_region(
        self, layer: LayerSpec, merge: bool = False, smooth: float | None = None
    ) -> kdb.Region:
        """Returns a Region of the Component.

        Note that all operations that you do with the Region will be done in the database units.

        Where for most processes 1 dbu = 1 nm.

        Args:
            layer: layer to get region from.
            merge: if True, merges the region.
            smooth: if True, smooths the region by the specified amount (in um).
        """
        from gdsfactory import get_layer

        layer_index = get_layer(layer)
        r = kdb.Region(self.kdb_cell.begin_shapes_rec(layer_index))
        if smooth:
            r.smooth(self.kcl.to_dbu(smooth))
        if merge:
            r.merge()
        return r

    def get_polygons_points(
        self,
        merge: bool = False,
        scale: float | None = None,
        by: Literal["index", "name", "tuple"] = "index",
        layers: LayerSpecs | None = None,
    ) -> dict[int | str | tuple[int, int], list[npt.NDArray[np.floating[Any]]]]:
        """Returns a dict with list of points per layer.

        Args:
            merge: if True, merges the polygons.
            scale: if True, scales the points.
            by: the format of the resulting keys in the dictionary ('index', 'name', 'tuple')
            layers: list of layers to get polygons from. Defaults to all layers.
        """
        if merge and self.locked:
            raise LockedError(self)

        from gdsfactory.functions import get_polygons_points

        return get_polygons_points(self, merge=merge, scale=scale, by=by, layers=layers)

    def extract(
        self,
        layers: LayerSpecs,
        recursive: bool = True,
    ) -> Component:
        """Extracts a list of layers and adds them to a new Component.

        Args:
            layers: list of layers to extract.
            recursive: if True, extracts layers recursively and returns a flattened Component.
        """
        from gdsfactory.functions import extract

        return extract(self, layers=layers, recursive=recursive)

    def copy_layers(
        self,
        layer_map: dict[LayerSpec, LayerSpec],
        recursive: bool = False,
    ) -> Self:
        pass

    def remove_layers(
        self,
        layers: LayerSpecs,
        recursive: bool = True,
    ) -> Self:
        """Removes a list of layers and returns the same Component.

        Args:
            layers: list of layers to remove.
            recursive: if True, removes layers recursively and temporarily unlocks components.
        """
        from gdsfactory import get_layer

        if recursive:
            self.locked = False

        if self.locked:
            raise LockedError(self)

        layer_indexes = self.kcl.layer_indexes()
        layer_indexes_to_remove = [get_layer(layer) for layer in layers]
        layer_indices = [
            layer for layer in layer_indexes_to_remove if layer in layer_indexes
        ]
        if not layer_indices:
            return self

        kdb_cell = self.kdb_cell
        for layer_index in layer_indices:
            kdb_cell.shapes(layer_index).clear()

        if recursive:
            for ci in kdb_cell.called_cells():
                child = self.kcl[ci]
                child_cell = child.kdb_cell
                was_locked = child.locked
                child.locked = False
                try:
                    for layer_idx in layer_indices:
                        child_cell.shapes(layer_idx).clear()
                finally:
                    if was_locked:
                        child.locked = True
        return self

    def remap_layers(
        self, layer_map: dict[LayerSpec, LayerSpec], recursive: bool = False
    ) -> Self:
        pass

    def to_3d(
        self,
        layer_views: LayerViews | None = None,
        layer_stack: LayerStack | None = None,
        exclude_layers: Sequence[Layer] | None = None,
    ) -> Scene:
        """Return Component 3D trimesh Scene.

        Args:
            component: to extrude in 3D.
            layer_views: layer colors from Klayout Layer Properties file.
                Defaults to active PDK.layer_views.
            layer_stack: contains thickness and zmin for each layer.
                Defaults to active PDK.layer_stack.
            exclude_layers: layers to exclude.

        """
        from gdsfactory.export.to_3d import to_3d

        return to_3d(
            self,
            layer_views=layer_views,
            layer_stack=layer_stack,
            exclude_layers=exclude_layers,
        )

    def over_under(
        self,
        layer: LayerSpec,
        distance: float = 0.001,
        remove_old_layer: bool = True,
        corner_mode: int | CornerMode = 2,
    ) -> None:
        pass

    def fix_spacing(
        self,
        layer: LayerSpec,
        min_space: float = 0.2,
        size_bias: float = 0.0,
    ) -> None:
        pass

    def fix_width(
        self,
        layer: LayerSpec,
        min_width: float = 0.2,
        n_threads: int | None = None,
        tile_size: tuple[float, float] | None = None,
        overlap: int = 1,
        smooth: int | None = None,
        flatten: bool = True,
    ) -> None:
        pass

    def offset(
        self,
        layer: LayerSpec,
        distance: float,
        flatten: bool = False,
        corner_mode: int | CornerMode = 2,
    ) -> None:
        """Offsets a Component layer by a distance in um.

        Args:
            layer: layer to offset the Component on.
            distance: distance to offset the Component in um.
            flatten: if True, flattens the Component before offsetting.
            corner_mode: determines behavior around corners
        """
        from gdsfactory import get_layer

        if self.locked:
            raise LockedError(self)

        if flatten:
            self.flatten()

        distance_dbu = self.kcl.to_dbu(distance)

        layer_index = get_layer(layer)
        region = kdb.Region(self.kdb_cell.begin_shapes_rec(layer_index))
        region.size(distance_dbu, distance_dbu, corner_mode)
        self.remove_layers([layer])
        self.kdb_cell.shapes(layer_index).insert(region)

        self.kcl.layout.end_changes()

    def add_polygon(self, points: _PolygonPoints, layer: LayerSpec) -> kdb.Shape | None:
        """Adds a Polygon to the Component and returns a klayout Shape.

        Args:
            points: Coordinates of the vertices of the Polygon.
            layer: layer spec to add polygon on.
        """
        from gdsfactory.pdk import get_layer

        if self.locked:
            raise LockedError(self)

        _layer = get_layer(layer)

        polygon = points_to_polygon(points)
        if isinstance(polygon, kdb.DPolygon | kdb.DSimplePolygon):
            polygon = polygon.to_itype(self.kcl.dbu)  # type: ignore[assignment]

        return self.kdb_cell.shapes(_layer).insert(polygon)

    @overload
    def plot(
        self,
        lyrdb: pathlib.Path | str | None = None,
        display_type: Literal["image", "widget"] | None = None,
        *,
        show_labels: bool = True,
        show_ruler: bool = True,
        pixel_buffer_options: PixelBufferOptions | None = None,
        return_fig: Literal[True] = True,
        ax: Axes | None = None,
    ) -> Figure: ...

    @overload
    def plot(
        self,
        lyrdb: pathlib.Path | str | None = None,
        display_type: Literal["image", "widget"] | None = None,
        *,
        show_labels: bool = True,
        show_ruler: bool = True,
        pixel_buffer_options: PixelBufferOptions | None = None,
        return_fig: Literal[False] = False,
        ax: Axes | None = None,
    ) -> None: ...

    def plot(
        self,
        lyrdb: pathlib.Path | str | None = None,
        display_type: Literal["image", "widget"] | None = None,
        *,
        show_labels: bool = True,
        show_ruler: bool = True,
        pixel_buffer_options: PixelBufferOptions | None = None,
        return_fig: bool = False,
        ax: Axes | None = None,
    ) -> Figure | None:
        pass

    def plot_netlist(
        self,
        recursive: bool = False,
        with_labels: bool = True,
        font_weight: str = "normal",
        **kwargs: Any,
    ) -> nx.Graph:
        pass

    def plot_netlist_graphviz(
        self, recursive: bool = False, interactive: bool = False, splines: str = "ortho"
    ) -> None:
        pass

    def to_graphviz(self, recursive: bool = False) -> Digraph:
        pass

    def fill(
        self,
        fill_cell: ComponentSpec,
        fill_layers: Iterable[tuple[LayerSpec, float]] = [],
        fill_regions: Iterable[tuple[kdb.Region, float]] = [],
        exclude_layers: Iterable[tuple[LayerSpec, float]] = [],
        exclude_regions: Iterable[tuple[kdb.Region, float]] = [],
        n_threads: int | None = None,
        tile_size: tuple[float, float] | None = None,
        row_step: kdb.DVector | None = None,
        col_step: kdb.DVector | None = None,
        x_space: float = 0.0,
        y_space: float = 0.0,
        tile_border: tuple[float, float] = (20, 20),
        multi: bool = False,
    ) -> None:
        pass


class ComponentAllAngle(ComponentBase, kf.VKCell):
    def plot(self, **kwargs: Any) -> None:
        pass

    def dup(self, new_name: str | None = None) -> ComponentAllAngle:
        """Copy the full cell."""
        c = self.__class__(
            kcl=self.kcl, name=new_name or self.name + "$1" if self.name else None
        )
        c.ports = self.ports.copy()

        c.settings = self.settings.model_copy()
        c.settings_units = self.settings_units.model_copy()
        c.info = self.info.model_copy()
        for layer, shapes in self.shapes().items():
            for shape in shapes:
                c.shapes(layer).insert(shape)
        c._base.vinsts = self.vinsts.dup()

        return c

    def add_polygon(self, points: _PolygonPoints, layer: LayerSpec) -> kdb.Shape | None:
        """Adds a Polygon to the Component and returns a klayout Shape.

        Args:
            points: Coordinates of the vertices of the Polygon.
            layer: layer spec to add polygon on.
        """
        from gdsfactory.pdk import get_layer

        if self.locked:
            raise LockedError(self)

        _layer = get_layer(layer)

        polygon = points_to_polygon(points)

        res = self.shapes(_layer).insert(polygon)  # type: ignore[func-returns-value]
        return res

    def get_polygons(self, layer: LayerSpec) -> list[kf.kdb.DPolygon]:
        """Returns a list of polygons from the Component."""
        from gdsfactory import get_layer

        return [x for x in self.shapes(get_layer(layer)) if isinstance(x, kdb.DPolygon)]


def container(
    component: ComponentSpec,
    function: Callable[..., Any] | None = None,
    copy_ports: bool = True,
    **kwargs: Any,
) -> Component:
    """Returns new component with a component reference.

    Args:
        component: to add to container.
        function: function to apply to component.
        copy_ports: if True, copies ports from component to container.
        kwargs: keyword arguments to pass to function.
    """
    import gdsfactory as gf

    component = gf.get_component(component)
    c = Component()
    cref = c << component
    if copy_ports:
        c.add_ports(cref.ports)
    if function:
        function(component=c, **kwargs)

    c.copy_child_info(component)
    return c


def nets_to_connections(
    nets: list[dict[str, Any]], connections: dict[str, Any]
) -> dict[str, str]:
    pass
