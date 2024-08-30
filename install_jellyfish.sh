#!/bin/bash
set -euxo pipefail

mkdir -p jellyfish
cd jellyfish
wget -O jellyfish.tar.gz https://github.com/gmarcais/Jellyfish/releases/download/v2.3.1/jellyfish-2.3.1.tar.gz
tar -xf jellyfish.tar.gz --strip-components 1
./configure
make -j
