# Archive

This folder contains the initial experimental scripts from Phase 2, where each hardware component was tested individually.

These scripts have been refactored into class-based implementations under `src/` during Phase 6. They are kept as a record of the early-stage experimentation.

## Contents

- `ultrasonic_test.py` - Initial ultrasonic sensor test
- `echo_check.py` - GPIO pin state diagnostic
- `motor_test.py` - Single DC motor test
- `motors_test.py` - Dual DC motor independent control
- `camera_test.py` - Initial camera test
- `servo_test.py` - Initial servo motor test
- `keyboard_drive.py` - Early keyboard driving (pre-class)

## Current Implementation

Refactored code:
- `../src/` - Hardware abstraction classes
- `../tests/` - Unit tests for each class
- `../apps/` - Runnable applications