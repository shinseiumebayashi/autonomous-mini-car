"""
Motor control test using the new MotorController class.
"""

import sys
import os
import time

# 親ディレクトリを Python パスに追加（src/ をインポートできるように）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.motor import MotorController


def main():
    motor = MotorController()
    print("Motor test using MotorController class")

    try:
        print("Forward 50% for 2 seconds")
        motor.forward(50)
        time.sleep(2)

        print("Stop for 1 second")
        motor.stop()
        time.sleep(1)

        print("Backward 50% for 2 seconds")
        motor.backward(50)
        time.sleep(2)

        motor.stop()

    finally:
        motor.cleanup()
        print("Done")


if __name__ == "__main__":
    main()