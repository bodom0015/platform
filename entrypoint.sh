#!/bin/bash

echo "Starting nest UI..."
echo "Project: ${PROJECT_ENV:-knoweng}"
echo "Run Level: ${NEST_RUNLEVEL:-development}"

# Copy appropriate index.html to the foreground
cp client/index.${PROJECT_ENV}.html client/index.html

/usr/bin/supervisord
