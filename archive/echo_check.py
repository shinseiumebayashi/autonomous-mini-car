"""
HC-SR04 Echo pin diagnostic
HC-SR04 Echoピン診断ツール

Monitors the Echo pin state to debug ultrasonic sensor wiring.
Echoピンの状態を監視し、超音波センサーの配線問題をデバッグする。
"""

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN)

print("Echo pin state monitor (Ctrl+C to exit)")
print("Echoピン状態モニター（Ctrl+C で終了）")
try:
    while True:
        state = GPIO.input(24)
        print(f"Echo: {state}")
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()