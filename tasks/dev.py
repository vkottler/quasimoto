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
from quasimoto.enums.wave import WaveShape
from quasimoto.sampler import Sampler
from quasimoto.sampler.notes import Note
from quasimoto.sampler.signature import beat_period
from quasimoto.sampler.source import SourceInterface
from quasimoto.sampler.time import TimeCallback, TimeKeeper
from quasimoto.stereo import StereoInterface


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

    def register_source_state(
        self, name: str, source: SourceInterface, commandable: bool = True
    ) -> None:
        """Register state for a source instance."""

        self.env.channel(
            f"{name}.frequency", source.frequency, commandable=commandable
        )
        self.env.channel(
            f"{name}.amplitude", source.amplitude, commandable=commandable
        )
        self.env.channel(
            f"{name}.shape", source.shape, commandable=True, enum="WaveShape"
        )
        self.env.channel(f"{name}.enabled", source.enabled)

    def _init_state(self) -> None:
        """Add channels to this instance's channel environment."""

        WaveShape.register_enum(self.env.enums)

        self.stereo = StereoInterface()
        # register state from stereo / individual left and right channels

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

        # remove at some point
        num_bits = 16

        stream = audio.open(
            format=audio.get_format_from_width(num_bits // 8),
            channels=stereo.num_channels,
            rate=stereo.time.sample_rate,
            stream_callback=stereo.callback,
            output=True,
        )
        try:
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


def create_plots() -> None:
    """A method for creating some waveform plots."""

    sampler = Sampler(TimeKeeper())
    sampler.plot("out.png", 0.01)


def increment_wave_shapes(stereo: StereoInterface, step: int) -> None:
    """Increment wave shapes for current stereo sources."""

    # Change the wave shapes.
    if step % 100 == 0:
        for source in stereo.left.sources.values():
            if isinstance(source, Sampler):
                source.next_shape()
        for source in stereo.right.sources.values():
            if isinstance(source, Sampler):
                source.next_shape()


def sinusoidal_amplitude(stereo: StereoInterface, freq: float = 0.5) -> None:
    """Modify amplitude sinusoidally over time."""

    raw = (
        math.sin(math.tau * asyncio.get_running_loop().time() * freq) + 1.0
    ) / 2.0
    flipped = 1 - raw

    # Re-assign
    for source in stereo.left.sources.values():
        source.amplitude.value = raw
    for source in stereo.right.sources.values():
        source.amplitude.value = flipped


async def main(app: AppInfo) -> int:
    """Waits for the stop signal to be set."""

    # create_plots()

    stereo = list(app.search_tasks(kind=StereoTask))[0].stereo

    # register factories
    assert stereo.left.register_factory(Sampler)

    quarter = beat_period()

    source_idx = 0

    def play_note(
        duration: float, *notes: Note, octave: int = 0
    ) -> TimeCallback:
        """Create a routine that plays a simple note."""

        def routine(now: float) -> None:
            """Register the note source."""

            del now

            nonlocal source_idx

            for note in notes:
                for chan in (stereo.left, stereo.right):
                    chan.register_dynamic(
                        str(source_idx),
                        "sampler",
                        {
                            "duration": duration,
                            "frequency": note.frequency(octave),
                        },
                    )
                    source_idx += 1

        return routine

    stereo.time.call_sequence(
        (quarter, play_note(quarter, Note.C)),
        (quarter, play_note(quarter, Note.C, Note.E, Note.G)),
        (quarter, play_note(quarter, Note.D)),
        (quarter, play_note(quarter, Note.D, Note.F, Note.A)),
        (quarter, play_note(quarter, Note.E)),
        (quarter, play_note(quarter, Note.E, Note.G, Note.B)),
        (quarter, play_note(quarter, Note.F)),
        (quarter, play_note(quarter, Note.G)),
        (quarter, play_note(quarter, Note.A)),
        (quarter, play_note(quarter, Note.B)),
        (quarter, play_note(quarter, Note.C, octave=1)),
        (quarter, play_note(quarter, Note.B)),
        (quarter, play_note(quarter, Note.A)),
        (quarter, play_note(quarter, Note.G)),
        (quarter, play_note(quarter, Note.F)),
        (quarter, play_note(quarter, Note.E)),
        (quarter, play_note(quarter, Note.D)),
        (quarter, play_note(quarter * 4.0, Note.C)),
    )

    while not app.stop.is_set():
        await asyncio.sleep(1.0)

    return 0
