#!/bin/bash
set -ex

wget -O /tmp/config.json $CONFIG 
blockchain-explorer --global-config /tmp/config.json
