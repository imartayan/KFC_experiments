#!/bin/bash
set -euo pipefail

# https://stackoverflow.com/questions/18215973/how-to-check-if-running-as-root-in-a-bash-script
sudo="sudo"
if [ $(id -u) -eq 0 ]; then
    sudo=""
fi

set -x

${sudo} apt update

${sudo} apt install -y autoconf automake build-essential cmake gcc git libbz2-dev libcurl4-gnutls-dev liblzma-dev libssl-dev make perl python3 python3-pandas python3-seaborn wget zlib1g-dev
