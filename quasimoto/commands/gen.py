"""
An entry-point for the 'gen' command.
"""

# built-in
import argparse
from pathlib import Path

# third-party
from vcorelib.args import CommandFunction

# internal
from quasimoto import PKG_NAME
from quasimoto.enums import DEFAULT_FORMAT
from quasimoto.riff import RiffInterface


def gen_cmd(args: argparse.Namespace) -> int:
    """Execute the arbiter command."""

    with RiffInterface.from_path(args.output) as writer:
        print(writer)

    return 0


def add_gen_cmd(parser: argparse.ArgumentParser) -> CommandFunction:
    """Add gen-command arguments to its parser."""

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=f"{PKG_NAME}.{DEFAULT_FORMAT}",
        help="output file to write",
    )

    return gen_cmd
