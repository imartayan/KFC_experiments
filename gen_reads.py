from random import choices, choice, random, randrange
from sys import argv

BASES = ["A", "C", "G", "T"]


def gen_seq(seq_len):
    return choices(BASES, k=seq_len)


def mut_seq(seq, error_rate=0.005, indels=0.5):
    mut = []
    for base in seq:
        r = random()
        if r > error_rate:
            mut.append(base)
        elif r > error_rate * indels:
            mut.append(choice(BASES))
        elif r > error_rate * indels / 2:
            mut.append(choice(BASES))
            mut.append(base)
    return mut


def gen_reads(seq, read_len=20000, coverage=10, **args):
    reads = []
    for _ in range(len(seq) * coverage // read_len):
        mid = randrange(0, len(seq))
        start = max(0, mid - read_len // 2)
        stop = min(len(seq), mid + read_len // 2)
        reads.append(mut_seq(seq[start:stop], **args))
    return reads


if __name__ == "__main__":
    try:
        seq_len = int(argv[1])
    except Exception:
        seq_len = 1000000
    seq = gen_seq(seq_len)
    reads = gen_reads(seq)
    for i, read in enumerate(reads, start=1):
        print(f">{i}")
        print("".join(read))
