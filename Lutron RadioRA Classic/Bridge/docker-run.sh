#!/bin/bash

# to run in Docker:
#docker run --env SERIAL_TTY=$SERIAL_TTY -t -i --device=$SERIAL_TTY --privileged radiora-classic-bridge

CMD='docker run -t -i --privileged radiora-classic-bridge'

echo "Running $CMD"
$CMD
