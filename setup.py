# =====================================
# generator=datazen
# version=3.1.4
# hash=372222f3f6b266691437ff06877b630c
# =====================================

"""
quasimoto - Package definition for distribution.
"""

# third-party
try:
    from setuptools_wrapper.setup import setup
except (ImportError, ModuleNotFoundError):
    from quasimoto_bootstrap.setup import setup  # type: ignore

# internal
from quasimoto import DESCRIPTION, PKG_NAME, VERSION

author_info = {
    "name": "Vaughn Kottler",
    "email": "vaughnkottler@gmail.com",
    "username": "vkottler",
}
pkg_info = {
    "name": PKG_NAME,
    "slug": PKG_NAME.replace("-", "_"),
    "version": VERSION,
    "description": DESCRIPTION,
    "versions": [
        "3.11",
        "3.12",
    ],
}
setup(
    pkg_info,
    author_info,
)
