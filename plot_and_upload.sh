#!/bin/bash

set -e

# Ensure correct directory in case script is called from outside
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

./plot_graph.py record.log
dropbox_uploader.sh upload graph.png /
