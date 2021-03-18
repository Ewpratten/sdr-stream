"""Handles subprocess management"""

import subprocess
from typing import Optional
import signal

# Subprocesses used to handle data
_stream_proc: Optional[subprocess.Popen] = None

def stop_all():
    global _stream_proc

    for proc, name in [(_stream_proc, "rtl_fm")]:
        if proc:
            print(f"Sending SIGKILL to process: {name}")
            proc.send_signal(sig=signal.SIGKILL)
            proc.wait()

def start_stream(frequency: str, mode: str, squelch: int):
    global _stream_proc_stream_proc

    # Begin rtl_fm
    command = f"rtl_fm -g 50 -f {frequency} -M {mode} -s 48k -E deemp -A fast -l {squelch} | sox -traw -r 48k -es -b16 -c1 -V1 - -t mp3 - | cvlc - --sout '#standard{{access=http,mux=mp3}}' --http-host localhost"
    print(f"Spawning process: {command}")
    _stream_proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
