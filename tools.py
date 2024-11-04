import os
import typing
import pathlib
from tool import Tool, basename

def select_param(key: typing.Any, 
                 params: typing.Any, 
                 default: typing.Any | None = None
                 ) -> typing.Any:
    if key in params:
        return params[key]
    elif default is not None:
        print(f"Using {key}={default} by default")
        return default
    else:
        raise Exception(f"{key} is missing from params")

def kfc_cmd(fasta: os.PathLike, 
            out_dir: os.PathLike, 
            tmp_dir: os.PathLike, 
            **params
            ) -> str:
    k = select_param("k", params, 31)
    m = select_param("m", params, 21)
    t = select_param("threshold", params, 2)
    out = pathlib.Path(out_dir)/basename(fasta)
    return [f"./KFC/kfc build -k {k} -m {m} -t {t} -i {fasta} -o {out} -f"]

def kmc_cmd(fasta: os.PathLike, 
            out_dir: os.PathLike, 
            tmp_dir: os.PathLike, 
            **params
            ) -> str:
    def kmc_filetype_option(filename: str) -> str:
        if ".fa" in filename or ".fasta" in filename: return "-fa"
        elif ".fq" in filename or ".fastq" in filename: return "-fq"
        else: raise RuntimeError("[KMC] unrecognized file format")

    k = select_param("k", params, 31)
    t = select_param("threads", params, 1)
    ci = select_param("threshold", params, 2)
    m = select_param("max_ram", params, 12)
    filetype = kmc_filetype_option(str(fasta))
    out = pathlib.Path(out_dir)/basename(fasta)
    return [f"./KMC/kmc {filetype} -k{k} -ci{ci} -t{t} -m{m} {fasta} {out} {tmp_dir}"]

def fastk_cmd(fasta: os.PathLike, 
              out_dir: os.PathLike, 
              tmp_dir: os.PathLike, 
              **params
              ) -> str:
    # assert type(fasta) is str
    # assert type(out_dir) is str
    # assert type(tmp_dir) is str
    k = select_param("k", params, 31)
    T = select_param("threads", params, 1)
    t = select_param("threshold", params, 2)
    M = select_param("max_ram", params, 12)
    out = pathlib.Path(out_dir)/basename(fasta)
    return [f"./FASTK/FastK -v -k{k} -t{t} -T{T} -M{M} {fasta} -N{out}"]

def jellyfish_cmd(fasta: os.PathLike, 
                  out_dir: os.PathLike, 
                  tmp_dir: os.PathLike, 
                  **params
                  ) -> str:
    k = select_param("k", params, 31)
    t = select_param("threads", params, 1)
    s_bf = select_param("bloom_filter_size", params, "1G")
    s_ht = select_param("hash_table_size", params, "10M")
    out_bc = pathlib.Path(out_dir)/f"{basename(fasta)}.bc"
    out = pathlib.Path(out_dir)/f"{basename(fasta)}.jf"
    cmd = []
    if fasta.suffix == ".gz":
        unzipped = pathlib.Path(out_dir)/f"{basename(fasta)}.fa"
        cmd.append(f"gzip -cd {fasta} > {unzipped}")
        fasta = unzipped
    return cmd + [
        f"./jellyfish/bin/jellyfish bc -C -m {k} -s {s_bf} -t {t} {fasta} -o {out_bc} --timing=/dev/stdout",
        f"./jellyfish/bin/jellyfish count -C -m {k} -s {s_ht} -t {t} --bc {out_bc} {fasta} -o {out} --timing=/dev/stdout",
    ]

def gerbil_cmd(fasta: os.PathLike, 
               out_dir: os.PathLike, 
               tmp_dir: os.PathLike, 
               **params
               ) -> str:
    k = select_param("k", params, 31)
    t = select_param("threads", params, 1)
    l = select_param("threshold", params, 2)
    out = pathlib.Path(out_dir)/basename(fasta)
    return [f"./gerbil/build/gerbil -k {k} -t {t} -l {l} {fasta} {tmp_dir} {out}"]

def kaarme_cmd(fasta: os.PathLike, 
               out_dir: os.PathLike, 
               tmp_dir: os.PathLike, 
               **params
               ) -> str:
    k = select_param("k", params, 31)
    t = select_param("threads", params, 1)
    a = select_param("threshold", params, 2)
    s = select_param("hash_table_size", params, 100000000)
    out = pathlib.Path(out_dir)/f"{basename(fasta)}.kaarme"
    return [f"./kaarme/build/kaarme -a {a} -t {t} {fasta} {k} -s {s} -o {out}"]

KFC = Tool("KFC", kfc_cmd)
KMC = Tool("KMC", kmc_cmd)
FASTK = Tool("FASTK", fastk_cmd)
JELLYFISH = Tool("Jellyfish", jellyfish_cmd)
GERBIL = Tool("Gerbil", gerbil_cmd)
KAARME = Tool("Kaarme", kaarme_cmd)

TOOLS = [
    KFC,
    KMC,
    FASTK,
    JELLYFISH,
    GERBIL,
    KAARME
]
