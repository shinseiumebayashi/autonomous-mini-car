"""
キーボード操作で走行（SSH対応版）
W/S: 前進・後進
A/D: 左/右に操舵
Space: 停止 (ハンドル中央)
Q: 終了

操作方法: キーを押して Enter
（毎回 Enter が必要ですが、SSHでも動きます）
"""

import RPi.GPIO as GPIO
import time
import atexit
import sys
import tty
import termios

# ===== ピン設定 =====
SERVO_PIN = 21
ENA = 25
IN1 = 17
IN2 = 27
ENB = 6
IN3 = 22
IN4 = 5

# ===== 初期化 =====
GPIO.setmode(GPIO.BCM)
for pin in [ENA, IN1, IN2, ENB, IN3, IN4]:
    GPIO.setup(pin, GPIO.OUT)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm_left = GPIO.PWM(ENA, 1000)
pwm_right = GPIO.PWM(ENB, 1000)
pwm_servo = GPIO.PWM(SERVO_PIN, 50)

pwm_left.start(0)
pwm_right.start(0)
pwm_servo.start(7.5)

def cleanup():
    pwm_left.stop()
    pwm_right.stop()
    pwm_servo.stop()
    GPIO.cleanup()

atexit.register(cleanup)

# ===== 制御関数 =====
SPEED = 60

def forward():
    print("→ 前進")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_left.ChangeDutyCycle(SPEED)
    pwm_right.ChangeDutyCycle(SPEED)

def backward():
    print("→ 後進")
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_left.ChangeDutyCycle(SPEED)
    pwm_right.ChangeDutyCycle(SPEED)
    
def stop():
    print("→ 停止")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_left.ChangeDutyCycle(0)
    pwm_right.ChangeDutyCycle(0)

def steer_left():
    print("→ 左操舵")
    pwm_servo.ChangeDutyCycle(9.5)

def steer_right():
    print("→ 右操舵")
    pwm_servo.ChangeDutyCycle(5.5)

def steer_center():
    print("→ ハンドル中央")
    pwm_servo.ChangeDutyCycle(7.0)

# ===== 1キーずつ読むためのヘルパー関数 =====
def getch():
    """1文字をEnter押さずに読む"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# ===== メインループ =====
print("=" * 40)
print("キーボード操作スタート")
print("W: 前進  S: 後進")
print("A: 左操舵 D: 右操舵")
print("X: 停止   Z: ハンドル中央")
print("Q: 終了")
print("=" * 40)
print("（キーを1つ押すと即反応します）")

try:
    while True:
        key = getch().lower()
        if key == 'w':
            forward()
        elif key == 's':
            backward()
        elif key == 'a':
            steer_left()
        elif key == 'd':
            steer_right()
        elif key == 'x':
            stop()
        elif key == 'z':
            steer_center()
        elif key == 'q':
            print("終了")
            stop()
            steer_center()
            time.sleep(0.5)
            break
except KeyboardInterrupt:
    print("\n中断")
finally:
    stop()
    print("GPIO クリーンアップ完了")