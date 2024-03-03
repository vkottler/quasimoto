"""
A module implementing enumeration interfaces for this package.
"""

# built-in
from enum import StrEnum
from typing import BinaryIO, Optional


class AudioFileTypes(StrEnum):
    """An enumeration for supported file types."""

    WAVE = "wav"


DEFAULT_FORMAT = AudioFileTypes.WAVE


class ChunkType(StrEnum):
    """An enumeration for different kinds of RIFF chunks."""

    RIFF = "RIFF"
    LIST = "LIST"
    WAVE = "WAVE"

    FMT = "fmt "
    DATA = "data"
    ID3 = "ID3 "

    @property
    def is_container(self) -> bool:
        """Whether or not this is a container chunk type."""

        return self is ChunkType.RIFF or self is ChunkType.LIST

    @staticmethod
    def from_stream(stream: BinaryIO) -> Optional["ChunkType"]:
        """Read the chunk type from a stream."""

        result = None

        check = stream.read(3).decode("ascii")
        if len(check) == 3:
            # Some files hackily have some 'ID3' metadata at the end?
            if check != "ID3":
                result = ChunkType(check + stream.read(1).decode("ascii"))

        return result

    def to_stream(self, stream: BinaryIO) -> None:
        """Write the chunk header."""

        data = bytes(str(self).encode("ascii"))
        assert len(data) == 4
        stream.write(data)
