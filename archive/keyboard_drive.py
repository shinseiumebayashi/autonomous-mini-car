"""
Keyboard-controlled driving (SSH-compatible version)
キーボード操作で走行（SSH対応版）

W/S: forward / backward       前進・後進
A/D: steer left / right       左/右に操舵
X:   stop                     停止
Z:   center steering          ハンドル中央
Q:   quit                     終了

Reads a single key per press, no Enter required.
Works over SSH (no X server needed).
キーを1つ押すと即反応。Enterキー不要。
SSH越しでも動作する（X serverに依存しない）。
"""

import RPi.GPIO as GPIO
import time
import atexit
import sys
import tty
import termios

# ===== Pin configuration =====
# ピン設定
SERVO_PIN = 21
ENA = 25
IN1 = 17
IN2 = 27
ENB = 6
IN3 = 22
IN4 = 5

# ===== Initialization =====
# 初期化
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

# ===== Control functions =====
# 制御関数
SPEED = 60


def forward():
    print("-> Forward / 前進")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_left.ChangeDutyCycle(SPEED)
    pwm_right.ChangeDutyCycle(SPEED)


def backward():
    print("-> Backward / 後進")
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_left.ChangeDutyCycle(SPEED)
    pwm_right.ChangeDutyCycle(SPEED)


def stop():
    print("-> Stop / 停止")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_left.ChangeDutyCycle(0)
    pwm_right.ChangeDutyCycle(0)


def steer_left():
    print("-> Steer left / 左操舵")
    pwm_servo.ChangeDutyCycle(9.5)


def steer_right():
    print("-> Steer right / 右操舵")
    pwm_servo.ChangeDutyCycle(5.5)


def steer_center():
    print("-> Center steering / ハンドル中央")
    pwm_servo.ChangeDutyCycle(7.0)


# ===== Helper for reading single key =====
# 1キーずつ読むためのヘルパー関数
def getch():
    """Read a single character without requiring Enter.
    Enterキーを押さずに1文字を読む。"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


# ===== Main loop =====
# メインループ
print("=" * 40)
print("Keyboard control started / キーボード操作スタート")
print("W: forward    S: backward")
print("A: steer left D: steer right")
print("X: stop       Z: center steering")
print("Q: quit")
print("=" * 40)
print("(Press a single key for instant response)")
print("(キーを1つ押すと即反応します)")

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
            print("Quitting / 終了")
            stop()
            steer_center()
            time.sleep(0.5)
            break
except KeyboardInterrupt:
    print("\nInterrupted / 中断")
finally:
    stop()
    print("GPIO cleanup complete / GPIO クリーンアップ完了")