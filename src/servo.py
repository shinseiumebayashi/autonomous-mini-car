"""
Servo motor control for front-wheel steering (MG90S).
"""

import RPi.GPIO as GPIO
from . import config


class ServoController:
    """前輪操舵用サーボの制御"""

    def __init__(self):
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BCM)

        GPIO.setup(config.SERVO_PIN, GPIO.OUT)
        self._pwm = GPIO.PWM(config.SERVO_PIN, config.SERVO_PWM_FREQ)
        self._pwm.start(config.SERVO_CENTER)

    def center(self):
        """直進向きに戻す"""
        self._pwm.ChangeDutyCycle(config.SERVO_CENTER)

    def left(self):
        """左に最大操舵"""
        self._pwm.ChangeDutyCycle(config.SERVO_LEFT_MAX)

    def right(self):
        """右に最大操舵"""
        self._pwm.ChangeDutyCycle(config.SERVO_RIGHT_MAX)

    def set_angle(self, angle):
        """
        角度を直接指定 (-1.0 から 1.0 で正規化)
        -1.0 = 最大右、0 = 中央、1.0 = 最大左
        """
        angle = max(-1.0, min(1.0, angle))
        # 線形補間
        if angle >= 0:
            duty = config.SERVO_CENTER + angle * (config.SERVO_LEFT_MAX - config.SERVO_CENTER)
        else:
            duty = config.SERVO_CENTER + angle * (config.SERVO_CENTER - config.SERVO_RIGHT_MAX)
        self._pwm.ChangeDutyCycle(duty)

    def cleanup(self):
        self.center()
        self._pwm.stop()