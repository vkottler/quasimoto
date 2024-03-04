#!/bin/bash

set -e

pushd "$CWD" >/dev/null || exit

# Get PortAudio source.
if [ ! -d portaudio ]; then
	git clone https://github.com/PortAudio/portaudio
	sudo apt-get install libasound-dev
fi

# Get PyAudio source.
if [ ! -d pyaudio ]; then
	git clone https://people.csail.mit.edu/hubert/git/pyaudio.git
fi

VENV="venv$PYTHON_VERSION"
PIP="$VENV/bin/pip"
PYTHON="$VENV/bin/python"

setup_venv() {
	$PIP install -e "$REPO"
	$PIP install -e pyaudio
}

if [ ! -d "$VENV" ]; then
	"python$PYTHON_VERSION" -m venv "$VENV"
	test -f "$PYTHON"

	"$PIP" install -U pip
	setup_venv
fi

on_exit() {
	popd >/dev/null || exit
}

trap on_exit EXIT

SAMPLE_WAV="$REPO/tests/data/valid/vonbass.wav"
test -f "$SAMPLE_WAV"
