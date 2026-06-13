# =====================================
# generator=datazen
# version=3.2.4
# hash=3538e0b7fa49298836a10350f8149749
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
    ],
}
setup(
    pkg_info,
    author_info,
)
