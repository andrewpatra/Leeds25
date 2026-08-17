from gpiozero import RotaryEncoder
from time import sleep
import vlc

# 1. Add your video file paths here (can be any amount, e.g., 4, 12, or 25!)
video_files = [
    "/home/andrewp/Desktop/Leeds25/Assets/1.jpg",
    "/home/andrewp/Desktop/Leeds25/Assets/2.jpg",
    "home/andrewp/Desktop/Leeds25/Assets/3.jpg",
    # ... add all your files here
]
num_videos = len(video_files)

# 2. Initialize VLC Player instances in the background
instance = vlc.Instance("--no-osd", "--fullscreen")
players = [instance.media_player_new() for _ in range(num_videos)]

for i, file_path in enumerate(video_files):
    media = instance.media_new(file_path)
    players[i].set_media(media)
    players[i].play()
    sleep(0.1) 
    players[i].set_pause(1) # Pre-load and pause on frame 1
    players[i].audio_set_mute(True)

# 3. Setup the 24-Detent Encoder Hardware
# gpiozero defaults to tracking steps mathematically
encoder = RotaryEncoder(17, 18, max_steps=24, wrap=False)

current_index = 0
players[current_index].set_pause(0) # Start playing the first video
players[current_index].audio_set_mute(False)

print("Ready.")

try:
    while True:
        # Scale the encoder's internal position value (-1.0 to 1.0) 
        # directly into a clean index matching our video array size
        raw_val = int((encoder.value + 1.0) * (num_videos - 1) / 2)
        new_index = max(0, min(raw_val, num_videos - 1))
        
        # If the user clicks into a new video zone, switch them instantly
        if new_index != current_index:
            players[current_index].set_pause(1)
            players[current_index].audio_set_mute(True)
            
            current_index = new_index
            players[current_index].set_pause(0)
            players[current_index].audio_set_mute(False)
            print(f"Playing Video Index: {current_index}")
            
        sleep(0.02) # Fast refresh rate for highly responsive physical tracking

except KeyboardInterrupt:
    for p in players:
        p.stop()
