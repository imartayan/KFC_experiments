import json
import os
import platform
import struct
import subprocess
import sys

GNU_TIME = "/usr/bin/time" if platform.system() == "Linux" else "gtime"  # not clean


class Tool:
    def __init__(self, name, cmd, postprocess=None, log_dir="logs"):
        self.name = name
        self.cmd = cmd
        self.postprocess = postprocess
        self.log_dir = log_dir

    def name(self):
        return self.name

    def log_dir(self):
        return self.log_dir

    def set_log_dir(self, log_dir):
        self.log_dir = log_dir

    def log(self, input_file, time, memory, **params):
        os.makedirs(self.log_dir, exist_ok=True)
        name = basename(input_file)
        size = filesize(input_file)
        attrs = [self.name, name, str(size // 10**6)] + [
            f"{k}{v}" for (k, v) in params.items()
        ]
        json_file = f"{self.log_dir}/{"_".join(attrs)}.json"
        update_json(
            json_file,
            tool=self.name,
            time=time,
            memory=memory,
            filename=input_file,
            filesize=size,
            **params,
        )

    def run(self, input_file, repeat=1, timeout=None, **params):
        if not os.path.exists(input_file):
            print(f"{input_file} does not exist")
            return None
        os.makedirs("out", exist_ok=True)
        os.makedirs("tmp", exist_ok=True)
        cmd = self.cmd(input_file, **params)
        if cmd is None:
            return None
        time, memory, out, err = benchmark(cmd, repeat=repeat, timeout=timeout)
        if self.postprocess is not None:
            time, memory = self.postprocess(time, memory, out, err)
        self.log(input_file, time, memory, **params)


def select_param(key, params, default=None):
    if key in params:
        return params[key]
    elif default is not None:
        print(f"Using {key}={default} by default")
        return default
    else:
        raise Exception(f"{key} is missing from params")


def basename(filename):
    return os.path.basename(filename).split(".")[0]


def filesize(filename):
    if filename.endswith(".gz"):
        with open(filename, "rb") as f:
            f.seek(-4, 2)
            return struct.unpack("I", f.read(4))[0]
    else:
        return os.path.getsize(filename)


def update_json(json_file, **fields):
    if os.path.exists(json_file):
        with open(json_file, "r") as f:
            data = json.load(f)
            data |= fields
    else:
        data = fields
    with open(json_file, "w+") as f:
        json.dump(data, f)


def execute(*commands, timeout=None):
    for command in commands:
        sys.stderr.write("> " + command + "\n")
        try:
            proc = subprocess.run(
                command,
                shell=True,
                check=True,
                timeout=timeout,
                capture_output=True,
                text=True,
            )
            out, err = proc.stdout, proc.stderr
            if out is not None:
                sys.stdout.write(out + "\n")
            if err is not None:
                sys.stderr.write(err + "\n")
            return out, err
        except subprocess.SubprocessError as proc:
            out, err = proc.stdout, proc.stderr
            if isinstance(out, bytes):
                out = out.decode("utf-8")
            if isinstance(out, str):
                sys.stdout.write(out + "\n")
            if isinstance(err, bytes):
                err = err.decode("utf-8")
            if isinstance(err, str):
                sys.stderr.write(err + "\n")
            return None, None


def benchmark(*commands, repeat=1, timeout=None):
    total_time, total_memory = 0, 0
    for _ in range(repeat):
        for command in commands:
            out, err = execute(f"{GNU_TIME} -f '%e %M' {command}", timeout=timeout)
            try:
                time, memory = list(map(float, err.splitlines()[-1].split()))
                total_time += time
                total_memory = max(total_memory, memory)
            except Exception:
                return float("inf"), float("inf"), out, err  # fix?
    average_time = total_time / repeat
    average_memory = total_memory / repeat
    return average_time, average_memory, out, err
