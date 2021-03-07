#!/bin/bash

if [ "$RADIORA_BRIDGE_TTY" != "" ]; then
  EXTRA_OPTIONS="--env RADIORA_BRIDGE_TTY=\"$RADIORA_BRIDGE_TTY\" --device=\"$RADIORA_BRIDGE_TTY\""
fi

CMD="docker run --privileged -t -i $EXTRA_OPTIONS radiora-classic-bridge"
echo "Executing: $CMD"
$CMD
