<!--
    =====================================
    generator=datazen
    version=3.1.4
    hash=c8fbe39d4a560fc68d4d3bba34f88ccd
    =====================================
-->

# quasimoto ([0.2.0](https://pypi.org/project/quasimoto/))

[![python](https://img.shields.io/pypi/pyversions/quasimoto.svg)](https://pypi.org/project/quasimoto/)
![Build Status](https://github.com/vkottler/quasimoto/workflows/Python%20Package/badge.svg)
[![codecov](https://codecov.io/gh/vkottler/quasimoto/branch/master/graphs/badge.svg?branch=master)](https://codecov.io/github/vkottler/quasimoto)
![PyPI - Status](https://img.shields.io/pypi/status/quasimoto)
![Dependents (via libraries.io)](https://img.shields.io/librariesio/dependents/pypi/quasimoto)

*A lossless audio generator.*

## Documentation

### Generated

* By [sphinx-apidoc](https://vkottler.github.io/python/sphinx/quasimoto)
(What's [`sphinx-apidoc`](https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html)?)
* By [pydoc](https://vkottler.github.io/python/pydoc/quasimoto.html)
(What's [`pydoc`](https://docs.python.org/3/library/pydoc.html)?)

## Python Version Support

This package is tested with the following Python minor versions:

* [`python3.11`](https://docs.python.org/3.11/)
* [`python3.12`](https://docs.python.org/3.12/)

## Platform Support

This package is tested on the following platforms:

* `ubuntu-latest`
* `macos-latest`
* `windows-latest`

# Introduction

# Command-line Options

```
$ ./venv3.11/bin/quasimoto -h

usage: quasimoto [-h] [--version] [-v] [-q] [--curses] [--no-uvloop] [-C DIR]
                 {gen,noop} ...

A lossless audio generator.

options:
  -h, --help         show this help message and exit
  --version          show program's version number and exit
  -v, --verbose      set to increase logging verbosity
  -q, --quiet        set to reduce output
  --curses           whether or not to use curses.wrapper when starting
  --no-uvloop        whether or not to disable uvloop as event loop driver
  -C DIR, --dir DIR  execute from a specific directory

commands:
  {gen,noop}         set of available commands
    gen              generate audio
    noop             command stub (does nothing)

```

# Internal Dependency Graph

A coarse view of the internal structure and scale of
`quasimoto`'s source.
Generated using [pydeps](https://github.com/thebjorn/pydeps) (via
`mk python-deps`).

![quasimoto's Dependency Graph](im/pydeps.svg)
