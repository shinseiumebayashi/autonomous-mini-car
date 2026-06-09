"""
High-level robot control combining motors, servo, and ultrasonic sensor.
"""

import time
from .motor import MotorController
from .servo import ServoController
from .ultrasonic import UltrasonicSensor


class Robot:
    """車両全体を制御する高レベルクラス"""

    def __init__(self):
        self.motor = MotorController()
        self.servo = ServoController()
        self.sensor = UltrasonicSensor()
        self.servo.center()

    def forward(self, speed=60):
        """直進"""
        self.servo.center()
        self.motor.forward(speed)

    def backward(self, speed=60):
        """後退"""
        self.servo.center()
        self.motor.backward(speed)

    def stop(self):
        """停止"""
        self.motor.stop()

    def turn_left(self, speed=60):
        """左に曲がりながら前進"""
        self.servo.left()
        self.motor.forward(speed)

    def turn_right(self, speed=60):
        """右に曲がりながら前進"""
        self.servo.right()
        self.motor.forward(speed)

    def reverse_left(self, speed=60):
        """左にハンドル切って後退"""
        self.servo.right()  # 後退時はハンドルを逆に切ると前が左に向く
        self.motor.backward(speed)

    def reverse_right(self, speed=60):
        """右にハンドル切って後退"""
        self.servo.left()
        self.motor.backward(speed)

    def get_distance(self):
        """前方の距離をcmで返す。タイムアウトは999"""
        d = self.sensor.measure()
        return 999 if d < 0 else d

    def cleanup(self):
        """終了処理"""
        self.motor.cleanup()
        self.servo.cleanup()