#!/bin/bash
python3  $(git rev-parse --show-toplevel)/graphmaker.py "$@"

