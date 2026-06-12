# Engineering Challenges

This document records specific problems I encountered and how I solved them. Each one is an opportunity to discuss problem-solving methodology in interviews.

## Challenge 1: Power Supply Failure at Initial Boot

**Problem**: The official Raspberry Pi power adapter included with the kit didn't power the Pi. The red LED would not light up.

**Diagnosis**:
1. Tested with a different USB-C charger (MacBook adapter) — Pi booted successfully
2. Tested the original adapter on another USB-C device — no power output
3. Concluded the adapter was defective from the factory

**Solution**: Used an alternative USB-C charger for development. Contacted the seller for replacement.

**Lesson**: Always validate hardware components before assuming software issues.

---

## Challenge 2: Ultrasonic Sensor Echo Pin Always HIGH

**Problem**: The HC-SR04 sensor reported "timeout" on every measurement. Echo pin readings were stuck at HIGH (3.3V).

**Diagnosis**:
1. Wrote a minimal diagnostic script (`echo_check.py`) to monitor the Echo pin state
2. Confirmed Echo was permanently HIGH — not toggling
3. Inspected the breadboard wiring and found the voltage divider circuit was bypassed (the 1kΩ resistor was in the wrong column)

**Solution**: Rewired the voltage divider correctly: Echo → 1kΩ → midpoint → 2kΩ → GND, with the midpoint connecting to GPIO.

**Lesson**: When sensor data looks wrong, verify the physical signal at the pin level before debugging software.

---

## Challenge 3: Wheel-Chassis Mechanical Interference

**Problem**: During obstacle avoidance testing, the robot would freeze during turns. The motors were running but the wheels wouldn't rotate.

**Diagnosis**:
1. Observed that the inner wheel was physically touching the chassis frame at maximum steering angle
2. Identified this as a hardware constraint, not a software bug

**Solution**: Reduced servo PWM duty cycle range from ±2.0% to ±1.2% (8.7% / 6.3% from center 7.5%). Verified by manually rotating the servo through its full new range and confirming no contact.

**Lesson**: Always validate parameter ranges against physical constraints. Datasheet specifications don't account for individual chassis geometry.

---

## Challenge 4: Line Detection Failure on Pink-Tinted Floor

**Problem**: The OpenCV line detector (threshold = 60) worked in test images but failed during deployment. The floor surface had a pink hue that wasn't accounted for.

**Diagnosis**:
1. Wrote a diagnostic script (`test_threshold.py`) that:
   - Captures an image of the actual deployment environment
   - Analyzes brightness distribution across the ROI
   - Tests multiple threshold values and outputs binary images for each
2. Found that the floor's actual grayscale brightness was around 100-130, much brighter than expected
3. The tape itself measured around 80-100 in brightness

**Solution**: Increased threshold from 60 to 120, allowing the system to distinguish tape from floor.

**Lesson**: Empirical environmental calibration is essential for computer vision. Lab conditions don't reflect deployment conditions.

---

## Challenge 5: Carving Inside Curves (P-Control Overshoot)

**Problem**: During gentle curves, the robot would cut to the inside of the line and lose track of it.

**Diagnosis**:
- Initial Kp = 0.002 made steering too aggressive
- The robot would overshoot the line, then the camera saw the line on the other side, causing oscillation
- In gentle curves, this oscillation pulled the robot toward the inside of the turn

**Solution**: 
1. Reduced Kp from 0.002 → 0.001 → tested → too sluggish
2. Tried Kp = 0.0015 → smooth tracking achieved
3. Also reduced SPEED from 40 to 30 to give the camera more decision time per unit of motion

**Lesson**: Control parameter tuning is iterative. Documenting the search process (what I tried and why) is as valuable as the final values.

---

## Challenge 6: Random vs Scanning-Based Obstacle Avoidance

**Problem (Initial)**: Random turn direction during obstacle avoidance could cause deadlocks — turning right repeatedly into a wall.

**Solution**: Implemented bidirectional distance scanning:
1. When an obstacle is detected, reverse the robot
2. During reverse: steer hard left, sample distance (this points the front camera right)
3. Then steer hard right, sample distance (this points the front camera left)
4. Compare the two distances; turn toward the more open side

This mimics how real autonomous vehicles use sensor fusion for path planning.

**Lesson**: Even simple sensor-driven decisions outperform random behavior in real environments.