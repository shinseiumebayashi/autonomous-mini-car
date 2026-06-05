"""
HC-SR04 ultrasonic distance sensor.
"""

import RPi.GPIO as GPIO
import time
from . import config


class UltrasonicSensor:
    """HC-SR04 距離測定"""

    def __init__(self):
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BCM)

        GPIO.setup(config.ULTRASONIC_TRIG, GPIO.OUT)
        GPIO.setup(config.ULTRASONIC_ECHO, GPIO.IN)
        GPIO.output(config.ULTRASONIC_TRIG, False)
        time.sleep(0.1)

    def measure(self):
        """距離をcmで返す。タイムアウトの場合は-1"""
        # トリガパルス
        GPIO.output(config.ULTRASONIC_TRIG, True)
        time.sleep(0.00001)
        GPIO.output(config.ULTRASONIC_TRIG, False)

        # エコー立ち上がり待ち
        pulse_start = time.time()
        timeout = pulse_start + 0.04
        while GPIO.input(config.ULTRASONIC_ECHO) == 0:
            pulse_start = time.time()
            if pulse_start > timeout:
                return -1

        # エコー立ち下がり待ち
        pulse_end = time.time()
        timeout = pulse_end + 0.04
        while GPIO.input(config.ULTRASONIC_ECHO) == 1:
            pulse_end = time.time()
            if pulse_end > timeout:
                return -1

        # 距離計算（音速343m/s、往復なので2で割る）
        duration = pulse_end - pulse_start
        distance = duration * 34300 / 2
        return round(distance, 2)