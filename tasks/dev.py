"""
A module implementing developmental runtimepy interfaces.
"""

# built-in
import asyncio
from contextlib import contextmanager
import math
from typing import Iterator

# third-party
import pyaudio
from runtimepy.net.arbiter import AppInfo
from runtimepy.net.arbiter.task import ArbiterTask, TaskFactory
from runtimepy.primitives import Double

# internal
from tasks.stereo import StereoInterface


@contextmanager
def get_pyaudio() -> Iterator[pyaudio.PyAudio]:
    """Get a PyAudio instance."""

    audio = pyaudio.PyAudio()
    try:
        yield audio
    finally:
        audio.terminate()


class StereoTask(ArbiterTask):
    """A task for logging metrics."""

    auto_finalize = True

    audio: pyaudio.PyAudio
    stream: pyaudio.Stream

    def _init_state(self) -> None:
        """Add channels to this instance's channel environment."""

        # Add channels from this here.
        self.stereo = StereoInterface()

        sampler = self.stereo.left
        self.env.channel("left.frequency", sampler.frequency, commandable=True)
        self.env.channel("left.amplitude", sampler.amplitude, commandable=True)

        sampler = self.stereo.right
        self.env.channel(
            "right.frequency", sampler.frequency, commandable=True
        )
        self.env.channel(
            "right.amplitude", sampler.amplitude, commandable=True
        )

        self.buffer_depth_scalar = Double(value=10.0)
        self.env.channel(
            "buffer_depth_scalar", self.buffer_depth_scalar, commandable=True
        )

    @staticmethod
    @contextmanager
    def get_stream(
        audio: pyaudio.PyAudio, stereo: StereoInterface
    ) -> Iterator[pyaudio.Stream]:
        """Get a pyaudio stream."""

        try:
            stream = audio.open(
                format=audio.get_format_from_width(stereo.left.num_bits // 8),
                channels=stereo.num_channels,
                rate=stereo.left.sample_rate,
                stream_callback=stereo.callback,
                output=True,
            )
            yield stream
        finally:
            stream.close()

    async def init(self, app: AppInfo) -> None:
        """Initialize this task with application information."""

        await super().init(app)

        self.audio = app.stack.enter_context(get_pyaudio())

        self.stream = app.stack.enter_context(
            StereoTask.get_stream(self.audio, self.stereo)
        )

    async def dispatch(self) -> bool:
        """Dispatch an iteration of this task."""

        result: bool = self.stream.is_active()
        if result:
            # Populate 10x our period
            self.stereo.buffer_to_duration(
                self.period_s.value * self.buffer_depth_scalar.value
            )

        return result


class Stereo(TaskFactory[StereoTask]):
    """A factory for the stereo task."""

    kind = StereoTask


async def main(app: AppInfo) -> int:
    """Waits for the stop signal to be set."""

    stereo = list(app.search_tasks(kind=StereoTask))[0].stereo

    freq = 0.5
    loop = asyncio.get_running_loop()

    # Alter the frequencies.
    while not app.stop.is_set():
        # Conform to 0-1 domain.
        raw = (math.sin(math.tau * loop.time() * freq) + 1.0) / 2.0

        # Re-assign
        stereo.left.amplitude.value = raw
        stereo.right.amplitude.value = 1 - raw

        # Run periodically.
        await asyncio.sleep(0.01)

    return 0
