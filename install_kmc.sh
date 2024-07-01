#!/bin/bash
set -euo pipefail

version="3.2.4"

# https://stackoverflow.com/questions/394230/how-to-detect-the-os-from-a-bash-script
platform="unknown"
unamestr=$(uname)
if [[ "$unamestr" == "Linux" ]]; then
    platform="linux"
elif [[ "$unamestr" == "Darwin" ]]; then
    platform="mac"
else
    echo "Unknown platform: ${unamestr}"
    exit 1
fi

arch="unknown"
unamemstr=$(uname -m)
if [[ "$unamemstr" == "x86_64" ]]; then
    arch="x64"
elif [[ "$unamemstr" == "arm64" ]]; then
    arch="arm64"
else
    echo "Unknown architecture: ${unamemstr}"
    exit 1
fi

set -x

mkdir -p kmc
cd kmc
wget -O kmc.tar.gz https://github.com/refresh-bio/KMC/releases/download/v${version}/KMC${version}.${platform}.${arch}.tar.gz
tar -xf kmc.tar.gz --strip-components 1
