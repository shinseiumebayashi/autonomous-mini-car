"""
HC-SR04 Ultrasonic Sensor Test
距離を測定して0.5秒ごとに表示する
"""

import RPi.GPIO as GPIO
import time

# GPIOピン番号の設定（BCM番号で指定）
TRIG_PIN = 23
ECHO_PIN = 24

def setup():
    """GPIO初期化"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.5)

def measure_distance():
    """距離を測定して cm で返す"""
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    
    pulse_start = time.time()
    timeout = pulse_start + 0.04
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
        if pulse_start > timeout:
            return -1
    
    pulse_end = time.time()
    timeout = pulse_end + 0.04
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()
        if pulse_end > timeout:
            return -1
    
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 34300 / 2
    return round(distance, 2)

def main():
    setup()
    print("超音波センサーテスト開始（Ctrl+C で終了）")
    try:
        while True:
            distance = measure_distance()
            if distance < 0:
                print("タイムアウト（測定失敗）")
            elif distance > 400:
                print(f"範囲外: {distance} cm")
            else:
                print(f"距離: {distance} cm")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n終了")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()