"""
A module implementing a RIFF-chunk interface.
"""

# built-in
from typing import NamedTuple, Optional

# internal
from quasimoto.enums import ChunkType


class Chunk(NamedTuple):
    """A container for chunk data."""

    kind: ChunkType
    size: int
    data: Optional[bytes] = None
    form: Optional[ChunkType] = None

    def __str__(self) -> str:
        """Get this chunk as a string."""
        result = f"'{self.kind}' size={self.size}"

        if self.form is not None:
            result += f" (form='{self.form}')"

        return result


NULL_BYTE = "\0".encode()
