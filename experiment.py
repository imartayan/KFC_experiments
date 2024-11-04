import sys
import pathlib
from tools import TOOLS

def onk_main(args):
    assert args.repeat >= 0
    assert args.timeout is None or args.timeout >= 0
    assert args.threshold >= 0
    assert args.threads > 0
    assert args.max_ram > 0
    assert args.minimizer_length > 0

    input_file = pathlib.Path(args.input_file)
    out_dir = pathlib.Path(args.out_dir)
    log_dir = pathlib.Path(args.log_dir)
    tmp_dir = pathlib.Path(args.tmp_dir)

    assert input_file.exists() and input_file.is_file()
    out_dir.mkdir(exist_ok=True)
    log_dir.mkdir(exist_ok=True)
    tmp_dir.mkdir(exist_ok=True)

    for idx in args.tool_indexes:
        assert 0 <= idx < len(TOOLS), "Tool index out of range or negative"

    if args.max_k:
        assert len(args.kmer_lengths) == 2, "When --max-k is used, the k-mer list must be the pair [min-k, increment step]"
        mk, inc = args.kmer_lengths
        assert mk > 0
        assert inc > 0
        assert mk >= args.minimizer_length, "Minimizer length cannot be > than k"
        for k in range(mk, args.max_k, inc):
            # print(f"Counting {k}-mers in {args.input_file}")
            for idx in args.tool_indexes:
                TOOLS[idx].run(input_file, out_dir, log_dir, tmp_dir, args.repeat, args.timeout, k=k, m=args.minimizer_length, threshold=args.threshold, threads=args.threads, max_ram=args.max_ram)
    else:
        for k in args.kmer_lengths:
            assert k > 0
            assert k >= args.minimizer_length, "Minimizer length cannot be > than k"
        for k in args.kmer_lengths:
            # print(f"Counting {k}-mers in {args.input_file}")
            for idx in args.tool_indexes:
                TOOLS[idx].run(input_file, out_dir, log_dir, tmp_dir, args.repeat, args.timeout, k=k, m=args.minimizer_length, threshold=args.threshold, threads=args.threads, max_ram=args.max_ram)

def onc_main(args):
    from tool import execute
    assert args.repeat >= 0
    assert args.timeout is None or args.timeout >= 0
    assert args.threshold >= 0
    assert args.threads > 0
    assert args.max_ram > 0
    assert args.minimizer_length > 0
    assert args.min_coverage > 0
    assert args.max_coverage > 0
    assert args.step_coverage > 0

    input_file = pathlib.Path(args.input_file)
    out_dir = pathlib.Path(args.out_dir)
    log_dir = pathlib.Path(args.log_dir)
    tmp_dir = pathlib.Path(args.tmp_dir)

    assert input_file.exists() and input_file.is_file()
    out_dir.mkdir(exist_ok=True)
    log_dir.mkdir(exist_ok=True)
    tmp_dir.mkdir(exist_ok=True)

    for k in args.kmer_lengths:
        assert k > 0
        assert k >= args.minimizer_length, "Minimizer length cannot be > than k"

    for idx in args.tool_indexes:
        assert 0 <= idx < len(TOOLS), "Tool index out of range or negative"

    coverage_sampling_exe = pathlib.Path("./coverage_sampling")
    if not coverage_sampling_exe.exists(): execute("gcc coverage_sampling.c -O3 -o coverge_sampling -lz")
    assert coverage_sampling_exe.exists()
    coverage_sample_command = "./coverage_sampling -i {} -o {} -c {} -s {}"
    for coverage in range(args.min_coverage, args.max_coverage, args.step_coverage):
        tmp_file = input_file.name
        if (tmp_file.endswith(".gz")): 
            tmp_file = tmp_file[:-3]
        if (tmp_file.endswith(".fasta") or tmp_file.endswith(".fastq")):
            tmp_file = tmp_file[:-6]
        tmp_file = "{}.cov{}.fasta".format(tmp_file, coverage)
        tmp_file = pathlib.Path(args.tmp_dir)/tmp_file
        execute(coverage_sample_command.format(args.input_file, tmp_file, coverage, args.length))
        for k in args.kmer_lengths:
            # print(f"Counting {k}-mers in {args.input_file} with coverage {coverage}")
            for idx in args.tool_indexes:
                TOOLS[idx].run(tmp_file, out_dir, log_dir, tmp_dir, args.repeat, None, k=k, m=args.minimizer_length, threshold=args.threshold, threads=args.threads, max_ram=args.max_ram)
        tmp_file.unlink()

PLOT_FORMATS = ["png", "pdf"]
def plot_main(args):
    import json
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt

    MARKERS = {
        "KFC": "o",
        "KMC": "s",
        "FASTK": "^",
        "Jellyfish": "P",
        "Gerbil": "*",
        "Kaarme": "X",
    }

    PALETTE = {
        "KFC": "tab:blue",
        "KMC": "tab:green",
        "FASTK": "tab:red",
        "Jellyfish": "tab:purple",
        "Gerbil": "tab:orange",
        "Kaarme": "tab:brown",
    }

    assert args.format.lower() in PLOT_FORMATS
    log_dir = pathlib.Path(args.log_dir)
    assert log_dir.exists(), "Log directory does not exist"
    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(exist_ok=True)

    tool_names = [tool.name for tool in TOOLS]
    logs = []
    for log_file in log_dir.iterdir():
        if log_file.is_file():
            with open(log_file, "r") as f:
                log = json.load(f)
                if log["tool"] in tool_names:
                    logs.append(log)
    data = pd.json_normalize(logs)
    data["memory"] /= 1000
    data["filesize"] /= 1_000_000
    data = data.sort_values(by=["filesize", "k"])

    fig, ax = plt.subplots()
    sns.lineplot(
        ax=ax,
        data=data[data["filename"] == args.input_file],
        x="k",
        y="time",
        hue="tool",
        style="tool",
        markersize=args.marker_size,
        alpha=args.alpha,
        dashes=False,
        palette=PALETTE,
        markers=MARKERS,
    )
    x_left, x_right = ax.get_xlim()
    y_low, y_high = ax.get_ylim()
    ax.set_aspect(abs((x_right-x_left)/(y_low-y_high))*args.ratio)
    ax.set(xlabel="$k$", ylabel="Time (in s)", title="Time vs k")
    plt.savefig((out_dir / "plot_time_vs_k").with_suffix('.' + args.format), dpi=200, bbox_inches="tight", format=args.format)

    fig, ax = plt.subplots()
    sns.lineplot(
        ax=ax,
        data=data[data["filename"] == args.input_file],
        x="k",
        y="memory",
        hue="tool",
        style="tool",
        markersize=args.marker_size,
        alpha=args.alpha,
        dashes=False,
        palette=PALETTE,
        markers=MARKERS,
    )
    x_left, x_right = ax.get_xlim()
    y_low, y_high = ax.get_ylim()
    ax.set_aspect(abs((x_right-x_left)/(y_low-y_high))*args.ratio)
    ax.set(xlabel="$k$", ylabel="Memory usage (in MB)", title="Memory vs k")
    plt.savefig((out_dir / "plot_mem_vs_k").with_suffix('.' + args.format), dpi=200, bbox_inches="tight", format=args.format)

    k = args.kmer_length
    if (k):
        plt.figure()
        ax = sns.barplot(
            data=data[data["k"] == k],
            x="filesize",
            y="time",
            hue="tool",
            palette=PALETTE,
        )
        x_left, x_right = ax.get_xlim()
        y_low, y_high = ax.get_ylim()
        ax.set_aspect(abs((x_right-x_left)/(y_low-y_high))*args.ratio)
        ax.set(xlabel="Input size (in Mb)", ylabel="Time (in s)")
        plt.savefig((out_dir / "plot_time_dataset").with_suffix('.' + args.format), dpi=200, bbox_inches="tight", format=args.format)

        plt.figure()
        ax = sns.barplot(
            data=data[data["k"] == k],
            x="filesize",
            y="memory",
            hue="tool",
            palette=PALETTE,
        )
        x_left, x_right = ax.get_xlim()
        y_low, y_high = ax.get_ylim()
        ax.set_aspect(abs((x_right-x_left)/(y_low-y_high))*args.ratio)
        ax.set(xlabel="Input size (in Mb)", ylabel="Memory usage (in MB)")
        plt.savefig((out_dir / "plot_mem_dataset").with_suffix('.' + args.format), dpi=200, bbox_inches="tight", format=args.format)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("__default")
    subparsers = parser.add_subparsers(dest = "command")

    parser_onk = subparsers.add_parser("onk", help="Run experiments on given dataset by changing k")
    parser_onk.add_argument("-i", "--input-file", help="name of input file containing reads", type=str, required = True)
    parser_onk.add_argument("-o", "--out-dir", help="folder where to store tool's outputs", type=str, required=True)
    parser_onk.add_argument("-g", "--log-dir", help="folder where to store log files", type=str, required=True)
    parser_onk.add_argument("-k", "--kmer-lengths", help="k-mer lengths to test", nargs='+', type=int, required=True)
    parser_onk.add_argument("-K", "--max-k", help="Maximum k, if None then kmer-lengths is considered as a list of values. If != None this is the maximum value to stop in a range and kmer-lengths is expected to be a list of two values: the starting k and the increment", type=int, required=False)
    parser_onk.add_argument("-m", "--minimizer-length", help="minimizer length to be used ", type=int, required=True)
    parser_onk.add_argument("-r", "--threshold", help="minimum count to consider a k-mer solid [2]", type=int, default=2)
    parser_onk.add_argument("-p", "--repeat", help="number of repetitions for each test [1]", type=int, default=1)
    parser_onk.add_argument("-t", "--threads", help="number of threads [8]", type=int, default=8)
    parser_onk.add_argument("-x", "--max-ram", help="Maximum RAM in GB [16]", type=int, default=16)
    parser_onk.add_argument("-d", "--tmp-dir", help="temporary directory [.]", type=str, default=".")
    parser_onk.add_argument("-e", "--timeout", help="timeout for the commands [None]", type=int, default=None)
    parser_onk.add_argument("--tool-indexes", help=f"list of indexes corresponding to available tools to be tested (all by default)\n\t TOOLS = {TOOLS}", type=int, nargs='+', default=[idx for idx in range(len(TOOLS))])
    
    parser_onc = subparsers.add_parser("onc", help="Run experiments by changing coverage of the given dataset")
    parser_onc.add_argument("-i", "--input-file", help="name of input file containing reads", type=str, required = True)
    parser_onc.add_argument("-o", "--out-dir", help="folder where to store tool's outputs", type=str, required=True)
    parser_onc.add_argument("-g", "--log-dir", help="folder where to store log files", type=str, required=True)
    parser_onc.add_argument("-c", "--min-coverage", help="starting coverage to test [1]x", type=int, default=1)
    parser_onc.add_argument("-C", "--max-coverage", help="ending coverage to test", type=int, required=True)
    parser_onc.add_argument("-s", "--step-coverage", help="step in increasing coverage", type=int, required=True)
    parser_onc.add_argument("-l", "--length", help="reference genome size", type=int, required=True)
    parser_onc.add_argument("-k", "--kmer-lengths", help="k-mer lengths to test", nargs='+', type=int, required=True)
    parser_onc.add_argument("-m", "--minimizer-length", help="minimizer length to be used ", type=int, required=True)
    parser_onc.add_argument("-r", "--threshold", help="minimum count to consider a k-mer solid [2]", type=int, default=2)
    parser_onc.add_argument("-p", "--repeat", help="number of repetitions for each test [1]", type=int, default=1)
    parser_onc.add_argument("-t", "--threads", help="number of threads [8]", type=int, default=8)
    parser_onc.add_argument("-x", "--max-ram", help="Maximum RAM in GB [16]", type=int, default=16)
    parser_onc.add_argument("-d", "--tmp-dir", help="temporary directory [.]", type=str, default=".")
    parser_onc.add_argument("-e", "--timeout", help="timeout for the commands [None]", type=int, default=None)
    parser_onc.add_argument("--tool-indexes", help=f"list of indexes corresponding to available tools to be tested (all by default)\n\t TOOLS = {TOOLS}", type=int, nargs='+', default=[idx for idx in range(len(TOOLS))])

    parser_plot = subparsers.add_parser("plot", help="Plot set of experiments")
    parser_plot.add_argument("-i", "--input-file", help="name of input file analyzed", type=str, required = True)
    parser_plot.add_argument("-o", "--out-dir", help="folder where to store the plots", type=str, required=True)
    parser_plot.add_argument("-g", "--log-dir", help="folder where the log files are stored", type=str, required=True)
    parser_plot.add_argument("-k", "--kmer-length", help="specific k-mer length to plot", type=int, required=False)
    parser_plot.add_argument("-r", "--ratio", help="aspect ratio defined as height/length of the plots [0.5]", type=float, default=0.5)
    parser_plot.add_argument("-a", "--alpha", help="alpha (transparency), 1 for solid lines, 0 for invisible lines [0.8]", type=float, default=0.8)
    parser_plot.add_argument("-s", "--marker-size", help="marker size [5]", type=int, default=5)
    parser_plot.add_argument("-f", "--format", help=f"output format [pdf] {PLOT_FORMATS}", type=str, default="pdf")

    args = parser.parse_args(sys.argv)
    if (args.command == "onk"): onk_main(args)
    elif (args.command == "onc"): onc_main(args)
    elif (args.command == "plot"): plot_main(args)
    else: parser.print_help(sys.stderr)