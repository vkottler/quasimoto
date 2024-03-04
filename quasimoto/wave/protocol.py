"""
A module implementing a protocol factory for the 'fmt ' chunk data.
"""

# third-party
from runtimepy.codec.protocol import Protocol, ProtocolFactory

# internal
from quasimoto.enums.wave import wave_protocol


class WaveFormat(ProtocolFactory):
    """Parse the WAVE format data from bytes."""

    protocol: Protocol = wave_protocol()

    @classmethod
    def initialize(cls, protocol: Protocol) -> None:
        """Initialize this protocol."""

        protocol.add_field("type", "uint16", enum="WaveType")
        protocol.add_field("channels", "uint16")
        protocol.add_field("sample_rate", "uint32")
        protocol.add_field("bytes_per_second", "uint32")

        protocol.add_field("class", "uint16", enum="WaveClass")
        protocol.add_field("bits_per_sample", "uint16")
