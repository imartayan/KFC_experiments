from tools import TOOLS

FASTA_FILE = "reads.fa"

DATASET = [
    "reads1.fa",
    "reads2.fa",
    "reads3.fa",
]
DEFAULT_K = 99

for k in [31, 63, 99, 127, 151, 199]:
    print(f"Counting {k}-mers in {FASTA_FILE}")
    for tool in TOOLS:
        tool.run(FASTA_FILE, k=k, threads=8, repeat=5)

for fasta_file in DATASET:
    for tool in TOOLS:
        tool.run(fasta_file, k=DEFAULT_K, threads=8, repeat=5)
