"""
Camera control wrapper for Raspberry Pi Camera Module V2.
Uses picamera2 library.
"""

from picamera2 import Picamera2
import time


class Camera:
    """カメラ制御の薄いラッパー"""

    def __init__(self, resolution=(1280, 720)):
        self._cam = Picamera2()
        config = self._cam.create_still_configuration(main={"size": resolution})
        self._cam.configure(config)
        self._started = False

    def start(self):
        """カメラ起動（撮影前に呼ぶ）"""
        if not self._started:
            self._cam.start()
            time.sleep(2)  # 自動露出・ホワイトバランス安定待ち
            self._started = True

    def capture(self, filename):
        """静止画をファイルに保存"""
        if not self._started:
            self.start()
        self._cam.capture_file(filename)

    def capture_array(self):
        """画像をnumpy配列で返す（OpenCV処理用）"""
        if not self._started:
            self.start()
        return self._cam.capture_array()

    def stop(self):
        """カメラ停止"""
        if self._started:
            self._cam.stop()
            self._started = False

    def cleanup(self):
        self.stop()
