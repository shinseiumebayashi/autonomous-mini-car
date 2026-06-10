"""
Line detection using OpenCV.
Detects a dark line on a light background and returns its position offset.
"""

import cv2
import numpy as np


class LineDetector:
    """黒い線の検出と中心からの偏差計算"""

    def __init__(self, threshold=60, roi_ratio=0.33):
        """
        threshold: 二値化のしきい値（暗い部分=線）
        roi_ratio: 画像下から何割を見るか（0.5 = 下半分）
        """
        self.threshold = threshold
        self.roi_ratio = roi_ratio

    def detect(self, image_rgb):
        """
        画像から線を検出して、中心からのオフセットを返す。
        
        Args:
            image_rgb: picamera2から取得したRGB画像 (numpy array)
        
        Returns:
            offset: 線の位置（画像中央=0、右が+、左が-）。線が見つからなければNone
        """
        # RGB → グレースケール
        gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        height, width = gray.shape

        # ROI: 画像の下部
        roi_start = int(height * (1 - self.roi_ratio))
        roi = gray[roi_start:, :]

        # 二値化
        _, binary = cv2.threshold(roi, self.threshold, 255, cv2.THRESH_BINARY_INV)

        # ノイズ除去
        kernel = np.ones((5, 5), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

        # 輪郭検出
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None

        # 最大の輪郭の重心
        largest = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest)
        if M["m00"] == 0:
            return None

        cx = int(M["m10"] / M["m00"])

        # 中心からのオフセット
        offset = cx - width // 2
        return offset