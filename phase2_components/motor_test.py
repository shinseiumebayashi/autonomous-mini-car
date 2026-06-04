"""
L298N Motor Driver + DC Motor Test
モーターを正転 → 停止 → 逆転 → 停止 のサイクルで動かす
"""

import RPi.GPIO as GPIO
import time

# モーターA（左モーター想定）のピン
ENA = 25  # PWM速度制御
IN1 = 17  # 方向制御1
IN2 = 27  # 方向制御2

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    # PWMを1000Hzで初期化、初期デューティ比0%
    pwm = GPIO.PWM(ENA, 1000)
    pwm.start(0)
    return pwm

def forward(pwm, speed):
    """正転"""
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(speed)

def backward(pwm, speed):
    """逆転"""
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwm.ChangeDutyCycle(speed)

def stop(pwm):
    """停止"""
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)

def main():
    pwm = setup()
    print("モーターテスト開始")
    
    try:
        print("正転 50%スピードで3秒")
        forward(pwm, 50)
        time.sleep(3)
        
        print("停止 1秒")
        stop(pwm)
        time.sleep(1)
        
        print("逆転 50%スピードで3秒")
        backward(pwm, 50)
        time.sleep(3)
        
        print("停止 1秒")
        stop(pwm)
        time.sleep(1)
        
        print("正転 100%スピードで2秒")
        forward(pwm, 100)
        time.sleep(2)
        
        print("停止")
        stop(pwm)
        time.sleep(1)
        
    except KeyboardInterrupt:
        print("\n中断")
    finally:
        stop(pwm)
        pwm.stop()
        GPIO.cleanup()
        print("終了")

if __name__ == "__main__":
    main()