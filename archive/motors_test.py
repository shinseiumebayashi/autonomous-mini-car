"""
両モーター動作テスト
左右独立制御 → 差動駆動の確認
"""

import RPi.GPIO as GPIO
import time

# 左モーター
ENA = 25
IN1 = 17
IN2 = 27

# 右モーター
ENB = 6
IN3 = 22
IN4 = 5

def setup():
    GPIO.setmode(GPIO.BCM)
    for pin in [ENA, IN1, IN2, ENB, IN3, IN4]:
        GPIO.setup(pin, GPIO.OUT)
    
    pwm_left = GPIO.PWM(ENA, 1000)
    pwm_right = GPIO.PWM(ENB, 1000)
    pwm_left.start(0)
    pwm_right.start(0)
    return pwm_left, pwm_right

def left_motor(pwm, direction, speed):
    """direction: 'forward', 'backward', 'stop'"""
    if direction == 'forward':
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
    elif direction == 'backward':
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
    else:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(speed)

def right_motor(pwm, direction, speed):
    if direction == 'forward':
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
    elif direction == 'backward':
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
    else:
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)
    pwm.ChangeDutyCycle(speed)

def stop_all(pwm_left, pwm_right):
    left_motor(pwm_left, 'stop', 0)
    right_motor(pwm_right, 'stop', 0)

def main():
    pwm_left, pwm_right = setup()
    print("両モーターテスト開始")
    
    try:
        # 1. 両方正転（直進想定）
        print("両モーター正転 50% → 直進")
        left_motor(pwm_left, 'forward', 50)
        right_motor(pwm_right, 'forward', 50)
        time.sleep(2)
        
        stop_all(pwm_left, pwm_right)
        time.sleep(1)
        
        # 2. 左だけ回転
        print("左モーターのみ正転 → その場で右旋回")
        left_motor(pwm_left, 'forward', 60)
        right_motor(pwm_right, 'stop', 0)
        time.sleep(2)
        
        stop_all(pwm_left, pwm_right)
        time.sleep(1)
        
        # 3. 右だけ回転
        print("右モーターのみ正転 → その場で左旋回")
        left_motor(pwm_left, 'stop', 0)
        right_motor(pwm_right, 'forward', 60)
        time.sleep(2)
        
        stop_all(pwm_left, pwm_right)
        time.sleep(1)
        
        # 4. 左右逆方向（その場旋回）
        print("左正転・右逆転 → その場で右に高速旋回（戦車旋回）")
        left_motor(pwm_left, 'forward', 60)
        right_motor(pwm_right, 'backward', 60)
        time.sleep(2)
        
        stop_all(pwm_left, pwm_right)
        time.sleep(1)
        
        # 5. 両方逆転（後進）
        print("両モーター逆転 50% → 後進")
        left_motor(pwm_left, 'backward', 50)
        right_motor(pwm_right, 'backward', 50)
        time.sleep(2)
        
        stop_all(pwm_left, pwm_right)
        
    except KeyboardInterrupt:
        print("\n中断")
    finally:
        stop_all(pwm_left, pwm_right)
        pwm_left.stop()
        pwm_right.stop()
        GPIO.cleanup()
        print("終了")

if __name__ == "__main__":
    main()