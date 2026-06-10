"""
Line detection test using OpenCV.
Captures an image and visualizes the line detection process.
"""

import sys
import os
import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.camera import Camera


def detect_line(image):
    """
    画像から黒い線の中心位置を検出する。
    Returns: (cx, cy) or None if no line found
    """
    # グレースケール変換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 画像の下半分だけ使う（足元の線に集中）
    height, width = gray.shape
    roi = gray[height // 2 :, :]

    # 二値化: 暗い部分を白に
    _, binary = cv2.threshold(roi, 120, 255, cv2.THRESH_BINARY_INV)

    # ノイズ除去
    kernel = np.ones((5, 5), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    # 輪郭検出
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None, binary

    # 最大の輪郭を選ぶ
    largest = max(contours, key=cv2.contourArea)

    # 重心計算
    M = cv2.moments(largest)
    if M["m00"] == 0:
        return None, binary

    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"]) + height // 2  # ROI下半分なのでオフセット

    return (cx, cy), binary


def main():
    cam = Camera(resolution=(640, 480))

    try:
        print("Capturing image...")
        image = cam.capture_array()
        print(f"Image shape: {image.shape}")

        # OpenCVはBGR、picamera2はRGBで返すので変換
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 線検出
        center, binary = detect_line(image_bgr)

        # 可視化
        output = image_bgr.copy()
        h, w = output.shape[:2]
        # 画像中央に縦線
        cv2.line(output, (w // 2, 0), (w // 2, h), (0, 255, 0), 2)
        # ROI境界（下半分）に横線
        cv2.line(output, (0, h // 2), (w, h // 2), (255, 0, 0), 2)

        if center is None:
            print("❌ No line detected")
            cv2.putText(output, "NO LINE", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            cx, cy = center
            offset = cx - w // 2
            print(f"✅ Line found at ({cx}, {cy})")
            print(f"   Offset from center: {offset}px ({'right' if offset > 0 else 'left'})")
            # 検出した線の中心を赤い丸で示す
            cv2.circle(output, (cx, cy), 10, (0, 0, 255), -1)
            cv2.putText(output, f"offset={offset}", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # 保存
        cv2.imwrite("line_detection.jpg", output)
        cv2.imwrite("line_binary.jpg", binary)
        print("Saved: line_detection.jpg, line_binary.jpg")

    finally:
        cam.cleanup()


if __name__ == "__main__":
    main()