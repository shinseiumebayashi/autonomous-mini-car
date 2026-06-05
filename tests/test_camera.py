"""
Camera test using the new Camera class.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.camera import Camera


def main():
    cam = Camera()
    print("Camera test using Camera class")

    try:
        print("Capturing image...")
        cam.capture("test_camera_class.jpg")
        print("Saved: test_camera_class.jpg")

        print("Capturing as array...")
        arr = cam.capture_array()
        print(f"Array shape: {arr.shape}, dtype: {arr.dtype}")

    finally:
        cam.cleanup()
        print("Done")


if __name__ == "__main__":
    main()
