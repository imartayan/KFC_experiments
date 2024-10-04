from tools import KFC, KMC, FASTK, JELLYFISH, GERBIL, KAARME

TOOLS = [
    KFC,
    KMC,
    FASTK,
    # JELLYFISH,
    # GERBIL,
    # KAARME,
]

MAIN_FILE = "reads.fa"

DATASET = [
    "reads1.fa",
    "reads2.fa",
    "reads3.fa",
]
DEFAULT_K = 151

if __name__ == "__main__":
    for k in [63, 99, 127, 151, 199, 251, 299]:
        print(f"Counting {k}-mers in {MAIN_FILE}")
        for tool in TOOLS:
            tool.run(MAIN_FILE, k=k, m=21, threshold=2, threads=8, max_ram=16, repeat=5)
            # see tools.py for all the parameters used by the different tools

    for fasta_file in DATASET:
        for tool in TOOLS:
            tool.run(fasta_file, k=DEFAULT_K, threads=8, repeat=5)
