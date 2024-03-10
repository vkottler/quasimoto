"""
A module implementing a sound-source interface base class.
"""

# built-in
from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from copy import copy
from pathlib import Path
from typing import Any, Callable, TypeVar

# third-party
import matplotlib.pyplot as plt
from runtimepy.primitives import Double

# internal
from quasimoto.sampler.frequency import HasFrequencyMixin
from quasimoto.sampler.parameters import DEFAULT, SourceParameters
from quasimoto.sampler.time import TimeKeeper
from quasimoto.wave.writer import WaveWriter

T = TypeVar("T", bound="SourceInterface")
DEFAULT_AMPLITUDE = 1.0


class SourceInterface(HasFrequencyMixin, Iterable[int], ABC):
    """A class implementing a sound-source interface."""

    def __init__(
        self, time_keeper: TimeKeeper, params: SourceParameters = DEFAULT
    ) -> None:
        """Initialize this instance."""

        self.time_keeper = time_keeper
        self.params = params
        super().__init__(
            frequency=self.params.frequency, shape=self.params.shape
        )

        self.stop_time = self.params.stop_time
        self.set_duration(self.params.duration)

        # Amplitude should be applied by the iterator/caller.
        self.enabled.value = params.enabled
        self.amplitude = Double(value=self.params.amplitude)

        def _enable_event(_: float) -> None:
            """A simple method for enabling this source."""
            self.enabled.value = True

        self.enable_event = _enable_event

        def _disable_event(_: float) -> None:
            """A simple method for disabling this source."""
            self.enabled.value = False

        self.disable_event = _disable_event

    def set_duration(self, duration: float = None) -> None:
        """Set a duration for this source."""

        if duration is not None:
            self.stop_time = self.time_keeper.time + duration

    def __iter__(self) -> Iterator[int]:
        """Return an iterator."""
        return self

    @abstractmethod
    def __copy__(self: T) -> T:
        """Create a copy of this instance."""

    def copy(self: T) -> T:
        """Create a copy of this instance."""
        return copy(self)

    def clone(self: T, harmonic: int = None, stop_time: float = None) -> T:
        """Get a copy of this instance."""

        result = self.copy()

        if stop_time is not None:
            result.stop_time = stop_time
        if harmonic is not None:
            result.frequency.value = result.harmonic(harmonic)

        return result

    @abstractmethod
    def value(self, now: float) -> int:
        """Get the next value."""

    @classmethod
    def create(
        cls: type[T], time_keeper: TimeKeeper, data: dict[str, Any] = None
    ) -> T:
        """Create a source instance from dictionary data."""

        return cls(
            time_keeper,
            params=SourceParameters.from_dict(data)
            if data is not None
            else DEFAULT,
        )

    def __next__(self) -> int:
        """Get the next value from this sampler."""

        # Determine if we should stop.
        if (
            self.stop_time is not None
            and self.time_keeper.time >= self.stop_time
        ):
            raise StopIteration

        return self.value(self.time_keeper.time)

    def sample_for(
        self, duration_s: float, handler: Callable[[int], None]
    ) -> None:
        """Sample this source for the specified duration."""

        # Copy self and our time keeper to create equivalent but independent
        # results.
        inst = self.copy()
        inst.time_keeper = self.time_keeper.copy()

        for _ in range(inst.time_keeper.num_samples(duration_s)):
            handler(next(inst))
            inst.time_keeper.advance()

    def get_samples(self, duration_s: float) -> list[int]:
        """Collect samples."""
        data: list[int] = []
        self.sample_for(duration_s, data.append)
        return data

    def plot(self, path: Path | str, duration_s: float) -> None:
        """Create a plot."""

        # Plot data.
        plt.plot(self.get_samples(duration_s))
        plt.savefig(str(path), bbox_inches="tight")

    def to_wave(self, path: Path, duration_s: float) -> None:
        """Write this source to a wave file."""

        with WaveWriter.from_path(path) as writer:
            writer.write([(x, x) for x in self.get_samples(duration_s)])
