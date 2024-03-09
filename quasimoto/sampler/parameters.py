"""
A module implementing a sampler-creation-parameter interface.
"""

# built-in
from typing import Any, NamedTuple, Optional

# internal
from quasimoto.enums.wave import WaveShape
from quasimoto.sampler.notes import DEFAULT_FREQUENCY, Note

DEFAULT_AMPLITUDE = 1.0
DEFAULT_SHAPE = WaveShape.SINE


class SourceParameters(NamedTuple):
    """A container for parameters used to instantiate sources."""

    stop_time: Optional[float] = None
    duration: Optional[float] = None
    frequency: float = DEFAULT_FREQUENCY
    amplitude: float = DEFAULT_AMPLITUDE
    shape: WaveShape = DEFAULT_SHAPE
    enabled: bool = True

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "SourceParameters":
        """Get source parameters from dictionary data."""

        return SourceParameters(
            stop_time=data.get("stop_time"),
            duration=data.get("duration"),
            frequency=data.get("frequency", DEFAULT_FREQUENCY),
            amplitude=data.get("amplitude", DEFAULT_AMPLITUDE),
            shape=WaveShape.normalize(data.get("shape", DEFAULT_SHAPE)),
        )

    @staticmethod
    def from_note(
        note: Note, octave_offset: int = 0, **kwargs
    ) -> "SourceParameters":
        """Create parameters from a given note."""

        return SourceParameters.from_dict(
            {
                **kwargs,
                "frequency": note.frequency(octave_offset=octave_offset),
            }
        )

    @staticmethod
    def from_index(index: int, **kwargs) -> "SourceParameters":
        """Create source parameters from a note index."""
        note, offset = Note.from_index(index)
        return SourceParameters.from_note(note, octave_offset=offset, **kwargs)


DEFAULT = SourceParameters()
