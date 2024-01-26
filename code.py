import board  # Import modules for hardware interaction
import audiomp3  # Import module for audio playback
import audiopwmio  # Import module for audio output
import adafruit_vl53l0x  # Import module for VL53L0X sensor
import busio  # Import module for I2C communication
import time  # Import module for time-related functions
import random  # Import module for random number generation
import os  # Import module for file system operations

# Initialize I2C communication
i2c = busio.I2C(board.SCL, board.SDA)

# Create sensor object
sensor = adafruit_vl53l0x.VL53L0X(i2c)

# Create audio output object
audio = audiopwmio.PWMAudioOut(board.A0)

# Get initial range reading
last_range = sensor.range

# Filter for MP3 files in the current directory
filenames = [file for file in os.listdir() if file.endswith(".mp3")]

while True:
    # Calculate absolute difference between current and previous readings
    current_range = sensor.range
    range_diff = abs(current_range - last_range)
    print('Range: {}mm'.format(current_range))

    # If range difference exceeds threshold (100mm), play a random MP3 file
    if range_diff > 100:
        filename = random.choice(filenames)  # Randomly select filename within the loop
        print('Playing: {}'.format(filename))
        decoder = audiomp3.MP3Decoder(open(filename, "rb"))
        audio.play(decoder)
        while audio.playing:
            time.sleep(0.1)
        time.sleep(3)

        # Update range to avoid immediate retriggering
        current_range = sensor.range
    last_range = current_range
    time.sleep(0.1)
