"""
Ultrasonic sensor test using the new UltrasonicSensor class.
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ultrasonic import UltrasonicSensor


def main():
    sensor = UltrasonicSensor()
    print("Ultrasonic sensor test (Ctrl+C to stop)")

    try:
        while True:
            distance = sensor.measure()
            if distance < 0:
                print("Timeout (measurement failed)")
            elif distance > 400:
                print(f"Out of range: {distance} cm")
            else:
                print(f"Distance: {distance} cm")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStopped")


if __name__ == "__main__":
    main()
