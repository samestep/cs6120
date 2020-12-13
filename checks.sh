#!/usr/bin/env bash
set -ex

# testing
pytest
turnt lesson2/test/*.bril

# linting
flake8

# formatting
black .
