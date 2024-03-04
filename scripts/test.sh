#!/bin/bash

REPO=$(git rev-parse --show-toplevel)
CWD=$REPO/scripts
source "$CWD/common.sh"

# Can use this to verify sound output works.
# $PYTHON pyaudio/examples/play_wave.py "$SAMPLE_WAV"

set -x
$PYTHON stream.py
echo "Exited $?."
set +x
