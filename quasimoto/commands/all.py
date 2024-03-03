# =====================================
# generator=datazen
# version=3.1.4
# hash=b8d2bc2e3ccbd1d7eab451040c2edb8e
# =====================================

"""
A module aggregating package commands.
"""

# built-in
from typing import List as _List
from typing import Tuple as _Tuple

# third-party
from vcorelib.args import CommandRegister as _CommandRegister

# internal
from quasimoto.commands.gen import add_gen_cmd


def commands() -> _List[_Tuple[str, str, _CommandRegister]]:
    """Get this package's commands."""

    return [
        (
            "gen",
            "generate audio",
            add_gen_cmd,
        ),
        ("noop", "command stub (does nothing)", lambda _: lambda _: 0),
    ]
