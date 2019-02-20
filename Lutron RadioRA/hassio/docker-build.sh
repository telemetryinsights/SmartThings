#!/bin/bash

cd lutron-radiora1

# default build is homeassistant/amd64-base:latest
docker build -t local/lutron-radiora1 .
