#  Product     : Cokoino Real-Wheel Drive Steering Car Chassis kit
#  Auther      : www.cokoino.com
#  Modification: 2025/05/13
import RPi.GPIO as GPIO  # Import RPi.GPIO library
import time  # Import time library for delay

# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define servo control pins
servo_pin = 21  # The servo is connected to the GPO21 pin

# Set pins to output mode
GPIO.setup(servo_pin, GPIO.OUT)

# Create PWM object with frequency set to 50Hz
pwm = GPIO.PWM(servo_pin, 50)

# Start PWM with an initial duty cycle of 0%
pwm.start(0)

def set_angle(angle):
    # Calculate duty cycle (0.5ms to 2.5ms=>0% -180%)
    duty_cycle = angle / 18 + 2  # transcoding
    pwm.ChangeDutyCycle(duty_cycle)  # Modify the duty cycle of the servo motor
    time.sleep(1)  # Wait for 1 second to complete the servo rotation

try:
    set_angle(90)  # Set the servo to 90 degrees
    time.sleep(2)  # Wait for 2 seconds

except KeyboardInterrupt:
    # Stop PWM
    pwm.stop()
    GPIO.cleanup()  # Clean GPIO settings