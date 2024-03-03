"""
A module implementing interfaces for RIFF files.
"""

# built-in
from contextlib import contextmanager
import os
from pathlib import Path
from typing import BinaryIO, Iterator, Optional, Type, TypeVar, cast

# third-party
from runtimepy.primitives import Uint32
from runtimepy.primitives.byte_order import ByteOrder
from vcorelib.logging import LoggerMixin

# internal
from quasimoto.enums import ChunkType
from quasimoto.riff.chunk import NULL_BYTE, Chunk

T = TypeVar("T", bound="RiffInterface")


class RiffInterface(LoggerMixin):
    """A class for reading and writing RIFF files."""

    def __init__(self, stream: BinaryIO, is_writer: bool = True) -> None:
        """Initialize this instance."""

        super().__init__()

        self.stream = stream

        # Write the header.
        self.is_writer = is_writer
        if self.is_writer:
            ChunkType.RIFF.to_stream(self.stream)
            # Leave a placeholder for actual size.
            self.write_size(0)
        else:
            header = self.read()
            assert header is not None
            self.header: Chunk = header
            self.logger.info("Header: %s.", self.header)
            assert self.header.kind is ChunkType.RIFF

    def read_size(self) -> int:
        """Read a size from the stream."""

        return cast(
            int,
            Uint32.kind.read(self.stream, byte_order=ByteOrder.LITTLE_ENDIAN),
        )

    def read(self) -> Optional[Chunk]:
        """Read the next chunk."""

        result = None

        print(self.stream.tell())
        kind = ChunkType.from_stream(self.stream)
        if kind is not None:
            size = self.read_size()
            data = None
            form = None

            if not kind.is_container:
                data = self.stream.read(size)
                if size % 2 == 1:
                    self.stream.read(1)  # pragma: nocover
            else:
                form = ChunkType.from_stream(self.stream)

            result = Chunk(kind, size, data=data, form=form)

        return result

    def chunks(self) -> Iterator[Chunk]:
        """Read file chunks."""

        result = self.read()
        while result is not None:
            yield result
            result = self.read()

    def write_size(self, size: int, seek: int = None) -> None:
        """An interface for writing a size field."""

        # Validate size.
        prim = Uint32.kind
        bounds = prim.int_bounds
        assert bounds is not None
        assert bounds.validate(size), size

        if seek is not None:
            self.stream.seek(seek)

        # Write size.
        Uint32.kind.write(
            size, self.stream, byte_order=ByteOrder.LITTLE_ENDIAN
        )

    def _write_data(self, data: bytes) -> None:
        """Write chunk data."""

        size = len(data)
        self.write_size(size)

        # Write data.
        self.stream.write(data)
        if size % 2 == 1:
            self.stream.write(NULL_BYTE)  # pragma: nocover

    def write(self, chunk: Chunk) -> None:
        """Write a chunk to the file."""

        assert self.is_writer

        # Can't write container chunks this way.
        assert not chunk.kind.is_container

        # Write header.
        chunk.kind.to_stream(self.stream)

        # Write data.
        if chunk.data is not None:
            self._write_data(chunk.data)

    def finalize(self) -> None:
        """Finalize the header size."""

        if self.is_writer:
            self.stream.seek(0, os.SEEK_END)
            size = self.stream.tell() - 8
            self.write_size(size, seek=4)
        else:
            remaining = self.stream.read()
            if remaining:
                self.logger.warning(
                    "%d bytes remaining in file!", len(remaining)
                )

    @classmethod
    @contextmanager
    def from_path(
        cls: Type[T], path: Path, is_writer: bool = True
    ) -> Iterator[T]:
        """Create a RIFF interface from a path."""

        with path.open("wb" if is_writer else "rb") as out_fd:
            result = cls(out_fd, is_writer=is_writer)
            yield result
            result.finalize()
