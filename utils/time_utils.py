import ntptime
import time

def sync_time():

    try:

        ntptime.settime()

        print("Time synced with NTP")

    except Exception as e:

        print("NTP sync failed:", e)

def current_iso_time():

    t = time.localtime()

    return "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        t[0],
        t[1],
        t[2],
        t[3],
        t[4],
        t[5]
    )