"""
A module implementing a simple frequency interface class.
"""

# built-in
import math
from typing import Callable

# third-party
from runtimepy.primitives import Double, create

# internal
from quasimoto.enums.wave import WaveShape, WaveShapelike
from quasimoto.sampler.notes import DEFAULT_FREQUENCY


class HasFrequencyMixin:
    """A simple mixin class for classes that have some frequency component."""

    def __init__(
        self,
        frequency: float = DEFAULT_FREQUENCY,
        shape: WaveShapelike = WaveShape.SINE,
    ) -> None:
        """Initialize this instance."""

        # Can be changed after initialization.
        self.shape = create(WaveShape.primitive())
        self.shape.value = WaveShape.normalize(shape)
        self.frequency = Double(value=frequency)

        self.by_shape: dict[int, Callable[[float], float]] = {
            WaveShape.SINE: self.sin,
            WaveShape.TRIANGLE: self.triangle,
            WaveShape.SQUARE: self.square,
            WaveShape.SAWTOOTH: self.sawtooth,
        }

    def next_shape(self) -> None:
        """Increment to the next shape."""
        self.shape.value = 1 + (int(self.shape.value) % 4)

    def harmonic(self, index: int) -> float:
        """Get a harmonic frequency based on this instance's frequency."""
        return float(2**index) * self.frequency.value

    def sin(self, now: float) -> float:
        """Get a raw sin-wave value sample."""
        return math.sin(math.tau * now * self.frequency.value)

    def period(self) -> float:
        """Obtain the period for this frequency."""
        return 1.0 / self.frequency.value

    def quantize_to_period(self, time: float) -> float:
        """Return time extended to the next start-of-period."""
        period = self.period()
        return time + (period - divmod(time, period)[1])

    def triangle(self, now: float) -> float:
        """Get a raw triangle-wave value sample."""

        period = self.period()

        return (
            (4.0 / period)
            * abs(((now - period / 4.0) % period) - (period / 2.0))
        ) - 1.0

    def square(self, now: float) -> float:
        """Get a raw square-wave value sample."""

        step = self.frequency.value * now
        return 2 * (2 * math.floor(step) - math.floor(2 * step)) + 1

    def sawtooth(self, now: float) -> float:
        """Get a raw sawtooth-wave value sample."""

        phase = now / self.period()
        return 2.0 * (phase - math.floor(0.5 + phase))
