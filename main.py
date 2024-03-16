from src.model.eyes_detection import eye_detection
from src.model.pose_estimation import detect_gaze
import os


def get_best_photo(video_path):
    eye_detection_success = eye_detection(video_path)

    if not eye_detection_success:
        print("Something went wrong while analysing user eyes")
        return False

    eyes_image_directory = "public/eye_detection_output"
    eyes_images = os.listdir(eyes_image_directory)

    frame_number = 1
    for image in eyes_images:
        detect_gaze(image, frame_number)

    return True

get_best_photo("public/Demo Videos/dance1.webm")