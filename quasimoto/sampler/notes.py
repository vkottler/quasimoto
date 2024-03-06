"""
A module implementing an interface to musical notes.
"""

# third-party
from runtimepy.enum.registry import RuntimeIntEnum

TWELVE_TONE_EQUAL: float = 2 ** (1 / 12)

ROOT_FREQUENCY = 8.175799


def note_by_index(index: int) -> float:
    """
    Get the frequency of a note based on its index from the root (lowest)
    frequency.
    """
    assert index >= 0
    return TWELVE_TONE_EQUAL**index * ROOT_FREQUENCY


# Start 5 octaves above the root note by default (middle C).
OCTAVE_BASE = 5


class Note(RuntimeIntEnum):
    """An enumeration interface for notes."""

    C = 0

    CS = 1
    DB = 1

    D = 2

    DS = 3
    EB = 3

    E = 4
    F = 5

    FS = 6
    GB = 6

    G = 7

    GS = 8
    AB = 8

    A = 9

    AS = 10
    BB = 10

    B = 11

    def frequency(self, octave_offset: int = 0) -> float:
        """Get the frequency of a note."""
        return note_by_index(12 * (OCTAVE_BASE + octave_offset) + self)


DEFAULT_FREQUENCY: float = Note.C.frequency()
