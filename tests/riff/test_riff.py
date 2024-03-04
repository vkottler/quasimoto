"""
Test the 'riff' module.
"""

# built-in
from pathlib import Path

# third-party
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fftfreq, rfft
from vcorelib.paths.context import tempfile

# module under test
from quasimoto.riff import RiffInterface
from quasimoto.sampler import Sampler
from quasimoto.sampler.time import TimeKeeper
from quasimoto.wave import WaveReader, WaveWriter

# internal
from tests.resources import resource


def test_riff_reader_basic():
    """Test basic RIFF reading scenarios."""

    path = resource("vonbass.wav")

    with RiffInterface.from_path(path, is_writer=False) as reader:
        assert list(reader.chunks())

    left_chan = []
    right_chan = []
    with WaveReader.from_path(path) as wave:
        num_bits = wave.sample_bits
        for left, right in wave.samples:
            left_chan.append(left / num_bits)
            right_chan.append(right / num_bits)

        # try doing fft shit
        left_fft = np.abs(rfft(left_chan))

        num_samples = wave.num_samples
        plt.plot(
            fftfreq(num_samples, wave.sample_period)[: len(left_fft)],
            left_fft,
        )

        # Un-comment while debugging.
        # plt.show()

        assert len(rfft(right_chan)) > 0


def test_writing_test_wav():
    """Write the 'test.wav' output."""

    with WaveWriter.from_path(Path("test.wav")) as writer:
        stop_time = 4.0
        time = TimeKeeper()
        base = Sampler(time, stop_time=stop_time)
        assert iter(base)

        samplers = set(
            [
                base.copy(3, stop_time=stop_time / 8.0),
                base.copy(2, stop_time=stop_time / 4.0),
                base.copy(1, stop_time=stop_time / 2.0),
                base,
                base.copy(-1, stop_time=stop_time / 2.0),
                base.copy(-2, stop_time=stop_time / 4.0),
                base.copy(-3, stop_time=stop_time / 8.0),
            ]
        )

        samples = []
        single_chan = []

        while samplers:
            parts = []
            to_remove = []
            for sampler in samplers:
                val = next(sampler, None)
                if val is not None:
                    parts.append(val)
                else:
                    to_remove.append(sampler)

            for sampler in to_remove:
                samplers.remove(sampler)

            # Advance time.
            time.advance()

            if parts:
                val = int(sum(parts) / len(parts))
                samples.append((val, val))
                single_chan.append(val)

        writer.write(samples)

        # try doing fft shit
        chan_fft = np.abs(rfft(single_chan))

        num_samples = len(single_chan)
        plt.plot(
            fftfreq(num_samples, writer.sample_period)[: len(chan_fft)],
            chan_fft,
        )

        # Un-comment while debugging.
        # plt.show()


def test_riff_writer_basic():
    """Test basic RIFF writing scenarios."""

    num_samples = 4096

    with tempfile(suffix=".wav") as path:
        with WaveWriter.from_path(path) as writer:
            writer.write((0, 0) for _ in range(num_samples))

        with WaveReader.from_path(path) as wave:
            left_chan = []
            right_chan = []
            for left, right in wave.samples:
                left_chan.append(left)
                right_chan.append(right)

            assert left_chan == [0 for _ in range(num_samples)]
            assert right_chan == [0 for _ in range(num_samples)]
