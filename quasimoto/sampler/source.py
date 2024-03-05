"""
A module implementing a sound-source interface base class.
"""

# built-in
from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from copy import copy
from pathlib import Path
from typing import TypeVar

# third-party
import matplotlib.pyplot as plt
from runtimepy.primitives import Double

# internal
from quasimoto.sampler.frequency import DEFAULT_FREQUENCY, HasFrequencyMixin
from quasimoto.sampler.time import TimeKeeper

T = TypeVar("T", bound="SourceInterface")
DEFAULT_AMPLITUDE = 1.0


class SourceInterface(HasFrequencyMixin, Iterable[int], ABC):
    """A class implementing a sound-source interface."""

    def __init__(
        self,
        time_keeper: TimeKeeper,
        stop_time: float = None,
        frequency: float = DEFAULT_FREQUENCY,
        amplitude: float = DEFAULT_AMPLITUDE,
    ) -> None:
        """Initialize this instance."""

        self.time_keeper = time_keeper
        super().__init__(frequency=frequency)
        self.stop_time = stop_time

        # Amplitude should be applied by the iterator/caller.
        self.amplitude = Double(value=amplitude)

    def __iter__(self) -> Iterator[int]:
        """Return an iterator."""
        return self

    @abstractmethod
    def __copy__(self: T) -> T:
        """Create a copy of this instance."""

    @abstractmethod
    def value(self, now: float) -> int:
        """Get the next value."""

    def __next__(self) -> int:
        """Get the next value from this sampler."""

        # Determine if we should stop.
        if (
            self.stop_time is not None
            and self.time_keeper.time >= self.stop_time
        ):
            raise StopIteration

        return self.value(self.time_keeper.time)

    def plot(self, path: Path | str, duration_s: float) -> None:
        """Create a ."""

        # Copy self and our time keeper to create equivalent but independent
        # results.
        inst = copy(self)
        inst.time_keeper = self.time_keeper.copy()

        data = []
        for _ in range(inst.time_keeper.num_samples(duration_s)):
            data.append(next(inst))
            inst.time_keeper.advance()

        plt.plot(data)
        plt.savefig(str(path), bbox_inches="tight")
