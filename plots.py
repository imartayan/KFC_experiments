from tools import TOOLS
from main import MAIN_FILE
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
}
PALETTE = {
    "KFC": "tab:blue",
    "KMC": "tab:green",
    "FASTK": "tab:red",
    "Jellyfish": "tab:purple",
    "Gerbil": "tab:orange",
}
LABEL = {t: t for t in MARKERS} | {
    "time": "Construction time (in s)",
    "mem": "RAM usage during construction (in MB)",
}

LOG_DIRS = set(tool.log_dir for tool in TOOLS)
LOGS = []
for log_dir in LOG_DIRS:
    for log_file in os.listdir(log_dir):
        with open(f"{log_dir}/{log_file}") as f:
            LOGS.append(json.load(f))
DATA = pd.json_normalize(LOGS)
DATA["memory"] /= 1000

os.makedirs(PLOT_DIR, exist_ok=True)

plt.figure()
sns.lineplot(
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
plt.savefig(f"{PLOT_DIR}/plot_time_vs_k.png")

plt.figure()
sns.lineplot(
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
plt.savefig(f"{PLOT_DIR}/plot_mem_vs_k.png")
