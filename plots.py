from tools import TOOLS
from main import MAIN_FILE, DEFAULT_K
import os
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


PLOT_DIR = "plots"
PLOT_FORMAT = ".png"
FONT_SIZE = 14
MARKER_SIZE = 10
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
LABEL = {t: t for t in MARKERS} | {
    "time": "Construction time (in s)",
    "mem": "RAM usage during construction (in MB)",
}

TOOL_NAMES = [tool.name for tool in TOOLS]
LOG_DIRS = set(tool.log_dir for tool in TOOLS)
LOGS = []
for log_dir in LOG_DIRS:
    for log_file in os.listdir(log_dir):
        with open(f"{log_dir}/{log_file}") as f:
            log = json.load(f)
            if log["tool"] in TOOL_NAMES:
                LOGS.append(log)
DATA = pd.json_normalize(LOGS)
DATA["memory"] /= 1000
DATA["filesize"] /= 1_000_000
DATA = DATA.sort_values(by=["filesize", "k"])

os.makedirs(PLOT_DIR, exist_ok=True)

plt.figure()
ax = sns.lineplot(
    data=DATA[DATA["filename"] == MAIN_FILE],
    x="k",
    y="time",
    hue="tool",
    palette=PALETTE,
    style="tool",
    markers=MARKERS,
    dashes=False,
    markersize=MARKER_SIZE,
    alpha=0.5,
)
ax.set(xlabel="$k$", ylabel="Time (in s)")
plt.savefig(f"{PLOT_DIR}/plot_time_vs_k.png")

plt.figure()
ax = sns.lineplot(
    data=DATA[DATA["filename"] == MAIN_FILE],
    x="k",
    y="memory",
    hue="tool",
    palette=PALETTE,
    style="tool",
    markers=MARKERS,
    dashes=False,
    markersize=MARKER_SIZE,
    alpha=0.5,
)
ax.set(xlabel="$k$", ylabel="Memory usage (in MB)")
plt.savefig(f"{PLOT_DIR}/plot_mem_vs_k.png")

plt.figure()
ax = sns.barplot(
    data=DATA[DATA["k"] == DEFAULT_K],
    x="filesize",
    y="time",
    hue="tool",
    palette=PALETTE,
)
ax.set(xlabel="Input size (in Mb)", ylabel="Time (in s)")
plt.savefig(f"{PLOT_DIR}/plot_time_dataset.png")

plt.figure()
ax = sns.barplot(
    data=DATA[DATA["k"] == DEFAULT_K],
    x="filesize",
    y="memory",
    hue="tool",
    palette=PALETTE,
)
ax.set(xlabel="Input size (in Mb)", ylabel="Memory usage (in MB)")
plt.savefig(f"{PLOT_DIR}/plot_mem_dataset.png")
