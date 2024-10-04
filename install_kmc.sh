#!/bin/bash
set -euo pipefail

version="3.2.4"
MAX_K=1024

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

if [ ! -d "KMC" ]; then
    mkdir -p KMC
    cd KMC
    if [[ "$platform" == "linux" && "$arch" == "x64" ]]; then
        echo "Building KMC from source with MAX_K=${MAX_K} (this may take a while)"
        set -x
        git clone --recurse-submodules https://github.com/refresh-bio/kmc.git src
        cd src
        sed -i -e "s/256/${MAX_K}/g" kmc_core/defs.h
        make -j kmc kmc_dump kmc_tools
        cp bin/* ..
    else
        wget -O KMC.tar.gz https://github.com/refresh-bio/KMC/releases/download/v${version}/KMC${version}.${platform}.${arch}.tar.gz
        tar -xf KMC.tar.gz --strip-components 1
    fi
fi
