"""
A module implementing sampler interfaces.
"""

# built-in
from collections.abc import Iterable, Iterator
from copy import copy
import math
from typing import TypeVar

# internal
from quasimoto.wave.writer import DEFAULT_BITS, DEFAULT_SAMPLE_RATE

DEFAULT_FREQUENCY = 261.63
T = TypeVar("T", bound="Sampler")


class Sampler(Iterable[int]):
    """A base class for iterable sampler interfaces."""

    def __init__(
        self,
        num_bits: int = DEFAULT_BITS,
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        duration_s: float = None,
        frequency: float = DEFAULT_FREQUENCY,
        time: float = 0.0,
    ) -> None:
        """Initialize this instance."""

        # Can be changed after initialization.
        self.frequency = frequency
        self.duration_s = duration_s

        # Constants / final.
        self.sample_rate = sample_rate
        self.period = 1.0 / self.sample_rate
        self.time = time

        # Note: this assumed signed + zero-centered.
        self.num_bits = num_bits
        self.scalar = (2 ** (self.num_bits - 1)) - 1

    def __copy__(self: T) -> T:
        """Create a copy of this instance."""

        return type(self)(
            num_bits=self.num_bits,
            sample_rate=self.sample_rate,
            duration_s=self.duration_s,
            frequency=self.frequency,
            time=self.time,
        )

    def copy(self: T, harmonic: int = None, duration_s: float = None) -> T:
        """Get a copy of this instance."""

        result = copy(self)

        if duration_s is not None:
            result.duration_s = duration_s
        if harmonic is not None:
            result.frequency = float(2**harmonic) * self.frequency

        return result

    def advance(self, steps: int = 1) -> bool:
        """Advance time forward."""

        result = True

        for _ in range(steps):
            self.time += self.period
            if self.duration_s is not None:
                result = self.time < self.duration_s

        return result

    def sin(self, now: float) -> int:
        """Get a raw sin value sample."""
        return int(self.scalar * math.sin(math.tau * now * self.frequency))

    def value(self, now: float) -> int:
        """Get the next value."""
        return self.sin(now)

    def __iter__(self) -> Iterator[int]:
        """Return an iterator."""
        return self

    def __next__(self) -> int:
        """Get the next value from this sampler."""

        val: int = self.value(self.time)

        if not self.advance():
            raise StopIteration

        return val
