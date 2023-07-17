#!/bin/bash

# Start Xvfb
Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &

# Export the DISPLAY environment variable
export DISPLAY=:99

cd /opt/pwd
./testscript.sh
