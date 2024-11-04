# KFC experiments

Experiments on hyper-*k*-mers

You can clone the repository and its submodules with
```sh
git clone --recursive https://github.com/imartayan/KFC_experiments.git
```

If you did not use the `--recursive` flag, make sure to load the submodules with
```sh
git submodule update --init --recursive
```

## Setup

If you have not installed Rust yet, please visit [rustup.rs](https://rustup.rs/) to install it.
Once this is done, you can build all the tools with
```sh
bash install_all.sh
```

If the installation fails, make sure you have the following packages installed on your machine:
```
autoconf automake cmake gcc git libbz2 libcurl liblzma libssl make perl python3 python3-pandas python3-seaborn wget zlib
```
On Debian-based distributions, you can install them with
```sh
bash install_apt_dependencies.sh
```

## Running the experiments

On MacOS, you will first need to increase the limit of temporary files to run KMC properly:
```sh
ulimit -n 2048
```

The experiment script (experiment.py) contains a total of 3 subcommands {onk, onc, plot}.
Doing
```sh
python experiment.py -h
usage: experiment.py [-h] __default {onk,onc,plot} ...

positional arguments:
  __default
  {onk,onc,plot}
    onk           Run experiments on given dataset by changing k
    onc           Run experiments by changing coverage of the given dataset
    plot          Plot set of experiments

options:
  -h, --help      show this help message and exit
```

An example of testing a dataset "input.fasta.gz" for multiple, user-defined k's is given below:
```sh
python experiment.py -i input.fasta.gz -o output/folder/ -g log/folder/ -k 31 63 127 255 -m 27 -r 2 -p 1 -t 16 -x 128 -d tmp/folder/
```

It is also possible to test multiple k's for a given range of values:
```sh
python experiment.py -i input.fasta.gz -o output/folder/ -g log/folder/ -k 31 10 -K 255 -m 27 -r 2 -p 1 -t 16 -x 128 -d tmp/folder/
```

The above command will test all k-mer lengths from 31 (included) to 255 (excluded) by incrementing k by 10 at each iteration. 

Benchmark results are stored in `log/folder/` whereas `output/folder/` stores command outputs (k-mer counting tables).

## Generating the plots

You can generate all the plots with
```sh
python3 plots.py -g log/folder/ -i input.fasta.gz -o plots/folder/
```
`log/folder/` is the previous log directory.
Option `-i input.fasta.gz` is necessary because the name of the input file (absolute path) is used as key to find its experiments. 
This will save the plots in the `plots/folder/` folder.
