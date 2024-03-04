"""
A module implementing a simple time-keeper interface.
"""

# built-in
from copy import copy
from typing import TypeVar

# internal
from quasimoto.wave.writer import DEFAULT_SAMPLE_RATE

T = TypeVar("T", bound="TimeKeeper")


class TimeKeeper:
    """A class for keeping time."""

    def __init__(
        self, time: float = 0.0, sample_rate: int = DEFAULT_SAMPLE_RATE
    ) -> None:
        """Initialize this instance."""

        self.time = time

        # Constants / final.
        self.sample_rate = sample_rate
        self.period = 1.0 / self.sample_rate

    def num_samples(self, duration_s: float) -> int:
        """Get the number of samples for a specified amount of time."""
        return int(duration_s * self.sample_rate)

    def advance(self) -> None:
        """Advance time forward."""
        self.time += self.period

    def __copy__(self: T) -> T:
        """Get a copy of this instance."""
        return type(self)(time=self.time, sample_rate=self.sample_rate)

    def copy(self: T) -> T:
        """Get a copy of this instance."""
        return copy(self)
