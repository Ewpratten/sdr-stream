import argparse
import sys
import time
import sched

from .config import ConfigData
from . import proc

# Tracker for the current channel
current_channel = None

def begin_stream(channel: str, config: ConfigData):

    # Get the channel info
    channel_info = config.getChannelFromCode(channel)

    # Stop any existing processes
    proc.stop_all()

    # Spawn a new stream
    proc.start_stream(channel_info["frequency"], channel_info["mode"], channel_info["squelch"])

def handle_frequency_switch(config: ConfigData):
    global current_channel

    while True:

        # Fetch the current channel to listen to
        new_channel = config.getChannelCodeForCurrentTime()

        # Handle channel switch
        if new_channel != current_channel:
            print(f"Switching to channel: {new_channel}")
            begin_stream(new_channel, config)
            current_channel = new_channel

        time.sleep(60)


def main() -> int:
    global current_channel

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

    # Set up a scheduler
    scheduler = sched.scheduler(time.time, time.sleep)

    # Run
    try:
        scheduler.enter(60, 1, handle_frequency_switch, (config,))
        scheduler.run()
    except KeyboardInterrupt:
        pass

    proc.stop_all()
    return 0

if __name__ == "__main__":
    sys.exit(main())