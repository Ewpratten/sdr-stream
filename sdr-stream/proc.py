"""Handles subprocess management"""

import subprocess
from typing import Optional
import signal

# Subprocesses used to handle data
_rtl_fm_proc: Optional[subprocess.Popen] = None
_sox_proc: Optional[subprocess.Popen] = None
_cvlc_proc: Optional[subprocess.Popen] = None

def stop_all():
    global _rtl_fm_proc, _sox_proc, _cvlc_proc

    for proc, name in [(_cvlc_proc, "cvlc"), (_sox_proc, "sox"), (_rtl_fm_proc, "rtl_fm")]:
        if proc:
            print(f"Sending SIGKILL to process: {name}")
            proc.send_signal(sig=signal.SIGKILL)
            proc.wait()

def start_stream(frequency: str, mode: str):
    global _rtl_fm_proc, _sox_proc, _cvlc_proc

    # Begin rtl_fm
    command = f"rtl_fm -g50 -f {frequency} -M {mode} -s 180k -E deemp".split(" ")
    print(f"Spawning process: {command}")
    _rtl_fm_proc = subprocess.Popen(command, stdout=subprocess.PIPE)

    # Begin sox
    command = f"sox -traw -r180k -es -b16 -c1 -V1 - -t flac -".split(" ")
    print(f"Spawning process: {command}")
    _sox_proc = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=_rtl_fm_proc.stdout)

    # Begin vlc
    command = "cvlc - --sout '#standard{access=http,mux=ogg}' --http-host localhost".split(" ")
    print(f"Spawning process: {command}")
    _cvlc_proc = subprocess.Popen(command, stdin=_sox_proc.stdout)