import time
import board
import busio
import sys
import select
import json
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# === SETUP ===
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 60  # Standard servo frequency

# Initialize servos (base, shoulder, elbow, gripper)
servos = [
    servo.Servo(pca.channels[0], min_pulse=500, max_pulse=2500),
    servo.Servo(pca.channels[1], min_pulse=500, max_pulse=2500),
    servo.Servo(pca.channels[2], min_pulse=500, max_pulse=2500),
    servo.Servo(pca.channels[3], min_pulse=500, max_pulse=2500)
]

angles = [90, 90, 90, 90]
for i, s in enumerate(servos):
    s.angle = angles[i]

motion_sequence = []

# === EASING AND QUIET MOTION HELPERS ===
def ease_in_out(t):
    return 3 * t ** 2 - 2 * t ** 3

def move_smooth_eased(servo, current, target, steps=25, duration=0.5):
    for i in range(steps + 1):
        t = i / steps
        eased_t = ease_in_out(t)
        angle = current + (target - current) * eased_t
        quiet_set_angle(servo, angle)
        time.sleep(duration / steps)

def quiet_set_angle(servo, target, tolerance=0.2):
    current = servo.angle if servo.angle is not None else 90
    if abs(current - target) > tolerance:
        servo.angle = target

def move_servo(index, delta):
    current = int(servos[index].angle or 90)
    new_angle = max(0, min(180, current + delta))
    angles[index] = new_angle
    move_smooth_eased(servos[index], current, new_angle)

# === SEQUENCE HANDLING ===
def record_step():
    motion_sequence.append({
        "angles": angles.copy(),
        "duration": 0.5
    })
    print("📸 Recorded:", motion_sequence[-1])

def save_sequence(filename="sequence.json"):
    with open(filename, "w") as f:
        json.dump(motion_sequence, f)
    print("💾 Sequence saved to", filename)

def load_sequence(filename="sequence.json"):
    try:
        with open(filename, "r") as f:
            sequence = json.load(f)
        print("📂 Loaded sequence from", filename)
        return sequence
    except Exception as e:
        print("⚠️ Error loading:", e)
        return []

def replay_sequence(sequence):
    print("🔁 Replaying sequence")
    for step in sequence:
        print("⏩ Step:", step["angles"])
        for i, target in enumerate(step["angles"]):
            current = int(servos[i].angle or 90)
            move_smooth_eased(servos[i], current, target)
        time.sleep(step["duration"])

# === UI ===
print("""
Control the Robot Arm:
  q/a - base        (left/right)
  w/s - shoulder    (up/down)
  e/d - elbow       (up/down)
  r/f - gripper     (open/close)

  SPACE - record pose
  z     - save sequence
  x     - replay sequence
""")

# === MAIN LOOP ===
while True:
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        key = sys.stdin.read(1)

        if key == 'q': move_servo(0, +5)
        elif key == 'a': move_servo(0, -5)
        elif key == 'w': move_servo(1, +5)
        elif key == 's': move_servo(1, -5)
        elif key == 'e': move_servo(2, +5)
        elif key == 'd': move_servo(2, -5)
        elif key == 'r': move_servo(3, +5)
        elif key == 'f': move_servo(3, -5)

        elif key == ' ':  # Record pose
            record_step()

        elif key == 'z':  # Save to file
            save_sequence()

        elif key == 'x':  # Load and replay
            seq = load_sequence()
            replay_sequence(seq)
