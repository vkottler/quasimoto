"""
Test the 'commands.gen' module.
"""

# third-party
from vcorelib.paths.context import tempfile

# module under test
from quasimoto import PKG_NAME
from quasimoto.entry import main as package_main


def test_gen_command_basic():
    """Test basic usages of the 'gen' command."""

    with tempfile() as tmp:
        assert package_main([PKG_NAME, "gen", "-o", str(tmp)]) == 0
