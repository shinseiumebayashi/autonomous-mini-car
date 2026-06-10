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

def scan_surroundings(robot):
    """
    後退しながら左右の距離を測定して返す。
    Returns: (left_distance, right_distance)
    """
    # ハンドルを左に切って後退 → 車体が右に向くので「左方向」を見る
    robot.servo.left()
    robot.motor.backward(REVERSE_SPEED)
    time.sleep(0.4)
    right_distance = robot.get_distance()  # この時、車体は左に向いてる → 前方は右方向

    # ハンドルを右に切って後退 → 車体が左に向くので「右方向」を見る
    robot.servo.right()
    time.sleep(0.4)
    left_distance = robot.get_distance()  # 車体は右に向いてる → 前方は左方向

    robot.motor.stop()
    return left_distance, right_distance

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
                # 危険距離: 周囲を観察して回避
                print(f"  → Obstacle at {distance:.1f}cm, scanning surroundings...")
                robot.stop()
                time.sleep(0.3)

                # 左右を観察（後退しながら）
                left_distance, right_distance = scan_surroundings(robot)
                print(f"  → Left: {left_distance:.1f}cm, Right: {right_distance:.1f}cm")

                # 中央に戻して一旦停止
                robot.servo.center()
                robot.stop()
                time.sleep(0.3)

                # 遠い方に旋回
                if left_distance > right_distance:
                    print("  → Left is clearer, turning left")
                    robot.turn_left(TURN_SPEED)
                else:
                    print("  → Right is clearer, turning right")
                    robot.turn_right(TURN_SPEED)

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