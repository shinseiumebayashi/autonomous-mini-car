"""
Hardware configuration
ハードウェア設定

All GPIO pin assignments and constants are managed here.
全てのGPIOピン番号と定数をここで一元管理する。
"""

# ===== Motors (Rear-wheel drive via L298N) =====
# モーター（L298N経由の後輪駆動）
LEFT_MOTOR_ENA = 25
LEFT_MOTOR_IN1 = 17
LEFT_MOTOR_IN2 = 27

RIGHT_MOTOR_ENB = 6
RIGHT_MOTOR_IN3 = 22
RIGHT_MOTOR_IN4 = 5

MOTOR_PWM_FREQ = 1000

# ===== Servo (Front-wheel steering) =====
# サーボ（前輪操舵）
SERVO_PIN = 21
SERVO_PWM_FREQ = 50

# Servo positions (PWM duty cycle %)
# Calibrated to avoid wheel-chassis interference
# サーボ位置（PWMデューティ比%）
# タイヤと車体の干渉を避けるよう調整済み
SERVO_CENTER = 7.5
SERVO_LEFT_MAX = 8.7
SERVO_RIGHT_MAX = 6.3

# ===== Ultrasonic Sensor (HC-SR04) =====
# 超音波センサー（HC-SR04）
ULTRASONIC_TRIG = 23
ULTRASONIC_ECHO = 24

# ===== Default speeds =====
# デフォルト速度設定
DEFAULT_SPEED = 60
MIN_SPEED = 0
MAX_SPEED = 100