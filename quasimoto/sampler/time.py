"""
A module implementing a simple time-keeper interface.
"""

# built-in
from copy import copy
from typing import Callable, TypeVar

# internal
from quasimoto.wave.writer import DEFAULT_SAMPLE_RATE

T = TypeVar("T", bound="TimeKeeper")

TimeCallback = Callable[[float], None]


class PeriodMixin:
    """
    A simple class mixin for other classes that have a time-period component.
    """

    def __init__(self, sample_rate: int = DEFAULT_SAMPLE_RATE) -> None:
        """Initialize this instance."""

        # Constants / final.
        self.sample_rate = sample_rate
        self.period = 1.0 / self.sample_rate

    def sample_number(self, time: float) -> int:
        """Determine the sample number that the given time starts."""
        return int(time / self.period)

    def num_samples(self, duration_s: float) -> int:
        """Get the number of samples for a specified amount of time."""
        return int(duration_s * self.sample_rate)


class TimeKeeper(PeriodMixin):
    """A class for keeping time."""

    def __init__(
        self, time: float = 0.0, sample_rate: int = DEFAULT_SAMPLE_RATE
    ) -> None:
        """Initialize this instance."""

        super().__init__(sample_rate=sample_rate)
        self.time = time

        self.iteration: int = self.sample_number(self.time)

        self.callbacks: dict[int, list[TimeCallback]] = {}

    def call_at(self, time: float, callback: TimeCallback) -> None:
        """Register a callback that runs at the specified time."""

        assert time > self.time, time

        index = self.num_samples(time)
        if index not in self.callbacks:
            self.callbacks[index] = []
        self.callbacks[index].append(callback)

    def call_in(self, time: float, callback: TimeCallback) -> float:
        """
        Register a callback for some relative amount of time in the future.
        """

        call_time = self.time + time
        self.call_at(self.time + time, callback)
        return call_time

    def call_sequence(self, *callbacks: tuple[float, TimeCallback]) -> None:
        """Register a call sequence."""

        curr = self.time
        for offset, callback in callbacks:
            self.call_at(curr + offset, callback)
            curr += offset

    def advance(self) -> None:
        """Advance time forward."""

        self.time += self.period
        self.iteration += 1

        # Check for callbacks.
        callbacks = self.callbacks.get(self.iteration)
        if callbacks:
            for callback in callbacks:
                callback(self.time)
            del self.callbacks[self.iteration]

    def __copy__(self: T) -> T:
        """Get a copy of this instance."""

        result = type(self)(time=self.time, sample_rate=self.sample_rate)

        result.callbacks = copy(self.callbacks)

        return result

    def copy(self: T) -> T:
        """Get a copy of this instance."""
        return copy(self)
