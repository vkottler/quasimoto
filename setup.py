# =====================================
# generator=datazen
# version=3.2.4
# hash=18c61bc1f595b37f5bffe0cf746362c6
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
    "name": "Libre Embedded",
    "email": "vaughn@libre-embedded.com",
    "username": "libre-embedded",
}
pkg_info = {
    "name": PKG_NAME,
    "slug": PKG_NAME.replace("-", "_"),
    "version": VERSION,
    "description": DESCRIPTION,
    "versions": [
        "3.13",
        "3.14",
        "3.11",
        "3.12",
    ],
}
setup(
    pkg_info,
    author_info,
)
