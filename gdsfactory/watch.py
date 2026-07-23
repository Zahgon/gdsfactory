
from __future__ import annotations

import logging
import os
import pathlib
import sys
import threading
import time
import traceback
from types import SimpleNamespace

import kfactory as kf
from IPython.terminal.embed import embed
from watchdog.events import (
    DirCreatedEvent,
    DirDeletedEvent,
    DirModifiedEvent,
    DirMovedEvent,
    FileCreatedEvent,
    FileDeletedEvent,
    FileModifiedEvent,
    FileMovedEvent,
    FileSystemEventHandler,
)
from watchdog.observers import Observer

from gdsfactory.component import Component
from gdsfactory.config import cwd
from gdsfactory.pdk import Pdk, get_active_pdk
from gdsfactory.read.from_yaml_template import cell_from_yaml_template
from gdsfactory.typings import ComponentFactory, ComponentSpec, PathType

type _MovedEvent = DirMovedEvent | FileMovedEvent
type _CreatedEvent = DirCreatedEvent | FileCreatedEvent
type _DeletedEvent = DirDeletedEvent | FileDeletedEvent
type _ModifiedEvent = DirModifiedEvent | FileModifiedEvent


class FileWatcher(FileSystemEventHandler):

    def __init__(
        self,
        path: str,
        run_main: bool = False,
        run_cells: bool = True,
        logger: logging.Logger | None = None,
        allowed_dirs: list[PathType] | None = None,
    ) -> None:
        """Initialize the YAML event handler.

        Args:
            path: the path to the directory to watch.
            run_main: if True, will execute the main function of the file.
            run_cells: if True, will execute the cells of the file.
            logger: the logger to use.
            allowed_dirs: optional list of trusted directories. If provided, only
                files within these directories will be executed. Paths are resolved
                to absolute form for comparison.

        Security Warning:
            This watcher uses ``exec()`` to run Python files. Only watch directories
            containing trusted code. Use ``allowed_dirs`` to restrict execution to
            specific trusted directories.
        """
        super().__init__()

        self.logger = logger or logging.root
        self.run_cells = run_cells
        self.run_main = run_main
        self.allowed_dirs: list[pathlib.Path] | None = (
            [pathlib.Path(d).resolve() for d in allowed_dirs] if allowed_dirs else None
        )

        pdk = get_active_pdk()
        pdk.register_cells_yaml(dirpath=path, update=True)

        self.observer = Observer()
        self.path = path
        self.stopping = threading.Event()

    def start(self) -> None:
        self.observer.schedule(self, self.path, recursive=True)
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def run(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def update_cell(self, src_path: PathType, update: bool = False) -> ComponentFactory:
        """Parses a YAML file to a cell function and registers into active pdk.

        Args:
            src_path: the path to the file
            update: if True, will update an existing cell function of the same name without raising an error
        Returns:
            The cell function parsed from the yaml file.

        """
        pdk = get_active_pdk()
        print(f"Active PDK: {pdk.name!r}")
        filepath = pathlib.Path(src_path)
        cell_name = filepath.stem.split(".")[0]
        function = cell_from_yaml_template(filepath, name=cell_name)
        try:
            pdk.register_cells_yaml(update=update, **{cell_name: function})  # type: ignore[arg-type]
        except ValueError as e:
            print(e)
        return function

    def _get_path(self, path: str | bytes) -> str:
        pass

    def on_moved(self, event: _MovedEvent) -> None:
        pass

    def on_created(self, event: _CreatedEvent) -> None:
        pass

    def on_deleted(self, event: _DeletedEvent) -> None:
        pass

    def on_modified(self, event: _ModifiedEvent) -> None:
        pass

    def _is_allowed_path(self, filepath: pathlib.Path) -> bool:
        """Check if a file path is within the allowed directories.

        Args:
            filepath: the resolved path to check.

        Returns:
            True if allowed_dirs is not set, or if the file is within an allowed directory.
        """
        if self.allowed_dirs is None:
            return True
        resolved = filepath.resolve()
        return any(resolved == d or d in resolved.parents for d in self.allowed_dirs)

    def get_component(self, filepath: PathType) -> Component | None:
        """Parse a file and return the component, writing GDS output.

        Security Warning:
            Python files (``.py``) are executed via ``exec()`` with full interpreter
            privileges. Only run this on files you trust. Use the ``allowed_dirs``
            parameter on :class:`FileWatcher` to restrict which directories are
            eligible for execution.

        Args:
            filepath: path to a ``.py`` or ``.pic.yml`` file.

        Returns:
            The component parsed from the file, or None.
        """
        import pygit2

        from gdsfactory.get_factories import get_cells_from_dict

        try:
            repo = pygit2.Repository(cwd)
            dirpath_str = repo.workdir or repo.path
        except pygit2.GitError:
            dirpath_str = str(cwd)

        try:
            filepath = pathlib.Path(filepath)
            dirpath = pathlib.Path(dirpath_str) / "build" / "gds"
            dirpath.mkdir(parents=True, exist_ok=True)

            gitignore_path = pathlib.Path(dirpath_str) / "build" / ".gitignore"
            if not gitignore_path.exists():
                gitignore_path.write_text("*\n")

            if filepath.exists():
                if str(filepath).endswith(".pic.yml"):
                    return self.get_component_yaml(filepath, dirpath)
                if str(filepath).endswith(".py"):
                    if not self._is_allowed_path(filepath):
                        self.logger.error(
                            "Rejected file %s: not in allowed directories",
                            filepath,
                        )
                        return None

                    self.logger.warning("Executing Python file: %s", filepath.resolve())

                    context = dict(locals(), **globals())
                    if self.run_main:
                        context.update(__name__="__main__")

                    try:
                        exec(filepath.read_text(), context, context)
                    except SyntaxError:
                        self.logger.exception("Syntax error in %s", filepath)
                        return None
                    except Exception:
                        self.logger.exception("Error executing %s", filepath)
                        return None

                    if self.run_cells:
                        cells = get_cells_from_dict(context)
                        for name, cell in cells.items():
                            c = cell()
                            gdspath = dirpath / f"{name}.gds"
                            c.write_gds(gdspath)
                            kf.show(gdspath)

                else:
                    print(f"Changed file {filepath} ignored (not .pic.yml or .py)")

        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            print(e)
        return None

    def get_component_yaml(self, filepath: PathType, dirpath: PathType) -> Component:
        """Parses a YAML file to a cell function and registers into active pdk."""
        cell_func = self.update_cell(filepath, update=True)
        filepath_path = pathlib.Path(filepath)
        c = cell_func()
        gdspath = pathlib.Path(dirpath) / str(
            filepath_path.relative_to(self.path)
        ).replace(".pic.yml", ".gds")
        c.write_gds(gdspath)
        kf.show(gdspath)
        return c


def watch(
    path: PathType | None = cwd,
    pdk: Pdk | str | None = None,
    run_main: bool = True,
    run_cells: bool = True,
    pre_run: bool = False,
    logger: logging.Logger | None = None,
    run_embed: bool = True,
    allowed_dirs: list[PathType] | None = None,
) -> None:
    pass


def show(component: ComponentSpec) -> None:
    """Shows a component in klayout."""
    import gdsfactory as gf

    c = gf.get_component(component)
    c.show()
