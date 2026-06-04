"""
Camera Module V2 Test
picamera2で静止画を撮影
"""

from picamera2 import Picamera2
import time

def main():
    print("カメラ初期化中...")
    picam2 = Picamera2()
    
    config = picam2.create_still_configuration(main={"size": (1280, 720)})
    picam2.configure(config)
    
    print("カメラ起動")
    picam2.start()
    time.sleep(2)  # ホワイトバランス調整待ち
    
    print("撮影中...")
    picam2.capture_file("camera_test.jpg")
    print("保存完了: camera_test.jpg")
    
    picam2.stop()
    print("終了")

if __name__ == "__main__":
    main()