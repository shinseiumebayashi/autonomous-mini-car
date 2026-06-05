"""
Keyboard-controlled driving application.

Controls:
    W: forward
    S: backward
    A: steer left
    D: steer right
    X: stop motors
    Z: center steering
    Q: quit
"""

import sys
import os
import tty
import termios

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.motor import MotorController
from src.servo import ServoController


def getch():
    """1文字をEnterなしで読む"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def print_help():
    print("=" * 40)
    print("Keyboard Drive Control")
    print("  W: forward    S: backward")
    print("  A: left       D: right")
    print("  X: stop       Z: center")
    print("  Q: quit")
    print("=" * 40)


def main():
    motor = MotorController()
    servo = ServoController()

    print_help()

    try:
        while True:
            key = getch().lower()

            if key == 'w':
                print("Forward")
                motor.forward()
            elif key == 's':
                print("Backward")
                motor.backward()
            elif key == 'a':
                print("Left")
                servo.left()
            elif key == 'd':
                print("Right")
                servo.right()
            elif key == 'x':
                print("Stop")
                motor.stop()
            elif key == 'z':
                print("Center steering")
                servo.center()
            elif key == 'q':
                print("Quitting...")
                break

    except KeyboardInterrupt:
        print("\nInterrupted")
    finally:
        motor.cleanup()
        servo.cleanup()
        print("Cleanup complete")


if __name__ == "__main__":
    main()
