import argparse
import sys
import time

from .config import ConfigData
from . import proc

def begin_stream(channel: str, config: ConfigData):

    # Get the channel info
    channel_info = config.getChannelFromCode(channel)

    # Stop any existing processes
    proc.stop_all()

    # Spawn a new stream
    proc.start_stream(channel_info["frequency"], channel_info["mode"])


def main() -> int:

    # Handle args
    ap = argparse.ArgumentParser()
    ap.add_argument("config_file", help="Config JSON file location")
    args = ap.parse_args()

    # Load the config
    config = ConfigData(args.config_file)

    # Fetch the current channel to listen to
    current_channel = config.getChannelCodeForCurrentTime()

    # Spawn the audio server
    begin_stream(current_channel, config)

    # Busy loop
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        proc.stop_all()

    return 0

if __name__ == "__main__":
    sys.exit(main())