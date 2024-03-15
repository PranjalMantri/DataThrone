from src.model.youtube import download
from src.model.eyes_detection import eye_detection

# https://youtube.com/shorts/mMk7LZ6jRp0?si=nT0mt-B9fdc-lmvO

link = input("Enter a youtube link: ")
download_success, downloaded_video = download(link)

if not download_success:
    print("Could not download the video")

frames_to_process_per_second = 1

eye_detection_success = eye_detection(downloaded_video, frames_to_process_per_second)

if not eye_detection_success:
    print("Something went wrong while analysing user eyes")

