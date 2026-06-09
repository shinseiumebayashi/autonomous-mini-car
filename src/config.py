"""
Hardware configuration
全てのGPIOピン番号と定数をここで管理
"""

# ===== Motors (Rear-wheel drive via L298N) =====
LEFT_MOTOR_ENA = 25   # PWM
LEFT_MOTOR_IN1 = 17
LEFT_MOTOR_IN2 = 27

RIGHT_MOTOR_ENB = 6   # PWM
RIGHT_MOTOR_IN3 = 22
RIGHT_MOTOR_IN4 = 5

MOTOR_PWM_FREQ = 1000  # Hz

# ===== Servo (Front-wheel steering) =====
SERVO_PIN = 21
SERVO_PWM_FREQ = 50

# Servo positions (duty cycle %)
SERVO_CENTER = 7.5
SERVO_LEFT_MAX = 8.7   # Calibrated for this chassis
SERVO_RIGHT_MAX = 6.3

# ===== Ultrasonic Sensor (HC-SR04) =====
ULTRASONIC_TRIG = 23
ULTRASONIC_ECHO = 24

# ===== Default speeds =====
DEFAULT_SPEED = 60      # 0-100 %
MIN_SPEED = 0
MAX_SPEED = 100