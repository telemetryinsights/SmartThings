#!/bin/bash

if [[ -z "$SERIAL_TTY" ]]; then
    export SERIAL_TTY=/dev/tty.usbserial # update with /dev/tty* device connected to RadioRA hardware
fi
echo "RadioRA Classic Bridge is using serial $SERIAL_TTY"

# NOTE: mapping of Mac /dev/tty* into Linux Docker environment is currently not supported by Docker (Feb 2019)

python3 radiora-classic-bridge.py
