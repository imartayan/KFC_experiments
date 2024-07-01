#!/bin/bash
set -euxo pipefail

git submodule update --init --recursive

# https://stackoverflow.com/questions/394230/how-to-detect-the-os-from-a-bash-script
if [ -f /etc/debian_version ]; then
    bash install_apt_dependencies.sh
fi

bash install_kfc.sh
bash install_kmc.sh
bash install_fastk.sh
