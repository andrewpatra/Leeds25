from gpiozero import RotaryEncoder
from time import sleep
import vlc

# ------------------------------------------------------------
# ROTARY ENCODER WIRING
# ------------------------------------------------------------
#
# 3-pin mechanical rotary encoder:
#
# Encoder A / CLK  ---> GPIO 17 (physical pin 11)
# Encoder Common   ---> GND     (physical pin 9)
# Encoder B / DT   ---> GPIO 18 (physical pin 12)
#
# NO 3.3V or 5V connection is required.
#
# gpiozero enables the Raspberry Pi's internal pull-up
# resistors on GPIO 17 and GPIO 18. This holds the GPIO pins
# HIGH until the encoder connects them to GND.
# ------------------------------------------------------------


# 1. Add your video file paths here
video_files = [
    "/home/andrewp/Desktop/Leeds25/Assets/1.jpg",
    "/home/andrewp/Desktop/Leeds25/Assets/2.jpg",
    "/home/andrewp/Desktop/Leeds25/Assets/3.jpg",
    # Add additional videos here
]

num_videos = len(video_files)


# 2. Initialize VLC Player instances in the background
instance = vlc.Instance("--no-osd", "--fullscreen")

players = [
    instance.media_player_new()
    for _ in range(num_videos)
]

for i, file_path in enumerate(video_files):
    media = instance.media_new(file_path)
    players[i].set_media(media)

    # Start VLC briefly so the video gets loaded
    players[i].play()
    sleep(0.1)

    # Pause on the first frame
    players[i].set_pause(1)
    players[i].audio_set_mute(True)


# ------------------------------------------------------------
# 3. SET UP THE 3-PIN ROTARY ENCODER
# ------------------------------------------------------------
#
# GPIO Zero's RotaryEncoder uses pull-up resistors by default.
#
# This means:
#
# GPIO 17 ---- internal pull-up ---- 3.3V
# GPIO 18 ---- internal pull-up ---- 3.3V
#
# The encoder switches those GPIO pins to GND as it rotates.
#
# max_steps=0 means we don't limit the encoder to a fixed
# numerical range. We just watch for individual steps.
# ------------------------------------------------------------

encoder = RotaryEncoder(
    a=17,
    b=18,
    max_steps=0
)


# 4. Start with Video 0
current_index = 0

players[current_index].set_pause(0)
players[current_index].audio_set_mute(False)

# Remember the encoder's starting position
last_encoder_step = encoder.steps

print("System initialized.")
print("Turn the knob to change videos.")


try:
    while True:

        # Read the current encoder position
        current_encoder_step = encoder.steps

        # ----------------------------------------------------
        # CLOCKWISE
        # ----------------------------------------------------
        if current_encoder_step > last_encoder_step:

            # Pause current video
            players[current_index].set_pause(1)
            players[current_index].audio_set_mute(True)

            # Move forward one video
            current_index += 1

            # Wrap from the last video back to Video 0
            if current_index >= num_videos:
                current_index = 0

            # Play new video
            players[current_index].set_pause(0)
            players[current_index].audio_set_mute(False)

            print(f"Playing Video Index: {current_index}")


        # ----------------------------------------------------
        # COUNTER-CLOCKWISE
        # ----------------------------------------------------
        elif current_encoder_step < last_encoder_step:

            # Pause current video
            players[current_index].set_pause(1)
            players[current_index].audio_set_mute(True)

            # Move backward one video
            current_index -= 1

            # Wrap from Video 0 to the last video
            if current_index < 0:
                current_index = num_videos - 1

            # Play new video
            players[current_index].set_pause(0)
            players[current_index].audio_set_mute(False)

            print(f"Playing Video Index: {current_index}")


        # Save encoder position for the next loop
        last_encoder_step = current_encoder_step

        # Fast polling
        sleep(0.01)


except KeyboardInterrupt:

    print("\nStopping...")

    for p in players:
        p.stop()