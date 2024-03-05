"""
A module implementing sampler interfaces.
"""

# built-in
from copy import copy
from typing import cast

# third-party
from runtimepy.primitives import create

# internal
from quasimoto.enums.wave import WaveShape
from quasimoto.sampler.frequency import DEFAULT_FREQUENCY
from quasimoto.sampler.source import DEFAULT_AMPLITUDE, SourceInterface
from quasimoto.sampler.time import TimeKeeper
from quasimoto.wave.writer import DEFAULT_BITS


class Sampler(SourceInterface):
    """A base class for iterable sampler interfaces."""

    def __init__(
        self,
        time_keeper: TimeKeeper,
        num_bits: int = DEFAULT_BITS,
        stop_time: float = None,
        frequency: float = DEFAULT_FREQUENCY,
        amplitude: float = DEFAULT_AMPLITUDE,
        shape: WaveShape | int = WaveShape.SINE,
    ) -> None:
        """Initialize this instance."""

        super().__init__(
            time_keeper,
            stop_time=stop_time,
            frequency=frequency,
            amplitude=amplitude,
        )

        # Can be changed after initialization.
        self.shape = create(WaveShape.primitive())
        self.shape.value = shape

        # Note: this assumed signed + zero-centered.
        self.num_bits = num_bits
        self.scalar = (2 ** (self.num_bits - 1)) - 1

    def next_shape(self) -> None:
        """Increment to the next shape."""
        self.shape.value = 1 + (int(self.shape.value) % 4)

    def __copy__(self) -> "Sampler":
        """Create a copy of this instance."""

        return type(self)(
            self.time_keeper,
            num_bits=self.num_bits,
            stop_time=self.stop_time,
            frequency=self.frequency.value,
            amplitude=self.amplitude.value,
            shape=cast(int, self.shape.value),
        )

    def copy(self, harmonic: int = None, stop_time: float = None) -> "Sampler":
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
            self.scalar * self.by_shape[self.shape.value](now)  # type: ignore
        )
