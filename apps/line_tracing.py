"""
Line tracing using P (proportional) control.

The robot follows a black line on the ground using camera-based detection.
Steering is controlled proportional to how far the line is from the image center.

Press Ctrl+C to stop.
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.robot import Robot
from src.camera import Camera
from src.line_detector import LineDetector


# ===== Tunable parameters =====
SPEED = 45 # 走行速度 (0-100)
KP = 0.0015     # 比例ゲイン (調整必須)
CAMERA_RESOLUTION = (640, 480)
DETECT_THRESHOLD = 120
LOST_LINE_TIMEOUT = 0.5  # 線を見失ってから停止までの秒数


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
            # 画像取得
            image = camera.capture_array()

            # 線検出
            offset = detector.detect(image)

            if offset is None:
                # 線が見つからないので即停止
                print("Line lost - stopping")
                robot.stop()
                continue

            last_line_time = time.time()

            # P制御で操舵量を計算
            # offset を -1.0 ~ 1.0 に正規化してサーボに渡す
            steering = offset * KP
            steering = max(-0.6, min(0.6, steering))

            # 操舵 + 前進
            robot.servo.set_angle(-steering)  # 符号反転: offset右(+)なら右に切る = サーボは負
            robot.motor.forward(SPEED)

            print(f"Offset={offset:+4d}  Steering={steering:+.2f}")

            time.sleep(0.03)  # 30Hz程度

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        robot.stop()
        robot.cleanup()
        camera.cleanup()
        print("Cleanup complete")


if __name__ == "__main__":
    main()