#!/bin/bash

export TTY_SERIAL=/dev/tty.usbserial # update with /dev/tty* device connected to RadioRA hardware
python radiora-classic-bridge.py
