#!/bin/bash
set -euo pipefail

if [ ! -d "kaarme" ]; then
    git clone https://github.com/Denopia/kaarme.git
fi

set -x

cd kaarme
git pull
mkdir -p build
cd build
cmake -S .. -B .
cmake --build .
