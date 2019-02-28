#!/bin/bash

# NOTE: to override the Bridge's default /dev/tty* search path set SERIAL_TTY; can be comma separate list of devices to search
# export SERIAL_TTY=/dev/tty.usbserial,/dev/serial0

# NOTE: mapping of Mac /dev/tty* into Linux Docker environment is currently not supported by Docker (Feb 2019)

python3 radiora-classic-bridge.py
