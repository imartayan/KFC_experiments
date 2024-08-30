from tool import Tool, select_param, basename


def kfc_cmd(fasta, **params):
    k = select_param("k", params, 31)
    m = select_param("m", params, 21)
    t = select_param("threshold", params, 2)
    out = f"out/{basename(fasta)}"
    return [f"./KFC/kfc build -k {k} -m {m} -t {t} -i {fasta} -o {out} -f"]


KFC = Tool("KFC", kfc_cmd)


def kmc_cmd(fasta, **params):
    k = select_param("k", params, 31)
    if k > 256:
        return None
    t = select_param("threads", params, 1)
    ci = select_param("threshold", params, 2)
    out = f"out/{basename(fasta)}"
    return [f"./KMC/kmc -fa -k{k} -t{t} -ci{ci} {fasta} {out} tmp"]


KMC = Tool("KMC", kmc_cmd)


def fastk_cmd(fasta, **params):
    k = select_param("k", params, 31)
    T = select_param("threads", params, 1)
    t = select_param("threshold", params, 2)
    out = f"out/{basename(fasta)}"
    return [f"./FASTK/FastK -v -k{k} -t{t} -T{T} {fasta} -N{out}"]


FASTK = Tool("FASTK", fastk_cmd)


TOOLS = [
    KFC,
    KMC,
    FASTK,
]
