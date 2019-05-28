#!/bin/bash

if [ -z "RADIORA_BRIDGE_TTY"]
then
  CMD="docker run -t -i --privileged radiora-classic-bridge"
else
  CMD="docker run --env RADIORA_BRIDGE_TTY=$RADIORA_BRIDGE_TTY -t -i --device=$RADIORA_BRIDGE_TTY --privileged radiora-classic-bridge"
end

echo "Executing: $CMD"
$CMD
