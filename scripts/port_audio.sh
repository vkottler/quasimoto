#!/bin/bash

REPO=$(git rev-parse --show-toplevel)
CWD=$REPO/scripts
source "$CWD/common.sh"

pushd portaudio >/dev/null || exit

./configure
make clean
make -j
sudo make install

popd >/dev/null || exit
