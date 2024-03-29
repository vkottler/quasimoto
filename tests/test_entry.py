"""
quasimoto - Test the program's entry-point.
"""

# built-in
from subprocess import check_output
from sys import executable
from unittest.mock import patch

# module under test
from quasimoto import PKG_NAME
from quasimoto.entry import main as quasimoto_main


def test_entry_basic():
    """Test basic argument parsing."""

    args = [PKG_NAME, "noop"]
    assert quasimoto_main(args) == 0

    with patch("quasimoto.entry.entry", side_effect=SystemExit(1)):
        assert quasimoto_main(args) != 0


def test_package_entry():
    """Test the command-line entry through the 'python -m' invocation."""

    check_output([executable, "-m", "quasimoto", "-h"])
