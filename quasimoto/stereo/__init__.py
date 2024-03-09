"""
A module implementing a simple stereo signal interface.
"""

# built-in
from copy import copy
from io import BytesIO
from queue import SimpleQueue

# third-party
import pyaudio

# internal
from quasimoto.sampler.channel import SignalChannel
from quasimoto.sampler.time import TimeKeeper
from quasimoto.wave import WaveWriter


class StereoInterface:
    """An interface for managing stereo sound output."""

    num_channels = 2

    def __init__(self) -> None:
        """Initialize this instance."""

        self.time = TimeKeeper()
        self.left = SignalChannel(self.time)
        self.right = copy(self.left)

        self.sample_queue: SimpleQueue[tuple[int, int]] = SimpleQueue()

        self.left_raw: list[int] = []
        self.right_raw: list[int] = []

    def next(self) -> tuple[int, int]:
        """Get the next pair of samples."""

        left = next(self.left)
        right = next(self.right)
        self.time.advance()
        return left, right

    def buffer_to_duration(self, duration_s: float) -> None:
        """Fill sample-queue buffer to the specified duration."""

        for _ in range(
            int(duration_s * self.time.sample_rate) - self.sample_queue.qsize()
        ):
            self.sample_queue.put_nowait(self.next())

    def frames(self, frame_count: int) -> bytes:
        """Get sample frames in a single chunk of bytes."""

        with BytesIO() as stream:
            # Get pre-computed samples from queue.
            from_queue = min(self.sample_queue.qsize(), frame_count)
            for _ in range(from_queue):
                left, right = self.sample_queue.get_nowait()
                WaveWriter.to_stream(stream, left)
                WaveWriter.to_stream(stream, right)

                self.left_raw.append(left)
                self.right_raw.append(right)

            # Get new samples if necessary.
            frame_count -= from_queue
            for _ in range(frame_count):
                left, right = self.next()
                WaveWriter.to_stream(stream, left)
                WaveWriter.to_stream(stream, right)

                self.left_raw.append(left)
                self.right_raw.append(right)

            return stream.getvalue()

    def callback(self, in_data, frame_count, time_info, status):
        """Called when stream needs more data in raw bytes."""

        # Not an input callback (is None).
        del in_data

        # Example Contents:
        #
        # {
        #   'input_buffer_adc_time': 0.8380952380952347,
        #   'current_time': 16208.699135654,
        #   'output_buffer_dac_time': 16208.709929304794
        # }
        del time_info

        # Always 0?
        del status

        return (self.frames(frame_count), pyaudio.paContinue)
