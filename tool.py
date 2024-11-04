import os
import sys
import pathlib
import json
import typing
import struct
import subprocess

class Tool:
    def __init__(self, 
                 name: str, 
                 cmd: str, 
                 postprocess: typing.Callable[[int, int, str, str], tuple[int, int]] | None=None
                 ):
        assert name
        assert cmd
        self.name = name
        self.cmd = cmd
        self.postprocess = postprocess

    def log(self, 
            log_dir: os.PathLike, 
            input_file: os.PathLike, 
            time: float, 
            memory: int, 
            **params
            ) -> typing.NoReturn:
        
        def filesize(filename: os.PathLike) -> int:
            if filename.suffix == ".gz":
                with open(filename, "rb") as f:
                    f.seek(-4, 2)
                    return struct.unpack("I", f.read(4))[0]
            else:
                return filename.stat().st_size

        def update_json(json_file: os.PathLike, **fields) -> typing.NoReturn:
            if json_file.exists():
                with open(json_file, "r") as f:
                    data = json.load(f)
                    data |= fields
            else:
                data = fields
            with open(json_file, "w+") as f:
                json.dump(data, f)
        
        name = basename(input_file)
        size = filesize(input_file)
        attrs = "_".join(
            [self.name, name, str(size // 10**6)]
            + [f"{k}{v}" for (k, v) in params.items()]
        )
        json_file = log_dir/f"{attrs}.json"
        update_json(
            json_file,
            tool=self.name,
            time=time,
            memory=memory,
            filename=str(input_file), # Path objects are not serializable
            filesize=size,
            **params,
        )

    def run(self, 
            input_file: os.PathLike, 
            out_dir: os.PathLike, 
            log_dir: os.PathLike, 
            tmp_dir: os.PathLike, 
            repeat: int, 
            timeout: int | None, 
            **params
            ) -> typing.NoReturn:
        
        def benchmark(*commands, 
                      repeat: int, 
                      timeout: int | None
                      ) -> tuple[float, float, str, str]:
            TIME_EXE, _ = execute("which time")
            TIME_EXE = TIME_EXE.rstrip()
            total_time, total_memory = 0, 0
            for _ in range(repeat):
                for command in commands:
                    sys.stderr.write("> " + command + "\n")
                    out, err = execute(f"{TIME_EXE} -f '%e %M' {command}", timeout=timeout)
                    try:
                        time, memory = list(map(float, err.splitlines()[-1].split()))
                        total_time += time
                        total_memory = max(total_memory, memory)
                    except Exception:
                        return None
            average_time = total_time / repeat
            average_memory = total_memory / repeat
            return average_time, average_memory, out, err
        
        cmd = self.cmd(input_file, out_dir, tmp_dir, **params)
        result = benchmark(*cmd, repeat=repeat, timeout=timeout)
        if result:
            time, memory, out, err = result
            if self.postprocess is not None:
                time, memory = self.postprocess(time, memory, out, err)
            self.log(log_dir, input_file, time, memory, **params)
        else:
            print(f"{self.name} failed during execution")

def basename(filepath: str | os.PathLike) -> str:
    filepath = pathlib.Path(filepath)
    if filepath.suffixes:
        first_suffix = filepath.suffixes[0]
        return filepath.name.split(first_suffix)[0]
    else:
        return filepath.name
    # return os.path.basename(filename).split(".")[0]

def execute(*commands, 
            timeout: int | None=None
            ) -> tuple[str | None, str | None]:
    for command in commands:
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


