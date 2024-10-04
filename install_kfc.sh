#!/bin/bash
set -euo pipefail

if [ ! -d "KFC" ]; then
    git clone git@github.com:lrobidou/KFC.git
fi

set -x

cd KFC
git pull
RUSTFLAGS="-C target-cpu=native" cargo build --release
cp target/release/kfc .
