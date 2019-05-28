#!/bin/bash

# default to port 8333, if RADIORA_BRIDGE_PORT is not defined
RADIORA_BRIDGE_PORT="${RADIORA_BRIDGE_PORT:-8333}"

if [ "$RADIORA_BRIDGE_TTY" != "" ]; then
  EXTRA_OPTIONS="--env RADIORA_BRIDGE_TTY=\"$RADIORA_BRIDGE_TTY\" --device=\"$RADIORA_BRIDGE_TTY\""
fi

CMD="docker run --privileged -t -i $EXTRA_OPTIONS radiora-classic-bridge"
echo "Executing: $CMD"
$CMD
