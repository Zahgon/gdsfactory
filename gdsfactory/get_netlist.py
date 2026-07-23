
import inspect
import re
import secrets
import warnings
from collections import defaultdict
from collections.abc import Iterable
from hashlib import md5
from itertools import chain, product
from typing import Any, Literal, Protocol, cast

import kfactory as kf
from natsort import natsorted

import gdsfactory as gf
import gdsfactory.schematic as scm
from gdsfactory.component import Component
from gdsfactory.name import get_instance_name_from_alias as legacy_namer  # noqa: F401
from gdsfactory.serialization import DEFAULT_SERIALIZATION_MAX_DIGITS, clean_value_json

type Instance = kf.DInstance | kf.VInstance | kf.Instance
type ErrorBehavior = Literal["ignore", "warn", "error"]


class ComponentNamer(Protocol):

    def __call__(self, cell: kf.ProtoTKCell[Any]) -> str:
        """Return the component name for the given cell."""
        ...


def factory_namer(cell: kf.ProtoTKCell[Any]) -> str:
    pass


def function_namer(cell: kf.ProtoTKCell[Any]) -> str:
    pass


def cell_namer(cell: kf.ProtoTKCell[Any]) -> str:
    pass


class InstanceNamer(Protocol):

    def __call__(self, inst: Instance) -> str:
        """Return the instance name for the given instance."""
        ...


class OriginalNamer:

    def __init__(self) -> None:
        self._instance_names: dict[str | None, str] = {}
        self._rev_instance_names: dict[str, str | None] = {}

    def __call__(self, inst: Instance) -> str:
        inst_name = _instname(inst)
        if inst_name in self._instance_names:
            return self._instance_names[inst_name]
        name = self._instance_names[inst_name] = _clean_instname(inst_name)
        self._rev_instance_names[name] = inst_name
        return name


class CountedNamer:

    def __init__(self, component_namer: ComponentNamer) -> None:
        self._component_namer = component_namer
        self._instance_names: dict[str | None, str] = {}
        self._rev_instance_names: dict[str, str | None] = {}

    def __call__(self, inst: Instance) -> str:
        inst_name = _instname(inst)
        if inst_name in self._instance_names:
            return self._instance_names[inst_name]
        compname = _short_component_name(_instcell(inst), self._component_namer)
        name = _instname_from_compname(
            inst, compname, self._instance_names, self._rev_instance_names
        )
        name = self._instance_names[inst_name] = _clean_instname(name)
        self._rev_instance_names[name] = inst_name
        return name


class SmartNamer:

    def __init__(self, component_namer: ComponentNamer) -> None:
        self._component_namer = component_namer
        self._instance_names: dict[str | None, str] = {}
        self._rev_instance_names: dict[str, str | None] = {}

    def __call__(self, inst: Instance) -> str:
        inst_name = _instname(inst)
        if inst_name in self._instance_names:
            return self._instance_names[inst_name]
        compname = _short_component_name(_instcell(inst), self._component_namer)
        if inst_name is not None and inst_name.startswith(f"{compname}_"):
            name: str | None = _instname_from_compname(
                inst, compname, self._instance_names, self._rev_instance_names
            )
        else:
            name = inst_name
        cleaned = self._instance_names[inst_name] = _clean_instname(name)
        self._rev_instance_names[cleaned] = inst_name
        return cleaned


class NetlistNamer(Protocol):

    def __call__(self, cell: kf.ProtoTKCell[Any]) -> str:
        """Return the name for the given cell in the netlist."""
        ...


class CountedNetlistNamer:

    def __init__(self, component_namer: ComponentNamer) -> None:
        self._component_namer = component_namer
        self._cell_names: dict[str, str] = {}  # cell.name -> assigned name
        self._used_names: set[str] = set()

    def __call__(self, cell: kf.ProtoTKCell[Any]) -> str:
        if cell.name in self._cell_names:
            return self._cell_names[cell.name]

        base = self._component_namer(cell)

        if not _has_instances(cell):
            name = base
        else:
            name = self._get_unique_name(base)

        self._cell_names[cell.name] = name
        self._used_names.add(name)
        return name

    def _get_unique_name(self, base: str) -> str:
        pass


type MatchResult = bool | dict[str, Any]


class PortMatcher(Protocol):

    def __call__(
        self, port1: kf.DPort | kf.Port, port2: kf.DPort | kf.Port
    ) -> MatchResult:
        """Return match result: False, True, or dict with metadata."""
        ...


class PortCenterMatcher:

    def __init__(self, tolerance_dbu: int = 2) -> None:
        self.tolerance_dbu = tolerance_dbu

    def __call__(self, port1: kf.DPort | kf.Port, port2: kf.DPort | kf.Port) -> bool:
        """Return True if two ports are at the same location (within tolerance)."""
        if port1.port_type != port2.port_type:
            return False
        x1, y1 = port1.to_itype().center
        x2, y2 = port2.to_itype().center
        return abs(x2 - x1) < self.tolerance_dbu and abs(y2 - y1) < self.tolerance_dbu


class SmartPortMatcher:

    def __init__(
        self,
        position_tolerance_dbu: int = 2,
        width_tolerance: float = 0.001,
        angle_tolerance: float = 0.01,
    ) -> None:
        self.position_tolerance_dbu = position_tolerance_dbu
        self.width_tolerance = width_tolerance
        self.angle_tolerance = angle_tolerance

    def __call__(self, port1: kf.DPort | kf.Port, port2: kf.DPort | kf.Port) -> bool:
        """Return True if ports match in position, width, and orientation."""
        if port1.port_type != port2.port_type:
            return False
        x1, y1 = port1.to_itype().center
        x2, y2 = port2.to_itype().center
        if (
            abs(x2 - x1) >= self.position_tolerance_dbu
            or abs(y2 - y1) >= self.position_tolerance_dbu
        ):
            return False

        if abs(port1.width - port2.width) > self.width_tolerance:
            return False

        if port1.port_type == "electrical" or port2.port_type == "electrical":
            return True

        angle_diff = abs(_angle_difference(port1.orientation, port2.orientation))
        if abs(angle_diff - 180) > self.angle_tolerance:  # noqa: SIM103
            return False

        return True


class FlexiblePortMatcher:

    def __init__(
        self,
        position_tolerance_dbu: int = 2,
        angle_tolerance: float = 0.01,
    ) -> None:
        self.position_tolerance_dbu = position_tolerance_dbu
        self.angle_tolerance = angle_tolerance

    def __call__(
        self, port1: kf.DPort | kf.Port, port2: kf.DPort | kf.Port
    ) -> MatchResult:
        """Return match result with width mismatch metadata if applicable."""
        if port1.port_type != port2.port_type:
            return False

        x1, y1 = port1.to_itype().center
        x2, y2 = port2.to_itype().center
        if (
            abs(x2 - x1) >= self.position_tolerance_dbu
            or abs(y2 - y1) >= self.position_tolerance_dbu
        ):
            return False

        if port1.port_type != "electrical":
            angle_diff = abs(_angle_difference(port1.orientation, port2.orientation))
            if abs(angle_diff - 180) > self.angle_tolerance:
                return False

        width_diff = abs(port1.width - port2.width)
        if width_diff > 0.001:  # small tolerance for floating point
            return {
                "width1": port1.width,
                "width2": port2.width,
            }

        return True


def _angle_difference(angle1: float, angle2: float) -> float:
    pass


def _flip_port(port: kf.DPort | kf.Port) -> kf.DPort:
    """Return a copy of the port with orientation flipped by 180°."""
    return kf.DPort(
        name=port.name,
        center=(port.x, port.y),
        orientation=port.orientation + 180,
        width=port.width,
        layer=port.layer,
        port_type=port.port_type,
    )


_default_port_matcher = SmartPortMatcher()


def get_netlist(
    cell: kf.ProtoTKCell[Any],
    *,
    on_multi_connect: ErrorBehavior = "error",
    on_dangling_port: ErrorBehavior = "warn",
    instance_namer: InstanceNamer | None = None,
    component_namer: ComponentNamer = function_namer,
    port_matcher: PortMatcher | None = None,
    serialization_max_digits: int = DEFAULT_SERIALIZATION_MAX_DIGITS,
) -> dict[str, Any]:
    pass


def get_netlist_recursive(
    cell: kf.ProtoTKCell[Any],
    *,
    on_multi_connect: ErrorBehavior = "error",
    on_dangling_port: ErrorBehavior = "warn",
    instance_namer: InstanceNamer | None = None,
    component_namer: ComponentNamer = function_namer,
    netlist_namer: NetlistNamer | None = None,
    port_matcher: PortMatcher | None = None,
    serialization_max_digits: int = DEFAULT_SERIALIZATION_MAX_DIGITS,
) -> dict[str, Any]:
    """Extract netlists recursively from a cell and all its subcells.

    Args:
        cell: The cell to extract the netlist from.
        on_multi_connect: What to do when more than two ports overlap.
            "ignore": silently allow, "warn": allow with warning, "error": raise.
        on_dangling_port: What to do when an instance port is not connected.
            "ignore": silently allow, "warn": allow with warning, "error": raise.
        instance_namer: Callable to name instances.
            Defaults to SmartNamer(component_namer).
        component_namer: Callable to name components in instance dicts.
            Defaults to function_namer.
        netlist_namer: Callable to name cells in the recursive netlist.
            Defaults to CountedNetlistNamer(component_namer).
        port_matcher: Callable to determine if two ports are connected.
            Defaults to SmartPortMatcher().
        serialization_max_digits: How many float digits to preserve.
            Defaults to DEFAULT_SERIALIZATION_MAX_DIGITS

    Returns:
        A dictionary mapping cell names to their netlists.
    """
    recnet: dict[str, Any] = {}
    _insert_netlist(
        recnet,
        cell,
        on_multi_connect,
        on_dangling_port,
        instance_namer or SmartNamer(component_namer),
        component_namer,
        netlist_namer or CountedNetlistNamer(component_namer),
        port_matcher or _default_port_matcher,
        recursive=True,
    )
    return cast(
        dict[str, dict[str, Any]],
        clean_value_json(recnet, serialization_max_digits=serialization_max_digits),
    )


def _insert_netlist(
    recnet: dict[str, Any],
    cell: kf.ProtoTKCell[Any],
    on_multi_connect: ErrorBehavior,
    on_dangling_port: ErrorBehavior,
    instance_namer: InstanceNamer,
    component_namer: ComponentNamer,
    netlist_namer: NetlistNamer,
    port_matcher: PortMatcher,
    recursive: bool,
) -> None:
    cell_name = netlist_namer(cell)
    if cell_name in recnet:
        return
    net = recnet[cell_name] = {
        "instances": {},
        "placements": {},
        "ports": {},
        "nets": {},
    }
    _all_ports: dict[str, kf.DPort | kf.Port] = {}
    for _inst in sorted(
        chain(cell.insts, cell.vinsts), key=lambda i: getattr(i, "name", "") or ""
    ):
        inst = cast(Instance, _inst)
        inst_cell = _instcell(inst)
        inst_name = instance_namer(inst)
        if _is_pure_vinst(inst):
            if _is_array_inst(inst):
                msg = (
                    "Cannot export netlist: virtual array instances are not supported."
                )
                raise ValueError(msg)
            array = None
            virtual = True
            transform = inst.dcplx_trans
            _all_ports.update({f"{inst_name},{p.name}": p for p in inst.ports})
        elif _is_flattened_vinst(inst):
            if _is_array_inst(inst):
                msg = (
                    "Cannot export netlist: virtual array instances are not supported."
                )
            if hasattr(inst, "to_dtype"):  # always True - just making mypy happy
                inst = inst.to_dtype()
            array = None
            virtual = True
            transform = inst.dcplx_trans * inst.cell.vtrans  # type: ignore[union-attr]
            _all_ports.update({f"{inst_name},{p.name}": p for p in inst.ports})
        elif _is_array_inst(inst):
            if hasattr(inst, "to_dtype"):  # always True - just making mypy happy
                inst = inst.to_dtype()
            array = _get_array_config(inst)
            virtual = False
            transform = inst.dcplx_trans
            _all_ports.update(
                {
                    f"{inst_name}<{a}.{b}>,{p.name}": inst.ports[p.name, a, b]
                    for p, a, b in product(
                        inst_cell.ports, range(inst.na), range(inst.nb)
                    )
                }
            )
        else:
            if hasattr(inst, "to_dtype"):  # always True - just making mypy happy
                inst = inst.to_dtype()
            array = None
            virtual = False
            transform = inst.dcplx_trans
            _all_ports.update({f"{inst_name},{p.name}": p for p in inst.ports})

        net["instances"][inst_name] = _dump_instance(
            {
                "component": component_namer(inst_cell),
                "array": array,
                "settings": inst_cell.settings.model_dump(),
                "info": inst_cell.info.model_dump(),
                "virtual": virtual,
            }
        )
        net["placements"][inst_name] = {
            "x": transform.disp.x,
            "y": transform.disp.y,
            "rotation": transform.angle,
            "mirror": transform.mirror,
        }

        if recursive and _has_instances(inst_cell):
            net["instances"][inst_name]["component"] = netlist_namer(inst_cell)
            _insert_netlist(
                recnet,
                inst_cell,
                on_multi_connect,
                on_dangling_port,
                instance_namer,
                component_namer,
                netlist_namer,
                port_matcher,
                recursive,
            )

    for port in cell.ports:
        if port.name is not None:
            _all_ports[port.name] = _flip_port(cast(kf.DPort | kf.Port, port))

    all_nets = _get_nets(_all_ports, on_multi_connect, port_matcher)
    _handle_dangling_ports(_all_ports, all_nets, on_dangling_port)
    net["ports"], net["nets"] = _split_nets_and_ports(all_nets)


def _has_instances(cell: Any) -> bool:
    """Return True if the cell has any instances."""
    return bool(getattr(cell, "insts", False)) or bool(getattr(cell, "vinsts", False))


def _has_non_default_settings(cell: kf.ProtoTKCell[Any]) -> bool:
    pass


def _get_array_config(inst: Instance) -> scm.Array:
    kcl = inst.cell.kcl
    trans = inst.dcplx_trans
    inv_rot = kf.kdb.DCplxTrans(1, trans.angle, False, 0, 0).inverted()
    a = inv_rot * kf.kdb.DVector(inst.a.x, inst.a.y)
    b = inv_rot * kf.kdb.DVector(inst.b.x, inst.b.y)
    ax = round(kcl.dbu * a.x, 6)
    ay = round(kcl.dbu * a.y, 6)
    bx = round(kcl.dbu * b.x, 6)
    by = round(kcl.dbu * b.y, 6)
    match (
        ax == 0,
        ay == 0,
        bx == 0,
        by == 0,
    ):
        case (_, True, True, _):
            return scm.OrthogonalGridArray(
                columns=inst.na,
                rows=inst.nb,
                column_pitch=ax,
                row_pitch=by,
            )
        case (True, _, _, True):
            return scm.OrthogonalGridArray(
                columns=inst.nb,
                rows=inst.na,
                column_pitch=bx,
                row_pitch=ay,
            )
    return scm.GridArray(
        num_a=inst.na,
        num_b=inst.nb,
        pitch_a=(ax, ay),
        pitch_b=(bx, by),
    )


def _is_array_inst(inst: Instance) -> bool:
    return getattr(inst, "na", 0) > 1 or getattr(inst, "nb", 0) > 1


def _is_pure_vinst(inst: Instance) -> bool:
    return isinstance(inst, kf.VInstance)


def _is_flattened_vinst(inst: Instance) -> bool:
    return getattr(inst.cell, "vtrans", None) is not None


def _dump_instance(
    instance: dict[str, Any],
    instance_exclude: Iterable[str] = (),
) -> dict[str, Any]:
    instance_exclude = set(instance_exclude)
    dct = {}
    for k, v in instance.items():
        if (
            k in instance_exclude
            or (k == "array" and v is None)
            or (k == "virtual" and v is False)
        ):
            continue
        if hasattr(v, "model_dump"):
            dct[k] = v.model_dump()
        else:
            dct[k] = v
    return dct


def _short_component_name(
    cell: kf.ProtoTKCell[Any], component_namer: ComponentNamer
) -> str:
    pass


def _instname_from_compname(
    inst: Instance,
    compname: str,
    _instance_names: dict[str | None, str],
    _rev_instance_names: dict[str, str | None],
) -> str:
    pass


def _clean_instname(name: str | None) -> str:
    pass


def _handle_multi_connect(
    matched_pairs: dict[tuple[str, str], dict[str, Any] | None],
    all_ports: dict[str, kf.DPort | kf.Port],
    on_multi_connect: ErrorBehavior,
) -> None:
    """Check for multiple connections at same location and warn/error as configured."""
    if on_multi_connect == "ignore":
        return

    port_connections: dict[str, set[str]] = defaultdict(set)
    for p1, p2 in matched_pairs:
        port_connections[p1].add(p2)
        port_connections[p2].add(p1)

    for port, connected in port_connections.items():
        if len(connected) > 1:
            p = all_ports[port]
            x, y = p.x, p.y
            msg = f"More than two ports overlapping at ({x:.3f}, {y:.3f}), {port}: {connected | {port}}."
            if on_multi_connect == "error":
                raise ValueError(msg)
            warnings.warn(msg, stacklevel=5)


def _get_nets(
    all_ports: dict[str, kf.DPort | kf.Port],
    on_multi_connect: ErrorBehavior,
    port_matcher: PortMatcher,
) -> list[dict[str, Any]]:
    """Extract connections between ports.

    Uses spatial indexing to bucket ports by position for ~O(n) matching
    instead of O(n²).

    Returns:
        List of net dicts with keys 'p1', 'p2', and optionally 'settings'.
    """
    _matched_pairs: dict[tuple[str, str], dict[str, Any] | None] = {}

    _BUCKET = 5
    buckets: dict[tuple[int, int], list[tuple[str, kf.DPort | kf.Port]]] = defaultdict(
        list
    )
    for pname, p in all_ports.items():
        cx, cy = p.to_itype().center
        buckets[cx // _BUCKET, cy // _BUCKET].append((pname, p))

    for (bx, by), ports in buckets.items():
        candidates: list[tuple[str, kf.DPort | kf.Port]] = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nbr = buckets.get((bx + dx, by + dy))
                if nbr is not None:
                    candidates.extend(nbr)
        for pname, p in ports:
            for qname, q in candidates:
                if pname >= qname:
                    continue
                result = port_matcher(p, q)
                if result is not False:
                    if isinstance(result, dict):
                        _matched_pairs[pname, qname] = result
                    else:
                        _matched_pairs[pname, qname] = None

    _handle_multi_connect(_matched_pairs, all_ports, on_multi_connect)

    nets: list[dict[str, Any]] = []
    for (p1, p2), settings in _matched_pairs.items():
        net: dict[str, Any] = {"p1": p1, "p2": p2}
        if settings is not None:
            net["settings"] = settings
        nets.append(net)
    return nets


def _split_nets_and_ports(
    nets: list[dict[str, Any]],
) -> tuple[dict[str, str], list[dict[str, Any]]]:
    """Split nets into top-level port mappings and instance-to-instance nets.

    Top-level ports never have a ',' in their name, whereas instance ports
    are formatted as '{instance_name},{port_name}'.

    Note: Settings from nets involving top-level ports are discarded since
    the ports dict only maps port names to instance ports.
    """
    ports: dict[str, str] = {}
    instance_nets: list[dict[str, Any]] = []
    for net in nets:
        p1, p2 = net["p1"], net["p2"]
        if "," not in p1:
            ports[p1] = p2
        elif "," not in p2:
            ports[p2] = p1
        else:
            p1 = net["p1"]
            p2 = net["p2"]
            meta = {k: v for k, v in net.items() if k != "p1" and k != "p2"}
            if p1 < p2:
                instance_nets.append({"p1": p1, "p2": p2, **meta})
            else:
                instance_nets.append({"p1": p2, "p2": p1, **meta})
    ports = {k: ports[k] for k in natsorted(ports)}
    nets = natsorted(instance_nets, key=lambda n: f"{n['p1']}:{n['p2']}")
    return ports, nets


def _handle_dangling_ports(
    all_ports: dict[str, kf.DPort | kf.Port],
    nets: list[dict[str, Any]],
    on_dangling_port: ErrorBehavior,
) -> None:
    """Check for unconnected instance ports and warn/error as configured.

    Top-level ports (without ',' in name) are not considered dangling.
    """
    if on_dangling_port == "ignore":
        return

    connected: set[str] = set()
    for net in nets:
        connected.add(net["p1"])
        connected.add(net["p2"])

    dangling = [p for p in all_ports if "," in p and p not in connected]

    if dangling:
        msg = f"Unconnected ports: {dangling}"
        if on_dangling_port == "error":
            raise ValueError(msg)
        warnings.warn(msg, stacklevel=4)


@gf.cell
def _sample_circuit() -> Component:
    pass


def _width_mismatch_circuit() -> Component:
    pass


def _instname(inst: Instance) -> str:
    pass


def _instcell(inst: Instance) -> kf.ProtoTKCell[Any]:
    if _is_flattened_vinst(inst):
        inst_cell = gf.get_component(
            str(inst.cell.function_name or inst.cell.factory_name),
            **inst.cell.settings.model_dump(),
        )
        return cast(kf.ProtoTKCell[Any], inst_cell)
    return cast(kf.ProtoTKCell[Any], inst.cell)


if __name__ == "__main__":
    from gdsfactory.gpdk import PDK

    PDK.activate()

    c = _sample_circuit()
    netlist = c.get_netlist()
    c2 = gf.read.from_yaml(netlist)
    c2.show()
