# Project Story

## Motivation

I wanted to build something that demonstrated my interest in **automotive technology and embedded systems** for my job search. Toyota and Honda are heavily investing in autonomous driving, so I chose to build a small autonomous vehicle from scratch — covering both hardware assembly and software implementation. The goal was to show that I can work across the full stack: from soldering wires to writing computer vision algorithms.

## Approach: Incremental Development

Instead of trying to build everything at once, I broke the project into 6 phases, each with a clear deliverable:

| Phase | Goal | Outcome |
|-------|------|---------|
| 1 | Set up development environment | Raspberry Pi OS, Python venv, OpenCV, Git workflow |
| 2 | Test each component individually | All sensors and actuators working in isolation |
| 3 | Assemble chassis, keyboard-controlled driving | Manually drivable robot |
| 4 | Autonomous obstacle avoidance | Robot avoids obstacles with ultrasonic sensors |
| 5 | Camera-based line tracing | Robot follows a black line using OpenCV + P-control |
| 6 | Refactor and documentation | Clean architecture, demos, this story |

This phased approach allowed me to verify each layer before adding complexity. When something broke, I always had a known-working state to fall back to.

## Architecture Decisions

### Why Class-Based Design?

Initially, I had test scripts scattered across files with hardcoded GPIO pin numbers. As the project grew, changing a single pin required edits in multiple places. I refactored everything into:

- `src/config.py` — all GPIO assignments and tunable constants in one place
- `src/motor.py`, `src/servo.py`, `src/ultrasonic.py`, `src/camera.py` — clean hardware abstraction classes
- `src/robot.py` — high-level integration of all hardware
- `apps/` — runnable applications using the abstractions

This separation lets me write new behaviors (like obstacle avoidance) without touching low-level GPIO code.

### Why Rear-Wheel Drive with Front-Wheel Steering (Not Differential Drive)?

The chassis kit I used had a servo-based front-wheel steering system, similar to a real car (Ackermann steering). While differential drive is simpler to program, Ackermann steering is closer to how actual vehicles work. This made the project more relevant to automotive applications.

### Why P-Control Instead of PID for Line Tracing?

I started with proportional (P) control to keep things simple. After tuning Kp through real-machine experiments, the robot follows the line well enough for demonstration. PID with derivative term could improve curve handling, but P-control is sufficient as a proof of concept and clearer to explain in interviews.

## What This Project Demonstrates

- **End-to-end systems thinking**: I understand how hardware constraints affect software design
- **Iterative debugging**: I can isolate problems, form hypotheses, and verify them empirically  
- **Maintainable code**: I write code that I (and others) can read in 6 months
- **Self-directed learning**: I learned PWM, OpenCV, Linux administration, Git workflows — all on my own