"""
A module implementing interfaces for writing WAVE files.
"""

# built-in
from contextlib import contextmanager
import os
from pathlib import Path
from typing import Iterable, Iterator

# third-party
from runtimepy.primitives import Int16

# internal
from quasimoto.enums import ChunkType
from quasimoto.riff import RiffInterface
from quasimoto.riff.chunk import Chunk
from quasimoto.wave.mixins import FormatMixin

DEFAULT_SAMPLE_RATE = 44100
DEFAULT_CHANNELS = 2
DEFAULT_BITS = 16


class WaveWriter(FormatMixin):
    """A class for reading and writing WAVE files."""

    def __init__(
        self,
        riff: RiffInterface,
        num_channels: int = DEFAULT_CHANNELS,
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        bits_per_sample: int = DEFAULT_BITS,
    ) -> None:
        """Initialize this instance."""

        super().__init__()
        self.riff = riff
        assert self.riff.is_writer

        # Finish writing RIFF header.
        ChunkType.WAVE.to_stream(self.riff.stream)

        assert (num_channels * bits_per_sample) % 8 == 0
        class_num = num_channels * bits_per_sample // 8

        # Write 'fmt ' chunk.
        self.format["type"] = "pcm"
        self.format["channels"] = num_channels
        self.format["sample_rate"] = sample_rate
        self.format["bytes_per_second"] = int(class_num * sample_rate)
        self.format["class"] = class_num
        self.format["bits_per_sample"] = bits_per_sample

        data = bytes(self.format.array)
        self.riff.write(Chunk(ChunkType.FMT, len(data), data=data))

        # Write 'data' chunk header.
        ChunkType.DATA.to_stream(self.riff.stream)

    def write(self, samples: Iterable[tuple[int, ...]]) -> None:
        """Write samples to the output."""

        # Only support writing 16-bit samples.
        assert self.sample_bytes == 2

        with self.log_time("Writing samples", reminder=True):
            self.riff.stream.seek(0, os.SEEK_END)
            size_pos = self.riff.stream.tell()
            self.riff.write_size(0)

            size = 0
            for sample in samples:
                for point in sample:
                    Int16.kind.write(
                        point, self.riff.stream, byte_order=self.byte_order
                    )
                    size += 2

            self.riff.write_size(size, seek=size_pos)

    @staticmethod
    @contextmanager
    def from_path(path: Path, **kwargs) -> Iterator["WaveWriter"]:
        """Get a WAVE reader from a path."""
        with RiffInterface.from_path(path) as riff:
            yield WaveWriter(riff, **kwargs)
