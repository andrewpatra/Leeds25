from gpiozero import RotaryEncoder
from time import sleep
import vlc

# ------------------------------------------------------------
# VIDEO FILES
# ------------------------------------------------------------

video_files = [
    "/home/andrewp/Desktop/Leeds25/Assets/1.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/2.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/3.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/4.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/5.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/6.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/7.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/8.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/9.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/10.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/11.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/12.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/13.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/14.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/15.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/16.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/17.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/18.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/19.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/20.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/21.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/22.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/23.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/24.mp4",
    "/home/andrewp/Desktop/Leeds25/Assets/25.mp4",
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
# VLC -- ONE PLAYER + MEDIA LIST PLAYER
# ------------------------------------------------------------

instance = vlc.Instance(
    "--no-osd",
    "--fullscreen"
)

# The MediaListPlayer manages switching between media while
# using one underlying VLC media player/window.
player = instance.media_player_new()
media_list = instance.media_list_new()

for file_path in video_files:
    media = instance.media_new(file_path)
    media_list.add_media(media)

list_player = instance.media_list_player_new()
list_player.set_media_player(player)
list_player.set_media_list(media_list)


# ------------------------------------------------------------
# VIDEO CONTROL
# ------------------------------------------------------------

current_index = 0


def play_video(index):
    """Play the selected item from the VLC media list."""

    global current_index

    current_index = index

    print(f"Playing video {current_index}: {video_files[current_index]}")

    # Switch to the selected item in the existing VLC player.
    list_player.play_item_at_index(current_index)


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

    list_player.stop()
    player.stop()
