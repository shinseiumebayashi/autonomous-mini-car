"""
Motor control via L298N H-bridge.
Two DC motors (rear-wheel drive) with PWM speed control.
"""

import RPi.GPIO as GPIO
from . import config


class MotorController:
    """L298Nを介した2モーター駆動制御"""

    def __init__(self):
        # GPIOモード設定（既にBCMなら何もしない）
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BCM)

        # 全モーター制御ピンを出力に設定
        for pin in [config.LEFT_MOTOR_ENA, config.LEFT_MOTOR_IN1,
                    config.LEFT_MOTOR_IN2, config.RIGHT_MOTOR_ENB,
                    config.RIGHT_MOTOR_IN3, config.RIGHT_MOTOR_IN4]:
            GPIO.setup(pin, GPIO.OUT)

        # PWM初期化
        self._pwm_left = GPIO.PWM(config.LEFT_MOTOR_ENA, config.MOTOR_PWM_FREQ)
        self._pwm_right = GPIO.PWM(config.RIGHT_MOTOR_ENB, config.MOTOR_PWM_FREQ)
        self._pwm_left.start(0)
        self._pwm_right.start(0)

    def forward(self, speed=config.DEFAULT_SPEED):
        """前進"""
        GPIO.output(config.LEFT_MOTOR_IN1, GPIO.LOW)
        GPIO.output(config.LEFT_MOTOR_IN2, GPIO.HIGH)
        GPIO.output(config.RIGHT_MOTOR_IN3, GPIO.LOW)
        GPIO.output(config.RIGHT_MOTOR_IN4, GPIO.HIGH)
        self._set_speed(speed)

    def backward(self, speed=config.DEFAULT_SPEED):
        """後進"""
        GPIO.output(config.LEFT_MOTOR_IN1, GPIO.HIGH)
        GPIO.output(config.LEFT_MOTOR_IN2, GPIO.LOW)
        GPIO.output(config.RIGHT_MOTOR_IN3, GPIO.HIGH)
        GPIO.output(config.RIGHT_MOTOR_IN4, GPIO.LOW)
        self._set_speed(speed)

    def stop(self):
        """停止"""
        GPIO.output(config.LEFT_MOTOR_IN1, GPIO.LOW)
        GPIO.output(config.LEFT_MOTOR_IN2, GPIO.LOW)
        GPIO.output(config.RIGHT_MOTOR_IN3, GPIO.LOW)
        GPIO.output(config.RIGHT_MOTOR_IN4, GPIO.LOW)
        self._set_speed(0)

    def _set_speed(self, speed):
        """内部メソッド: PWMデューティ比設定"""
        speed = max(config.MIN_SPEED, min(config.MAX_SPEED, speed))
        self._pwm_left.ChangeDutyCycle(speed)
        self._pwm_right.ChangeDutyCycle(speed)

    def cleanup(self):
        """終了処理"""
        self.stop()
        self._pwm_left.stop()
        self._pwm_right.stop()