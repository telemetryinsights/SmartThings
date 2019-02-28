#!/bin/bash

if [[ -z "$SERIAL_TTY" ]]; then
    export SERIAL_TTY=/dev/tty.usbserial # update with /dev/tty* device connected to RadioRA hardware
fi
echo "RadioRA Classic Bridge is using serial $SERIAL_TTY"

# to run in Docker:
docker run --env SERIAL_TTY=$SERIAL_TTY -t -i --device=$SERIAL_TTY --privileged radiora-classic-bridge
