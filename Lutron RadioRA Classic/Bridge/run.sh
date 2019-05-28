#!/bin/bash

# NOTE: to override the RadioRA Classic Smart Bridge's default /dev/tty* search path,
# set RADIORA_BRIDGE_TTY; can be comma separate list of devices to search:
#
#   export RADIORA_BRIDGE_TTY=/dev/tty.usbserial,/dev/serial0

# NOTE: mapping of MacOS /dev/tty* into Docker environment is currently not supported (Feb 2019)

python3 radiora-classic-bridge.py
