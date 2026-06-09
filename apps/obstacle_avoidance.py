"""
Autonomous obstacle avoidance.

The robot drives forward, monitors front distance with ultrasonic sensor,
and turns away when obstacles are detected.

Press Ctrl+C to stop.
"""

import sys
import os
import time
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.robot import Robot


# ===== Tunable parameters =====
SAFE_DISTANCE = 30      # cm。これより近づいたら避ける
CAUTION_DISTANCE = 50   # cm。これより近いと減速
NORMAL_SPEED = 65
SLOW_SPEED = 50
REVERSE_TIME = 0.8      # 後退する秒数
TURN_TIME = 0.9         # 旋回する秒数
REVERSE_SPEED = 70
TURN_SPEED = 70
def main():
    robot = Robot()
    print("=" * 40)
    print("Autonomous Obstacle Avoidance")
    print("Press Ctrl+C to stop")
    print("=" * 40)

    time.sleep(1)

    try:
        while True:
            distance = robot.get_distance()
            print(f"Distance: {distance:.1f} cm")

            if distance > CAUTION_DISTANCE:
                robot.forward(NORMAL_SPEED)
                time.sleep(0.1)

            elif distance > SAFE_DISTANCE:
                robot.forward(SLOW_SPEED)
                time.sleep(0.1)

            else:
                print(f"  → Obstacle at {distance:.1f}cm, avoiding...")
                robot.stop()
                time.sleep(0.3)

                # 後退（起動電力が必要なので REVERSE_SPEED）
                print("  → Backing up")
                robot.backward(REVERSE_SPEED)
                time.sleep(REVERSE_TIME)

                robot.stop()
                time.sleep(0.2)

                # 旋回（ハンドル切るので抵抗大、TURN_SPEED）
                if random.random() > 0.5:
                    print("  → Turning right")
                    robot.turn_right(TURN_SPEED)
                else:
                    print("  → Turning left")
                    robot.turn_left(TURN_SPEED)

                time.sleep(TURN_TIME)
                robot.stop()
                time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        robot.stop()
        robot.cleanup()
        print("Cleanup complete")


if __name__ == "__main__":
    main()