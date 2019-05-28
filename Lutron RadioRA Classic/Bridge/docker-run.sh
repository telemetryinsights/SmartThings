#!/bin/bash

# to run in Docker:
#CMD="docker run --env SERIAL_TTY=$RADIORA_BRIDGE_TTY -t -i --device=$RADIORA_BRIDGE_TTY --privileged radiora-classic-bridge"
CMD="docker run -t -i --privileged radiora-classic-bridge"

echo "Executing: $CMD"
$CMD