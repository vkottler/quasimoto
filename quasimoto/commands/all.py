# =====================================
# generator=datazen
# version=3.2.4
# hash=749efda4399fce4d27bf9ba7f63ca7a4
# =====================================

"""
A module aggregating package commands.
"""

# third-party
from vcorelib.args import CommandRegister as _CommandRegister

# internal
from quasimoto.commands.gen import add_gen_cmd


def commands() -> list[tuple[str, str, _CommandRegister]]:
    """Get this package's commands."""

    return [
        (
            "gen",
            "generate audio",
            add_gen_cmd,
        ),
        ("noop", "command stub (does nothing)", lambda _: lambda _: 0),
    ]
