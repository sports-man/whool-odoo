from pathlib import Path
from tarfile import TarFile

from wodoo.buildapi import _build_sdist


def test_build_sdist(data_path: Path, tmp_path: Path) -> None:
    sdist_name = _build_sdist(data_path / "addon_1", tmp_path)
    assert sdist_name == "odoo12-addon-addon_1-12.0.1.0.0.tar.gz"
    assert (tmp_path / sdist_name).exists()


def test_build_sdist_from_sdist(data_path: Path, tmp_path: Path) -> None:
    sdist_name = _build_sdist(data_path / "addon_1", tmp_path)
    assert sdist_name == "odoo12-addon-addon_1-12.0.1.0.0.tar.gz"
    # extract sdist and test that the root directory has the correct name
    tmp_path2 = tmp_path / "2"
    tmp_path2.mkdir()
    with TarFile.open(tmp_path / sdist_name, mode="r:gz") as tf1:
        tf1_names = sorted(tf1.getnames())
        tf1.extractall(tmp_path2)
    assert "odoo12-addon-addon_1-12.0.1.0.0/PKG-INFO" in tf1_names
    assert "odoo12-addon-addon_1-12.0.1.0.0/pyproject.toml" in tf1_names
    # build sdist from sdist
    tmp_path3 = tmp_path / "3"
    tmp_path3.mkdir()
    sdist_name = _build_sdist(tmp_path2 / "odoo12-addon-addon_1-12.0.1.0.0", tmp_path3)
    assert sdist_name == "odoo12-addon-addon_1-12.0.1.0.0.tar.gz"
    # extract 2nd sdist and test that the root directory has the correct name
    with TarFile.open(tmp_path3 / sdist_name, mode="r:gz") as tf2:
        tf2_names = sorted(tf2.getnames())
        tf2.extractall(tmp_path3)
    # content of both sdists must be identical
    assert tf1_names == tf2_names
    # PKG-INFO in both sdists must be identical
    assert (
        tmp_path2 / "odoo12-addon-addon_1-12.0.1.0.0" / "PKG-INFO"
    ).read_bytes() == (
        tmp_path3 / "odoo12-addon-addon_1-12.0.1.0.0" / "PKG-INFO"
    ).read_bytes()
