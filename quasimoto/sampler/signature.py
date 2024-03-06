"""
A module implementing a simple time-signature interface.
"""

DEFAULT_TEMPO = 120


def beat_period(tempo: int = DEFAULT_TEMPO) -> float:
    """
    Get the period in seconds of a single beat, based on beats-per-second
    tempo.
    """
    return 1.0 / (float(tempo) / 60.0)
