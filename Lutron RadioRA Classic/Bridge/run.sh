#!/bin/bash

export SERIAL_TTY=/dev/tty.usbserial # update with /dev/tty* device connected to RadioRA hardware

# to run in Docker:
docker run --env SERIAL_TTY=$SERIAL_TTY -t -i --device=$SERIAL_TTY radiora-classic-bridge

# to run directly via the command line:
#python radiora-classic-bridge.py
