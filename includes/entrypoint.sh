#!/usr/bin/env bash

Xvfb -ac :99 -screen 0 1920x1080x16 &
export DISPLAY=:99
cd /app
./fast_test_executor.py