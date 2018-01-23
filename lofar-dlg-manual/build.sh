#!/bin/bash

# Make sure we're standing in the correct place
dir=$(dirname $0)
cd $dir

# Go!
docker build -t dlglofar-man/centos7:latest .
