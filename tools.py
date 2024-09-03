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
        print("KMC requires k ≤ 256")
        return None
    t = select_param("threads", params, 1)
    ci = select_param("threshold", params, 2)
    filetype = "-fa" if (".fa" in fasta or ".fasta" in fasta) else "-fq"
    out = f"out/{basename(fasta)}"
    return [f"./KMC/kmc {filetype} -k{k} -t{t} -ci{ci} {fasta} {out} tmp"]


KMC = Tool("KMC", kmc_cmd)


def fastk_cmd(fasta, **params):
    k = select_param("k", params, 31)
    T = select_param("threads", params, 1)
    t = select_param("threshold", params, 2)
    out = f"out/{basename(fasta)}"
    return [f"./FASTK/FastK -v -k{k} -t{t} -T{T} {fasta} -N{out}"]


FASTK = Tool("FASTK", fastk_cmd)


def jellyfish_cmd(fasta, **params):
    k = select_param("k", params, 31)
    if k > 64:
        print("Jellyfish requires k ≤ 64")
        return None
    t = select_param("threads", params, 1)
    s_bf = select_param("bloom_filter_size", params, "1G")
    s_ht = select_param("hash_table_size", params, "10M")
    out_bc = f"out/{basename(fasta)}.bc"
    out = f"out/{basename(fasta)}.jf"
    cmd = []
    if fasta.endswith(".gz"):
        unzipped = f"out/{basename(fasta)}.fa"
        cmd.append(f"gzip -cd {fasta} > {unzipped}")
        fasta = unzipped
    return cmd + [
        f"./jellyfish/bin/jellyfish bc -C -m {k} -s {s_bf} -t {t} {fasta} -o {out_bc} --timing=/dev/stdout",
        f"./jellyfish/bin/jellyfish count -C -m {k} -s {s_ht} -t {t} --bc {out_bc} {fasta} -o {out} --timing=/dev/stdout",
    ]


JELLYFISH = Tool("Jellyfish", jellyfish_cmd)


def gerbil_cmd(fasta, **params):
    k = select_param("k", params, 31)
    # m = select_param("m", params, 21)
    t = select_param("threads", params, 1)
    l = select_param("threshold", params, 2)
    out = f"out/{basename(fasta)}"
    return [f"./gerbil/build/gerbil -k {k} -t {t} -l {l} {fasta} tmp {out}"]


GERBIL = Tool("Gerbil", gerbil_cmd)


def kaarme_cmd(fasta, **params):
    k = select_param("k", params, 31)
    t = select_param("threads", params, 1)
    a = select_param("threshold", params, 2)
    s = select_param("hash_table_size", params, 100000000)
    out = f"out/{basename(fasta)}.kaarme"
    return [f"./kaarme/build/kaarme -a {a} -t {t} {fasta} {k} -s {s} -o {out}"]


KAARME = Tool("Kaarme", kaarme_cmd)
