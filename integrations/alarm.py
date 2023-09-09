import json
import threading
import time
from datetime import datetime

class Alarm:
    list_alarms = json.load(open("../json_files/alarms.json", "r"))

    @classmethod
    def start_alarm_initialisation(cls):
        for alarm in cls.list_alarms:
            date_time_alarm = datetime.strptime(f"{cls.list_alarms[alarm]['date']}_{cls.list_alarms[alarm]['time']}",
                                                "%Y-%m-%d_%H:%M")
            difference = date_time_alarm - datetime.now()
            if str(difference).__contains__(","):
                days, time = str(date_time_alarm - datetime.now()).replace(" days", "").split(",")
            else:
                days = 0
                time = difference
            seconds = cls.transform_day_to_seconds(int(days)) + cls.transform_time_to_seconds(time)
            print("Seconds till alarm time:", seconds)
            new_thread = threading.Timer(seconds, cls.test_code, args=(alarm,))
            new_thread.start()

    @classmethod
    def test_code(cls, description):
        print(f"called from function test_code: {description}")
    @classmethod
    def transform_day_to_seconds(cls, total_days):
        return total_days * 86400
    @classmethod
    def transform_time_to_seconds(cls, time_stamp):
        time_data = str(time_stamp).split(":")
        hour_to_seconds = int(time_data[0]) * 3600
        minute_to_seconds = int(time_data[1]) * 60
        seconds = int(time_data[2].split(".")[0])
        return hour_to_seconds + minute_to_seconds + seconds - 2
    @classmethod
    def create_alarm(cls):
        pass

    @classmethod
    def update_alarm(cls):
        pass

    @classmethod
    def read_alarm(cls):
        pass

    @classmethod
    def remove_alarm(cls):
        pass

int_alarm = Alarm()
int_alarm.start_alarm_initialisation()
