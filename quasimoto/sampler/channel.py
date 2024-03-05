"""
A module implementing a signal channel.
"""

# built-in
from copy import copy
from typing import NamedTuple

# internal
from quasimoto.sampler.frequency import DEFAULT_FREQUENCY
from quasimoto.sampler.source import SourceInterface
from quasimoto.sampler.time import TimeKeeper


class SignalOperationResult(NamedTuple):
    """A container for information about results of signal operations."""

    status: bool
    message: str = ""

    def __bool__(self) -> bool:
        """Get this instance as a boolean."""
        return self.status


SUCCESS = SignalOperationResult(True)


class SignalChannel(SourceInterface):
    """
    A signal channel that allows an arbitrary number of sources to contribute
    to it.
    """

    def __init__(
        self,
        time_keeper: TimeKeeper,
        stop_time: float = None,
        frequency: float = DEFAULT_FREQUENCY,
    ) -> None:
        """Initialize this instance."""

        super().__init__(time_keeper, stop_time=stop_time, frequency=frequency)
        self.sources: dict[str, SourceInterface] = {}

    def value(self, now: float) -> int:
        """Get the next value."""

        # We enforce that all managed sources use the same time keeper as us,
        # though we do not use the time data ourselves to compute anything.
        del now

        value = 0.0
        contributors = 0
        to_remove = []

        # Sample all sources.
        for name, source in self.sources.items():
            raw = next(source, None)
            if raw is not None:
                contributors += 1

                # Apply source-specific amplitudes here.
                value += raw * source.amplitude.value
            else:
                to_remove.append(name)

        # Weigh each signal source equally by dividing the final result by
        # the number of contributing sources.
        if contributors > 1:
            value /= contributors

        # Apply our amplitude.
        value *= self.amplitude.value

        for name in to_remove:
            assert self.remove_source(name), name

        return int(value)

    def __copy__(self) -> "SignalChannel":
        """Create a copy of this instance."""

        result = SignalChannel(self.time_keeper)
        result.sources = copy(self.sources)
        return result

    def register_source(
        self, name: str, source: SourceInterface
    ) -> SignalOperationResult:
        """Attempt to register a signal source."""

        result = SUCCESS

        if name in self.sources:
            result = SignalOperationResult(
                False, f"Duplicate source '{name}'."
            )
        elif source.time_keeper is not self.time_keeper:
            result = SignalOperationResult(
                False, "Sources use different time keepers!"
            )
        else:
            self.sources[name] = source

        return result

    def remove_source(self, name: str) -> SignalOperationResult:
        """Attempt to register a signal source."""

        result = SUCCESS

        if name not in self.sources:
            result = SignalOperationResult(False, f"No source '{name}'.")
        else:
            del self.sources[name]

        return result
