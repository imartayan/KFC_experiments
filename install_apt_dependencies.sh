#!/bin/bash
set -euo pipefail

# https://stackoverflow.com/questions/18215973/how-to-check-if-running-as-root-in-a-bash-script
sudo="sudo"
if [ $(id -u) -eq 0 ]; then
    sudo=""
fi

set -x

${sudo} apt update

${sudo} apt install -y build-essential cmake git python3 wget
