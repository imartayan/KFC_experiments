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

## Running the experiments

You can run all the experiments with
```sh
python3 main.py
```

This will write the results of the experiments in the `logs` folder, please leave it untouched if you want to generate plots with them.

## Generating the plots

You can generate all the plots with
```sh
python3 plots.py
```

This will save the plots in the `plots` folder.
