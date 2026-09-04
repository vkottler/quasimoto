"""
A module implementing interfaces for reading WAVE files.
"""

# built-in
from collections.abc import Iterator
from contextlib import contextmanager
from io import BytesIO
from pathlib import Path
from typing import cast

# third-party
from runtimepy.primitives import Int16
from vcorelib.math.time import nano_str

# internal
from quasimoto.enums import ChunkType
from quasimoto.riff import RiffInterface
from quasimoto.riff.chunk import Chunk
from quasimoto.wave.mixins import FormatMixin


class WaveReader(FormatMixin):
    """A class for reading and writing WAVE files."""

    def __init__(self, riff: RiffInterface) -> None:
        """Initialize this instance."""

        super().__init__()

        assert not riff.is_writer

        # Only need 'fmt ' and 'data' chunks.
        chunks = list(riff.chunks())
        format_chunk = None
        for chunk in chunks:
            if chunk.kind is ChunkType.FMT:
                assert format_chunk is None
                format_chunk = chunk

            if chunk.kind is ChunkType.DATA:
                assert not hasattr(self, "data")
                self.data: Chunk = chunk

        # Parse format.
        assert format_chunk is not None
        assert format_chunk.kind is ChunkType.FMT
        assert format_chunk.size == 16
        assert format_chunk.data is not None
        self.format.update(format_chunk.data)

        # Validate format.
        self.validate_header(self.format)
        self.logger.info("Format header: %s.", self.format)

        # Validate data chunk.
        assert self.data.kind is ChunkType.DATA

        # Dump some information.
        self.logger.info("%s of sample data.", self.duration_str)

    @property
    def num_samples(self) -> int:
        """Get the number of samples contained."""

        all_channels = self.channels * self.sample_bytes
        assert self.data.size % all_channels == 0
        return self.data.size // all_channels

    @property
    def duration_s(self) -> float:
        """Get the duration in seconds of this data."""
        return self.num_samples / self.sample_rate

    @property
    def duration_str(self) -> str:
        """Get this data's duration as a human-readable string."""
        return nano_str(int(self.duration_s * 1e9), is_time=True) + "s"

    def chunked_samples(self, count: int) -> Iterator[list[tuple[int, ...]]]:
        """Iterate over samples in chunks."""

        chunk = []
        for sample in self.samples:
            chunk.append(sample)
            if len(chunk) == count:
                yield chunk
                chunk = []

        if chunk:
            yield chunk

    @property
    def samples(self) -> Iterator[tuple[int, ...]]:
        """Get raw samples as a generator."""

        assert self.data.data is not None

        # Only support reading 16-bit samples.
        assert self.sample_bytes == 2

        num_channels = self.channels

        with BytesIO(self.data.data) as stream:
            with self.log_time("Processing samples", reminder=True):
                for _ in range(self.num_samples):
                    yield tuple(
                        cast(
                            int,
                            Int16.kind.read(
                                stream, byte_order=self.byte_order
                            ),
                        )
                        for _ in range(num_channels)
                    )

                # Confirm we're at the end of the data.
                assert stream.tell() == self.data.size

    @staticmethod
    @contextmanager
    def from_path(path: Path) -> Iterator["WaveReader"]:
        """Get a WAVE reader from a path."""

        with RiffInterface.from_path(path, is_writer=False) as riff:
            yield WaveReader(riff)
