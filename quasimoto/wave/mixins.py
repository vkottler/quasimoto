"""
A module hosting mixin classes related to WAVE files.
"""

# built-in
from typing import cast

# third-party
from runtimepy.codec.protocol import Protocol
from runtimepy.primitives.byte_order import ByteOrder
from vcorelib.logging import LoggerMixin

# internal
from quasimoto.wave.protocol import WaveFormat


class FormatMixin(LoggerMixin):
    """A class mixin for classes that use wave format data."""

    def __init__(self) -> None:
        """Initialize this instance."""

        super().__init__()
        self.format = WaveFormat.instance()

    @property
    def byte_order(self) -> ByteOrder:
        """Get the byte order for this format."""
        return self.format.array.byte_order

    @property
    def channels(self) -> int:
        """Get the number of channels in this stream."""
        return cast(int, self.format["channels"])

    @property
    def sample_bits(self) -> int:
        """Get the number of bits per sample."""
        return cast(int, self.format["bits_per_sample"])

    @property
    def sample_bytes(self) -> int:
        """Get the number of bytes per sample."""

        bits = self.sample_bits
        assert bits % 8 == 0
        return self.sample_bits // 8

    @property
    def sample_rate(self) -> int:
        """Get the sample rate."""
        return cast(int, self.format["sample_rate"])

    @property
    def sample_period(self) -> float:
        """Get the sample period for this data."""
        return 1.0 / self.sample_rate

    def validate_header(self, header: Protocol) -> None:
        """Validate the 'fmt ' chunk data."""

        # Validate bitrate.
        assert (
            header["bytes_per_second"]
            == header["sample_rate"]  # type: ignore
            * header["bits_per_sample"]
            * header["channels"]
            / 8
        )
