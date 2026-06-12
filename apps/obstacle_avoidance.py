"""
Autonomous obstacle avoidance.
自律障害物回避

The robot drives forward, monitors front distance with ultrasonic sensor,
and turns away when obstacles are detected.
ロボットは前進しながら超音波センサーで前方距離を監視し、
障害物を検知すると方向転換して回避する。

Press Ctrl+C to stop.
停止するには Ctrl+C を押す。
"""

import sys
import os
import time
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.robot import Robot


# ===== Tunable parameters =====
# 調整可能なパラメータ
SAFE_DISTANCE = 30      # cm. Below this, perform avoidance / これより近づいたら回避
CAUTION_DISTANCE = 50   # cm. Below this, slow down / これより近いと減速
NORMAL_SPEED = 65       # Normal driving speed / 通常走行速度
SLOW_SPEED = 50         # Cautious speed near obstacles / 障害物接近時の減速
REVERSE_TIME = 0.8      # Reverse duration in seconds / 後退する秒数
TURN_TIME = 0.9         # Turning duration in seconds / 旋回する秒数
REVERSE_SPEED = 70      # Speed for reversing (needs higher torque) / 後退速度（起動電力大）
TURN_SPEED = 70         # Speed for turning (load increases when steered) / 旋回速度（ハンドル負荷）


def scan_surroundings(robot):
    """
    Measure left and right distances while reversing.
    後退しながら左右の距離を測定して返す。

    Returns:
        (left_distance, right_distance)
    """
    # Steer left while reversing -> chassis points right -> sensor sees the left side
    # ハンドルを左に切って後退 → 車体が右に向くので「左方向」を見る
    robot.servo.left()
    robot.motor.backward(REVERSE_SPEED)
    time.sleep(0.4)
    right_distance = robot.get_distance()  # Chassis facing left -> front = right direction
                                            # 車体は左に向いてる → 前方は右方向

    # Steer right while reversing -> chassis points left -> sensor sees the right side
    # ハンドルを右に切って後退 → 車体が左に向くので「右方向」を見る
    robot.servo.right()
    time.sleep(0.4)
    left_distance = robot.get_distance()  # Chassis facing right -> front = left direction
                                           # 車体は右に向いてる → 前方は左方向

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
                # Plenty of space, drive at normal speed
                # 余裕あり、通常速度で前進
                robot.forward(NORMAL_SPEED)
                time.sleep(0.1)

            elif distance > SAFE_DISTANCE:
                # Caution zone, slow down
                # 注意距離、減速
                robot.forward(SLOW_SPEED)
                time.sleep(0.1)

            else:
                # Danger zone: scan surroundings and avoid
                # 危険距離: 周囲を観察して回避
                print(f"  → Obstacle at {distance:.1f}cm, scanning surroundings...")
                robot.stop()
                time.sleep(0.3)

                # Scan left and right while reversing
                # 左右を観察（後退しながら）
                left_distance, right_distance = scan_surroundings(robot)
                print(f"  → Left: {left_distance:.1f}cm, Right: {right_distance:.1f}cm")

                # Return steering to center and stop briefly
                # ハンドルを中央に戻して一旦停止
                robot.servo.center()
                robot.stop()
                time.sleep(0.3)

                # Turn toward the more open direction
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