"""
A module implementing a protocol factory for the 'fmt ' chunk data.
"""

# third-party
from runtimepy.codec.protocol import Protocol, ProtocolFactory
from runtimepy.enum.registry import EnumRegistry, RuntimeIntEnum
from runtimepy.primitives.byte_order import ByteOrder

ENUMS = EnumRegistry()


class WaveType(RuntimeIntEnum):
    """Enumeration for WAVE data formats."""

    PCM = 1


WaveType.register_enum(ENUMS)


class WaveClass(RuntimeIntEnum):
    """An enumeration for valid kinds of WAVE configurations."""

    MONO_8 = 1
    STEREO_8 = 2
    STEREO_16 = 4


WaveClass.register_enum(ENUMS)
BYTE_ORDER = ByteOrder.LITTLE_ENDIAN


class WaveFormat(ProtocolFactory):
    """Parse the WAVE format data from bytes."""

    protocol: Protocol = Protocol(ENUMS, byte_order=BYTE_ORDER)

    @classmethod
    def initialize(cls, protocol: Protocol) -> None:
        """Initialize this protocol."""

        protocol.add_field("type", "uint16", enum="WaveType")
        protocol.add_field("channels", "uint16")
        protocol.add_field("sample_rate", "uint32")
        protocol.add_field("bytes_per_second", "uint32")

        protocol.add_field("class", "uint16", enum="WaveClass")
        protocol.add_field("bits_per_sample", "uint16")
