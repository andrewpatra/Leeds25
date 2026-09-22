from gpiozero import RotaryEncoder
from time import sleep
import vlc

# ------------------------------------------------------------
# VIDEO FILES
# ------------------------------------------------------------

video_files = [
    "/home/andrewp/Desktop/Leeds25/Assets/1.jpg",
    "/home/andrewp/Desktop/Leeds25/Assets/2.jpg",
    "/home/andrewp/Desktop/Leeds25/Assets/3.jpg",
    # Add more videos here
]

num_videos = len(video_files)

if num_videos == 0:
    raise RuntimeError("No video files were specified.")


# ------------------------------------------------------------
# ROTARY ENCODER
# ------------------------------------------------------------

# Encoder:
# A / CLK -> GPIO 17
# Common -> GND
# B / DT -> GPIO 18

encoder = RotaryEncoder(
    a=17,
    b=18,
    max_steps=0
)

# ------------------------------------------------------------
# VLC -- Initializes a single frame - make sure to update video files to match monitor size
# ------------------------------------------------------------

# Create one VLC instance
instance = vlc.Instance(
    "--no-osd",
    "--fullscreen"
    "--mouse-hide-timeout=0"
)

# Create one player
player = instance.media_player_new()

# Force fullscreen
player.set_fullscreen(True)


def play_video(index):
    media = instance.media_new(video_files[index])
    player.set_media(media)
    player.play()

    # Make sure we remain fullscreen
    player.set_fullscreen(True)

    print(f"Playing video {index}: {video_files[index]}")


# Start with the first video
play_video(0)


# Remember where the encoder started
last_encoder_step = encoder.steps

print("Ready.")
print(current_index)


# ------------------------------------------------------------
# MAIN LOOP
# ------------------------------------------------------------

try:

    while True:

        current_encoder_step = encoder.steps

        # ----------------------------------------------------
        # CLOCKWISE
        # ----------------------------------------------------

        if current_encoder_step > last_encoder_step:

            current_index += 1

            # Wrap around to the first video
            if current_index >= num_videos:
                current_index = 0

            play_video(current_index)


        # ----------------------------------------------------
        # COUNTER-CLOCKWISE
        # ----------------------------------------------------

        elif current_encoder_step < last_encoder_step:

            current_index -= 1

            # Wrap around to the last video
            if current_index < 0:
                current_index = num_videos - 1

            play_video(current_index)


        # Remember the encoder position
        last_encoder_step = current_encoder_step

        sleep(0.01)


except KeyboardInterrupt:

    print("\nStopping...")

    player.stop()