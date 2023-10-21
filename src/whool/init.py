import logging
from pathlib import Path
from typing import Sequence

from manifestoo_core.addon import is_addon_dir

from .compat import tomllib

_logger = logging.getLogger(__name__)

BUILD_SYSTEM_TOML = b"""\
[build-system]
requires = ["whool"]
build-backend = "whool.buildapi"
"""


def init_addon_dir(addon_dir: Path) -> bool:
    modified = False
    pyproject_toml_path = addon_dir / "pyproject.toml"
    if not pyproject_toml_path.exists():
        # create pyproject.toml
        with open(pyproject_toml_path, "wb") as f:
            f.write(BUILD_SYSTEM_TOML)
        modified = True
    else:
        with open(pyproject_toml_path, "rb") as f:
            pyproject_toml = tomllib.load(f)
        if "build-system" not in pyproject_toml:
            # no build-system in existing pyproject.toml, add one
            with open(pyproject_toml_path, "ab") as f:
                f.write(b"\n")
                f.write(BUILD_SYSTEM_TOML)
            modified = True
    return modified


def init(dir: Path) -> Sequence[Path]:
    res = []
    if is_addon_dir(dir):
        if init_addon_dir(dir):
            res.append(dir)
    else:
        for subdir in dir.iterdir():
            if subdir.is_dir():
                if is_addon_dir(subdir):
                    if init_addon_dir(subdir):
                        res.append(subdir)
    return res
