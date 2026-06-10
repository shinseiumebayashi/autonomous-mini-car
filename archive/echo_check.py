import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN)

print("Echo pin状態モニター（Ctrl+C で終了）")
try:
    while True:
        state = GPIO.input(24)
        print(f"Echo: {state}")
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()