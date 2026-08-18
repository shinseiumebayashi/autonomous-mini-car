# Autonomous Mini Car 🚗

A personal project to build a small autonomous vehicle from scratch using Raspberry Pi 4, OpenCV, and various sensors. Built to demonstrate embedded systems, computer vision, and software architecture skills.

> 🇯🇵 [日本語版 README はこちら](README.ja.md)

## Demo

## Demo

### Full Demo (Overview)
[![Watch the full demo](docs/images/thumbnail_overview.jpg)](https://youtu.be/bMbf2mNTPEo)

### Obstacle Avoidance
[![Obstacle avoidance demo](docs/images/thumbnail_obstacle.jpg)](https://youtu.be/IshrE6iSXc4)

### Line Tracing
[![Line tracing demo](docs/images/thumbnail_linetrace.jpg)](https://youtu.be/zX4fuUpp8hw)

> I've uploaded the video to YouTube as unlisted videos.


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
- [x] **Phase 5**: Line tracing with OpenCV + PID control
- [x] **Phase 6**: Integration and demo videos

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

![Robot Overview](docs/images/robot_main.jpg)
![Robot Side View](docs/images/robot_side.jpg)

## Project Highlights

### Real-Machine Parameter Tuning
Discovered through testing that the chassis exhibited wheel-body interference when the servo was set to its maximum range (±2.0%). Through iterative observation and measurement, identified ±1.2% (8.7 and 6.3 duty cycle) as the optimal range that maintains turning capability without mechanical conflict. This experience reinforced the importance of empirical validation beyond datasheet specifications.

### Threshold Calibration for Different Environments  
The initial line detection threshold (60) failed on a pink-tinted hardwood floor. Built a diagnostic script (`tests/test_threshold.py`) that analyzes brightness distribution across the captured ROI and tested multiple threshold values systematically. Identified 120 as the optimal threshold for the current environment, demonstrating data-driven parameter optimization.

### Sensor-Driven Decision Making
Initial obstacle avoidance used random turn direction selection, which could deadlock in corner scenarios. Improved the algorithm to scan left and right distances during the reverse phase, then turn toward the more open direction. This bidirectional scanning approach mimics how autonomous vehicles use sensor data for path planning.

## What I Learned

### Hardware Engineering
- **GPIO timing control** at microsecond precision for ultrasonic distance measurement
- **PWM signal generation** for both DC motor speed control (1kHz) and servo angle (50Hz)
- **Power system isolation** between logic (5V via USB-C) and motor (7.4V via batteries) circuits
- **H-bridge motor driver** (L298N) and direction control logic
- **Voltage divider** circuits for safe 5V→3.3V signal level conversion

### Software Architecture
- **Class-based hardware abstraction** to separate application logic from GPIO details
- **Centralized configuration** in `src/config.py` for maintainability
- **Reusable components** across multiple applications (keyboard drive, obstacle avoidance, line tracing)

### Computer Vision
- **OpenCV image processing pipeline**: grayscale → thresholding → noise removal → contour detection
- **Region of Interest (ROI)** optimization for real-time line detection
- **Threshold tuning** through empirical brightness analysis (`tests/test_threshold.py`)

### Control Theory
- **Proportional (P) control** for line following
- **Real-machine PID tuning**: Started at KP=0.002, observed overshooting in curves, settled at KP=0.0015 after iterative testing
- **Ackermann steering geometry**: Front-wheel steering vs differential drive trade-offs
- **Physical constraint awareness**: Adjusted servo max angle from ±2.0% to ±1.2% (8.7 and 6.3 duty cycle %) to avoid wheel-chassis interference

### Embedded Systems Practice
- **Headless development** via SSH and VSCode Remote-SSH
- **Reproducible environment** with Python virtual environment and `requirements.txt`
- **Iterative debugging** with empirical threshold detection scripts

## Documentation

- [📖 Project Story](docs/STORY.md) - Full narrative of the project
- [🔧 Engineering Challenges](docs/CHALLENGES.md) - Specific problems and solutions
- [📚 Key Learnings](docs/LEARNINGS.md) - Summary of skills acquired

## License

MIT — see LICENSE.
