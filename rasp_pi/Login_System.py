# The code will throw an error / problemm as the imports are for a micropython enviroment but all code works with rasp pi.
from machine import Pin
from mfrc522 import MFRC522
import utime 
import time
from machine import RTC

# PiicoDev modules
from PiicoDev_SSD1306 import *
from PiicoDev_TMP117 import PiicoDev_TMP117
from PiicoDev_RGB import PiicoDev_RGB
from PiicoDev_Unified import sleep_ms

# Real Time Clock Setup
rtc = RTC()
rtc.datetime((2026, 6, 24, 2, 9, 33, 0, 0))
# (year, month, day, weekday, hour, minute, second, subseconds)


# Timestamp Helper - AI help
def get_timestamp():
    dt = rtc.datetime()
    date_str = "{:04d}-{:02d}-{:02d}".format(dt[0], dt[1], dt[2])
    time_str = "{:02d}:{:02d}:{:02d}".format(dt[4], dt[5], dt[6])
    return date_str, time_str

# RFID setup
reader = MFRC522(spi_id=0, sck=6, miso=4, mosi=7, cs=5, rst=22)

# PiicoDev devices
oled = create_PiicoDev_SSD1306()
tempSensor = PiicoDev_TMP117()
rgb = PiicoDev_RGB()

# CSV LOOKUP FUNCTION - AI used to fix CSV writing, as previous code was reading correctly but not writing and fixed formating.
def lookup_tag(tag_number):
    try:
        with open("registered_tags.csv") as f:
            raw_header = f.readline().strip().split(",")
            header = [h.strip().lower().replace(" ", "_") for h in raw_header]

            for line in f:
                parts = [p.strip() for p in line.strip().split(",")]
                row = dict(zip(header, parts))

                if row.get("tag") == str(tag_number):

                    date_str, time_str = get_timestamp() #AI Help

                    with open("attendance.csv", "a") as af:
                        af.write("{},{},{},{},{}\n".format(row.get("Tag"), row.get("FirstName"), row.get("LastName"), date_str, time_str))
                    return row

    except Exception as e:
        print("CSV read error:", e)

    return None

# LED FUNCTIONS
def led_green():
    rgb.setPixel(0, (0, 255, 0))
    rgb.show()

def led_blue():
    rgb.setPixel(0, (0, 0, 255))
    rgb.show()

def led_red():
    rgb.setPixel(0, (255, 0, 0))
    rgb.show()

def led_off():
    rgb.setPixel(0, (0, 0, 0))
    rgb.show()


# OLED SCREENS - AI used to fix displaying of CSV.
def idle_screen():
    temperature = tempSensor.readTempC()
    oled.fill(0)
    oled.text("Waiting for card", 0, 0)
    oled.text("Temp: {:.1f}C".format(temperature), 0, 20)
    oled.show()

# CSV displaying info to OLED using tag ID.
def show_scan_result(info):
    oled.fill(0)

    oled.text("FN: {}".format(info.get("firstname", "")), 0, 0)
    oled.text("Surname: {}".format(info.get("lastname", "")), 0, 12)
    oled.text("Role: {}".format(info.get("role", "N/A")), 0, 24)
    oled.text("Tag: {}".format(info.get("tag", "N/A")), 0, 36)

    oled.show()



# MAIN - Modified from tutorial code to work with OLED and RGB. https://how2electronics.com/using-rc522-rfid-reader-module-with-raspberry-pi-pico/
while True:
    idle_screen()

    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)

    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid), "little", False)
            print("Scanned:", card)

            info = lookup_tag(card)

            if info:
                role = info["role"]

                # LED logic based on role
                if role.lower() == "teacher":
                    led_green()
                elif role.lower() == "student":
                    led_blue()
                else:
                    led_red()

                show_scan_result(info)

            else:
                print("UNKNOWN CARD")
                led_red()
                show_scan_result({
                    "first_name": "Unknown",
                    "last_name": "",
                    "role": "No Access",
                    "tag": card
                })

            utime.sleep(2)
            led_off()
    
    utime.sleep(0.2)
