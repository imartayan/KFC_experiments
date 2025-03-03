#!/bin/bash
set -euo pipefail

if [ ! -d "KFC" ]; then
    git clone https://github.com/lrobidou/KFC.git
fi

set -x

cd KFC
git pull
RUSTFLAGS="-C target-cpu=native" cargo +nightly build --release -F nightly
cp target/release/kfc .
