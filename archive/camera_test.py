"""
Camera Module V2 Test
カメラモジュールV2 テスト

Capture a still image using picamera2.
picamera2 を使って静止画を撮影する。
"""

from picamera2 import Picamera2
import time


def main():
    print("Initializing camera... / カメラ初期化中...")
    picam2 = Picamera2()

    config = picam2.create_still_configuration(main={"size": (1280, 720)})
    picam2.configure(config)

    print("Starting camera / カメラ起動")
    picam2.start()
    time.sleep(2)  # Wait for auto-exposure and white balance to stabilize
                   # 自動露出・ホワイトバランスの安定待ち

    print("Capturing... / 撮影中...")
    picam2.capture_file("camera_test.jpg")
    print("Saved: camera_test.jpg / 保存完了: camera_test.jpg")

    picam2.stop()
    print("Done / 終了")


if __name__ == "__main__":
    main()