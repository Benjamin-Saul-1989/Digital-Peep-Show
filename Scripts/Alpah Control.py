import pygame
import RPi.GPIO as GPIO
import time
import subprocess

# Set up GPIO pin
GPIO_PIN = 17  # Adjust the pin number based on your configuration
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN)

# Set up Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))  # Adjust the resolution as needed
pygame.display.set_caption("Image and Video Player")

# Load static image
static_image = pygame.image.load("static_image.jpg")
static_image = pygame.transform.scale(static_image, (800, 600))

# Load video
video_file = "video.mp4"  # Adjust the video file name
video_process = None

# Main loop
try:
    while True:
        # Check GPIO pin state
        if GPIO.input(GPIO_PIN) == GPIO.HIGH:
            # GPIO pin is high, play the video
            if video_process is None or video_process.poll() is not None:
                video_process = subprocess.Popen(["omxplayer", "-b", "--no-osd", video_file])

        # Display static image
        screen.blit(static_image, (0, 0))
        pygame.display.flip()

        # Check if the video has finished
        if video_process is not None and video_process.poll() is not None:
            # Video has ended, set video_process to None
            video_process = None

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        time.sleep(0.1)  # Adjust the sleep duration as needed

finally:
    GPIO.cleanup()
