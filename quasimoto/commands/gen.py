"""
An entry-point for the 'gen' command.
"""

# built-in
import argparse
from enum import StrEnum
from pathlib import Path

# third-party
from vcorelib.args import CommandFunction

# internal
from quasimoto import PKG_NAME


class AudioFileTypes(StrEnum):
    """An enumeration for supported file types."""

    WAVE = "wav"


DEFAULT_FORMAT = AudioFileTypes.WAVE


def gen_cmd(args: argparse.Namespace) -> int:
    """Execute the arbiter command."""

    with args.output.open("wb") as out_fd:
        print(out_fd)

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
