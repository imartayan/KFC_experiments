#!/bin/bash
set -euxo pipefail

git submodule update --init --recursive

bash install_kfc.sh
bash install_kmc.sh
bash install_fastk.sh
