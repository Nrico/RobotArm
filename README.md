# 🤖 Smooth Motion Robot Arm Controller (CircuitPython)

This project controls a 4-servo robot arm using CircuitPython and the PCA9685 PWM controller. It features **ease-in/ease-out smoothed motion**, keyboard-based control, and the ability to **record, save, and replay motion sequences**.

Designed for hobby robotics, creative coding, and educational demonstrations.

---

## 🔧 Features

- 🔁 **Control 4 servos**: base rotation, shoulder, elbow, and gripper
- ⌨️ **Keyboard interface** over USB serial (e.g., via Mu editor or screen)
- 🎞️ **Record and replay** motion sequences
- 🧈 **Smooth, eased motion** using cubic interpolation
- 🔇 **Deadband filtering** to reduce servo noise and jitter
- 💾 **Save motion sequences** to a `.json` file on the microcontroller
- 🧠 Future-ready: can be adapted for AI, remote control, or sensors

---

## 🧰 Hardware Requirements

- Microcontroller running **CircuitPython** (e.g., Feather, QT Py, etc.)
- **PCA9685 16-Channel PWM Servo Driver** (Adafruit or compatible)
- 4x standard 180° servos
- External power source for servos (recommended)
- USB connection to computer for keyboard control

---

## 📁 File Structure

