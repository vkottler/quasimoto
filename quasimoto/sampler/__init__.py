"""
A module implementing sampler interfaces.
"""

# built-in
from collections.abc import Iterable, Iterator
from copy import copy
from pathlib import Path
from typing import TypeVar, cast

# third-party
import matplotlib.pyplot as plt
from runtimepy.primitives import Double, create

# internal
from quasimoto.enums.wave import WaveShape
from quasimoto.sampler.frequency import DEFAULT_FREQUENCY, HasFrequencyMixin
from quasimoto.sampler.time import TimeKeeper
from quasimoto.wave.writer import DEFAULT_BITS

T = TypeVar("T", bound="Sampler")


class Sampler(HasFrequencyMixin, Iterable[int]):
    """A base class for iterable sampler interfaces."""

    def __init__(
        self,
        time_keeper: TimeKeeper,
        num_bits: int = DEFAULT_BITS,
        stop_time: float = None,
        frequency: float = DEFAULT_FREQUENCY,
        amplitude: float = 1.0,
        shape: WaveShape | int = WaveShape.SINE,
    ) -> None:
        """Initialize this instance."""

        self.time_keeper = time_keeper

        # Can be changed after initialization.
        super().__init__(frequency=frequency)
        self.amplitude = Double(value=amplitude)
        self.stop_time = stop_time

        self.shape = create(WaveShape.primitive())
        self.shape.value = shape

        # Note: this assumed signed + zero-centered.
        self.num_bits = num_bits
        self.scalar = (2 ** (self.num_bits - 1)) - 1

    def __copy__(self: T) -> T:
        """Create a copy of this instance."""

        return type(self)(
            self.time_keeper,
            num_bits=self.num_bits,
            stop_time=self.stop_time,
            frequency=self.frequency.value,
            amplitude=self.amplitude.value,
            shape=cast(int, self.shape.value),
        )

    def copy(self: T, harmonic: int = None, stop_time: float = None) -> T:
        """Get a copy of this instance."""

        result = copy(self)

        if stop_time is not None:
            result.stop_time = stop_time
        if harmonic is not None:
            result.frequency.value = result.harmonic(harmonic)

        return result

    def value(self, now: float) -> int:
        """Get the next value."""

        # Select underlying wave generator.
        return int(
            self.scalar
            * self.amplitude.value
            * self.by_shape[self.shape.value](now)  # type: ignore
        )

    def __iter__(self) -> Iterator[int]:
        """Return an iterator."""
        return self

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
        inst = self.copy()
        inst.time_keeper = self.time_keeper.copy()

        data = []
        for _ in range(inst.time_keeper.num_samples(duration_s)):
            data.append(next(inst))
            inst.time_keeper.advance()

        plt.plot(data)
        plt.savefig(str(path), bbox_inches="tight")
