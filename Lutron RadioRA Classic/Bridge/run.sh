#!/bin/bash

if [[ -z "$SERIAL_TTY" ]]; then
    export SERIAL_TTY=/dev/tty.usbserial # update with /dev/tty* device connected to RadioRA hardware
fi
echo "RadioRA Classic Bridge is using serial $SERIAL_TTY"

python3 radiora-classic-bridge.py
