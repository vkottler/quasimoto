"""
A module implementing sampler interfaces.
"""

# internal
from quasimoto.sampler.source import DEFAULT, SourceInterface, SourceParameters
from quasimoto.sampler.time import TimeKeeper
from quasimoto.wave.writer import DEFAULT_BITS


class Sampler(SourceInterface):
    """A base class for iterable sampler interfaces."""

    def __init__(
        self,
        time_keeper: TimeKeeper,
        params: SourceParameters = DEFAULT,
        num_bits: int = DEFAULT_BITS,
    ) -> None:
        """Initialize this instance."""

        super().__init__(time_keeper, params=params)

        # Note: this assumed signed + zero-centered.
        self.num_bits = num_bits
        self.scalar = (2 ** (self.num_bits - 1)) - 1

    def __copy__(self) -> "Sampler":
        """Create a copy of this instance."""

        return type(self)(
            self.time_keeper, params=self.params, num_bits=self.num_bits
        )

    def value(self, now: float) -> int:
        """Get the next value."""

        # Select underlying wave generator.
        return int(
            self.scalar * self.by_shape[self.shape.value](now)  # type: ignore
        )
