"""Handles interaction with the config file"""

import json
import datetime
from typing import Optional


class ConfigData(object):

    _object: dict

    def __init__(self, file_path: str) -> None:

        with open(file_path, "r") as fp:
            print(f"Loading JSON config from: {file_path}")
            self._object = json.load(fp)

    def getCurrentScheduledChannelOrNone(self) -> Optional[dict]:

        # Get the current time in both local and utc formats
        cur_time_local = datetime.datetime.now().time()
        cur_time_utc = datetime.datetime.utcnow().time()
        cur_day_num = datetime.datetime.now().weekday() - 1

        # Try to find a better match
        for entry in self._object["schedule"]:
            if cur_day_num in entry["days"]:

                # Get the specified start and end times
                start_time = entry["time"]["start"]
                start_time = datetime.time(
                    int(start_time.split(":")[0]), int(start_time.split(":")[1]))

                end_time = entry["time"]["end"]
                end_time = datetime.time(
                    int(end_time.split(":")[0]), int(end_time.split(":")[1]))

                is_utc = entry["time"]["utc"]

                # Check if the current time falls in the timeslot
                if is_utc:
                    if cur_time_utc >= start_time and cur_time_utc <= end_time:
                        return entry
                else:
                    if cur_time_local >= start_time and cur_time_local <= end_time:
                        return entry

    def getChannelCodeForCurrentTime(self) -> str:

        current_channel = self.getCurrentScheduledChannelOrNone()

        if not current_channel:
            current_channel = self._object["default_channel"]
        else:
            current_channel = current_channel["channel"]

        return current_channel

    def getChannelFromCode(self, channel_code: str) -> dict:
        return self._object["channels"][channel_code]
