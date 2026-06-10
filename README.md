# Autonomous Mini Car 🚗

A personal project to build a small autonomous vehicle from scratch using Raspberry Pi 4, OpenCV, and various sensors. Built to demonstrate embedded systems, computer vision, and software architecture skills.

> 🇯🇵 [日本語版 README はこちら](README.ja.md)

## Demo

> 📹 Demo video coming soon

## Overview

This project covers the full stack of building an autonomous mini car: from hardware assembly to computer vision and PID control. The car uses **rear-wheel drive with front-wheel steering** (Ackermann-style) — closer to a real car than typical differential-drive robots.

### Features

- 🎮 Keyboard-controlled driving (WASD)
- 📏 Ultrasonic distance sensing (HC-SR04)
- 📷 Real-time image capture (Pi Camera V2)
- ⚙️ PWM-based motor and servo control
- 🧱 Modular architecture with clean class abstractions

## Tech Stack

| Category | Stack |
|----------|-------|
| Hardware | Raspberry Pi 4 (2GB), L298N motor driver, MG90S servo, HC-SR04 ultrasonic, Pi Camera V2 |
| Software | Python 3.13, OpenCV 4.13, NumPy, RPi.GPIO, picamera2 |
| Control | PWM motor control, Ackermann steering |
| Tools | VSCode + Remote-SSH, Git/GitHub |

## Roadmap

- [x] **Phase 1**: Environment setup
- [x] **Phase 2**: Individual component testing
- [x] **Phase 3**: Chassis assembly and keyboard-controlled driving
- [x] **Phase 4**: Obstacle avoidance with ultrasonic sensors
- [ ] **Phase 5**: Line tracing with OpenCV + PID control
- [ ] **Phase 6**: Integration and demo videos

## Project Structure

​```
autonomous-mini-car/
├── src/                    # Hardware abstraction modules
│   ├── config.py          # GPIO pin assignments
│   ├── motor.py           # MotorController class
│   ├── servo.py           # ServoController class
│   ├── ultrasonic.py      # UltrasonicSensor class
│   └── camera.py          # Camera class
├── apps/                   # Runnable applications
│   └── keyboard_drive.py  # Manual driving
├── tests/                  # Component tests
└── docs/                   # Documentation
​```

## Hardware Wiring

| Component | GPIO (BCM) | Notes |
|-----------|------------|-------|
| L298N ENA | 25 | Left motor PWM |
| L298N IN1/IN2 | 17/27 | Left motor direction |
| L298N ENB | 6 | Right motor PWM |
| L298N IN3/IN4 | 22/5 | Right motor direction |
| MG90S Servo | 21 | Front-wheel steering |
| HC-SR04 Trig | 23 | Ultrasonic trigger |
| HC-SR04 Echo | 24 | Via voltage divider (1kΩ + 2kΩ) |

Motors powered by 2x 18650 batteries (7.4V) via L298N. Pi powered separately via USB-C.

## Setup

​```bash
git clone https://github.com/shinseiumebayashi/autonomous-mini-car.git
cd autonomous-mini-car

python3 -m venv --system-site-packages venv
source venv/bin/activate

pip install -r requirements.txt
​```

## Usage

​```bash
# Test individual components
python3 tests/test_motor.py
python3 tests/test_servo.py
python3 tests/test_ultrasonic.py
python3 tests/test_camera.py

# Drive with keyboard
python3 apps/keyboard_drive.py
​```

### Keyboard Controls

| Key | Action |
|-----|--------|
| W | Forward |
| S | Backward |
| A | Steer left |
| D | Steer right |
| X | Stop motors |
| Z | Center steering |
| Q |
## What I Learned

- GPIO control at microsecond precision for ultrasonic timing
- PWM signal generation for motor and servo control
- Power system isolation between logic (5V) and motor (7.4V) circuits
- Class-based abstraction for hardware control
- Ackermann steering vs differential drive trade-offs

## License

MIT — see LICENSE.