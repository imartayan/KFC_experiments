#!/bin/bash
set -euo pipefail

if [ ! -d "gerbil" ]; then
    git clone https://github.com/uni-halle/gerbil.git
fi

set -x

cd gerbil
git pull
mkdir -p build
cd build
cmake ..
make
