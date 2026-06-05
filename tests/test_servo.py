"""
Servo control test using the new ServoController class.
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.servo import ServoController


def main():
    servo = ServoController()
    print("Servo test using ServoController class")

    try:
        print("Center")
        servo.center()
        time.sleep(1)

        print("Left")
        servo.left()
        time.sleep(1)

        print("Right")
        servo.right()
        time.sleep(1)

        print("Back to center")
        servo.center()
        time.sleep(1)

        print("Sweep from -1.0 to 1.0")
        for i in range(-10, 11):
            angle = i / 10.0
            print(f"  angle = {angle:.1f}")
            servo.set_angle(angle)
            time.sleep(0.2)

        servo.center()

    finally:
        servo.cleanup()
        print("Done")


if __name__ == "__main__":
    main()
