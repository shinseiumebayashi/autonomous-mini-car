"""
Line tracing using P (proportional) control.
P（比例）制御によるライントレース

The robot follows a black line on the ground using camera-based detection.
Steering is controlled proportional to how far the line is from the image center.
カメラで黒い線を検出し、画像中心からのズレに比例して操舵量を決定する。

Press Ctrl+C to stop.
停止するには Ctrl+C を押す。
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.robot import Robot
from src.camera import Camera
from src.line_detector import LineDetector


# ===== Tunable parameters =====
# 調整可能なパラメータ
SPEED = 45                  # Driving speed (0-100) / 走行速度
KP = 0.0015                 # Proportional gain (requires tuning) / 比例ゲイン（調整必須）
CAMERA_RESOLUTION = (640, 480)
DETECT_THRESHOLD = 120      # Brightness threshold for line detection / 線検出のしきい値
LOST_LINE_TIMEOUT = 0.5     # Seconds before stopping after line loss / 線を見失ってから停止までの秒数


def main():
    robot = Robot()
    camera = Camera(resolution=CAMERA_RESOLUTION)
    detector = LineDetector(threshold=DETECT_THRESHOLD)

    camera.start()

    print("=" * 40)
    print("Line Tracing (P Control)")
    print(f"Speed={SPEED}, Kp={KP}")
    print("Press Ctrl+C to stop")
    print("=" * 40)
    time.sleep(1)

    last_line_time = time.time()

    try:
        while True:
            # Capture image
            # 画像取得
            image = camera.capture_array()

            # Detect line
            # 線検出
            offset = detector.detect(image)

            if offset is None:
                # No line found, stop immediately
                # 線が見つからないので即停止
                print("Line lost - stopping")
                robot.stop()
                continue

            last_line_time = time.time()

            # Calculate steering with P control
            # offset is normalized to a range usable by the servo
            # P制御で操舵量を計算
            # offset を正規化してサーボに渡す
            steering = offset * KP
            steering = max(-0.6, min(0.6, steering))

            # Steer + drive forward
            # Sign inversion: offset positive (right) means steer right = negative servo
            # 操舵 + 前進
            # 符号反転: offset右(+) なら右に切る = サーボは負
            robot.servo.set_angle(-steering)
            robot.motor.forward(SPEED)

            print(f"Offset={offset:+4d}  Steering={steering:+.2f}")

            time.sleep(0.03)  # About 30Hz control loop / 約30Hzの制御ループ

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        robot.stop()
        robot.cleanup()
        camera.cleanup()
        print("Cleanup complete")


if __name__ == "__main__":
    main()