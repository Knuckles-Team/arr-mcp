"""Verify package initialization and version metadata."""

import importlib

import pytest

PKG_NAME = __name__.rsplit(".", 1)[0] if "." in __name__ else None


def _get_pkg_name():
    """Discover the importable package by scanning the project for the package
    directory (one holding ``__init__.py`` plus the server entrypoint), rather
    than assuming it matches the project folder name — the folder differs from
    the package in git worktrees (e.g. ``harden-discovery`` vs ``arr_mcp``)."""
    import pathlib

    project_dir = pathlib.Path(__file__).resolve().parent.parent
    for child in sorted(project_dir.iterdir()):
        if not child.is_dir() or child.name in {"tests", "scripts"}:
            continue
        if child.name.startswith((".", "_")):
            continue
        if (child / "__init__.py").exists() and (
            (child / "mcp_server.py").exists() or (child / "__main__.py").exists()
        ):
            return child.name
    # Fallback: the old directory-name heuristic.
    return project_dir.name.replace("-", "_")


@pytest.fixture
def pkg_name():
    return _get_pkg_name()


def test_package_importable(pkg_name):
    """Package should be importable."""
    mod = importlib.import_module(pkg_name)
    assert mod is not None


def test_version_exists(pkg_name):
    """Package should expose __version__."""
    mod = importlib.import_module(pkg_name)
    version = getattr(mod, "__version__", None)
    # Version may come from importlib.metadata instead
    if version is None:
        from importlib.metadata import version as get_version

        version = get_version(pkg_name.replace("_", "-"))
    assert version is not None, f"{pkg_name} has no __version__"


def test_version_format(pkg_name):
    """Version should follow semver-like format."""
    mod = importlib.import_module(pkg_name)
    version = getattr(mod, "__version__", None)
    if version is None:
        from importlib.metadata import version as get_version

        version = get_version(pkg_name.replace("_", "-"))
    parts = version.split(".")
    assert len(parts) >= 2, f"Version {version} should have at least major.minor"
