#!/bin/bash
set -euo pipefail

if [ ! -d "KFC" ]; then
    git clone git@github.com:lrobidou/KFC.git
fi

set -x

cd KFC
git pull
cargo build --release
cp target/release/kfc .
