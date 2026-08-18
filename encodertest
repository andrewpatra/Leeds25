from gpiozero import RotaryEncoder
from signal import pause

# ------------------------------------------------------------
# WIRING
# ------------------------------------------------------------
# Encoder A / CLK  -> GPIO 17 (physical pin 11)
# Encoder Common   -> GND     (physical pin 9)
# Encoder B / DT   -> GPIO 18 (physical pin 12)
#
# No 3.3V or 5V connection is needed.
# gpiozero uses the Pi's internal pull-up resistors.
# ------------------------------------------------------------

encoder = RotaryEncoder(
    a=17,
    b=18,
    max_steps=0
)

def encoder_moved():
    print(f"Encoder step: {encoder.steps}")

# Run this function whenever the encoder moves
encoder.when_rotated = encoder_moved

print("Rotary encoder test")
print("-------------------")
print("Turn the encoder clockwise and counter-clockwise.")
print("Press Ctrl+C to quit.")
print()
print(f"Starting step: {encoder.steps}")

pause()
