"""
A module for streaming raw data to pyaudio.
"""

# built-in
from contextlib import contextmanager
from io import BytesIO
import sys
import time
from typing import Iterator

# third-party
import pyaudio

# internal
from quasimoto.sampler import Sampler
from quasimoto.wave import WaveWriter


@contextmanager
def get_pyaudio() -> Iterator[pyaudio.PyAudio]:
    """Get a PyAudio instance."""

    audio = pyaudio.PyAudio()
    try:
        yield audio
    finally:
        audio.terminate()


def main(argv: list[str]) -> int:
    """The program's main entry."""

    left = Sampler()
    right = left.copy(harmonic=-1)

    def callback(in_data, frame_count, time_info, status) -> bytes:
        """Called when stream needs more data?"""

        # Need to figure out what these are.
        del in_data
        del time_info
        del status

        with BytesIO() as stream:
            for _ in range(frame_count):
                WaveWriter.to_stream(stream, next(left))
                WaveWriter.to_stream(stream, next(right))
            return (stream.getvalue(), pyaudio.paContinue)

    with get_pyaudio() as audio:
        stream = audio.open(
            format=audio.get_format_from_width(left.num_bits // 8),
            channels=2,
            rate=left.sample_rate,
            output=True,
            stream_callback=callback,
        )

        keep_going = True

        while keep_going and stream.is_active():
            try:
                time.sleep(0.1)
            except KeyboardInterrupt:
                stream.close()
                keep_going = False

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
