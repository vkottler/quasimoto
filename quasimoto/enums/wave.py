"""
A module implementing enumeration interfaces related to WAVE files.
"""

# built-int
from typing import Optional

# third-party
from runtimepy.codec.protocol import Protocol
from runtimepy.enum.registry import EnumRegistry, RuntimeIntEnum
from runtimepy.primitives.byte_order import ByteOrder

ENUMS = EnumRegistry()


class WaveType(RuntimeIntEnum):
    """Enumeration for WAVE data formats."""

    PCM = 1

    @classmethod
    def id(cls) -> Optional[int]:
        """Override in sub-class to coerce enum id."""
        return 10


WaveType.register_enum(ENUMS)


class WaveClass(RuntimeIntEnum):
    """An enumeration for valid kinds of WAVE configurations."""

    MONO_8 = 1
    STEREO_8 = 2
    STEREO_16 = 4

    @classmethod
    def id(cls) -> Optional[int]:
        """Override in sub-class to coerce enum id."""
        return 11


WaveClass.register_enum(ENUMS)


class WaveShape(RuntimeIntEnum):
    """An enumeration describing possible wave shapes."""

    SINE = 1
    TRIANGLE = 2
    SQUARE = 3
    SAWTOOTH = 4

    @classmethod
    def id(cls) -> Optional[int]:
        """Override in sub-class to coerce enum id."""
        return 12


WaveShapelike = WaveShape | int | str
WaveShape.register_enum(ENUMS)
BYTE_ORDER = ByteOrder.LITTLE_ENDIAN


def wave_protocol() -> Protocol:
    """Get a protocol instance suitable for WAVE file interactions."""
    return Protocol(ENUMS, byte_order=BYTE_ORDER)
