import cv2
import dlib
import numpy as np
import os
from PIL import Image

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('src/model/shape_predictor_68_face_landmarks.dat')

directory = "public/eye_detection_output"
directory_name = "public/is_facing_camera_output"

if os.path.exists(directory_name):
    for file in os.listdir(directory_name):
        file_to_remove = os.path.join(directory_name, file)
        os.remove(file_to_remove)
else:
    os.mkdir(directory_name)

frame_number = 0

def detect_gaze(image_path, frame_number):
    image = Image.open(os.path.join(directory, image_path))
    image = np.array(image)
    
    if image is None:
        # print("Invalid image")
        return frame_number
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)

    for face in faces:
        look = "idk"
        shape = predictor(gray, face)

        # Calculate the center of the eyes
        left_eye = np.array([shape.part(36).x, shape.part(36).y])
        right_eye = np.array([shape.part(45).x, shape.part(45).y])
        eye_center = (left_eye + right_eye) // 2

        image_width, image_height = image.shape[1], image.shape[0]
        
        reference_point = np.array([image_width // 2, image_height // 2])
        gaze_vector = eye_center - reference_point

        gaze_vector = gaze_vector.astype(float)
        gaze_vector /= np.linalg.norm(gaze_vector)

        gaze_angle_rad = np.arctan2(gaze_vector[1], gaze_vector[0])

        gaze_angle_deg = np.degrees(gaze_angle_rad)

        if (60 <= gaze_angle_deg < 140) or (-150 < gaze_angle_deg <= -90):
            look = "Yes"
            # print("Person is looking at the camera")
        else:
            look = "No"
            # print("Person is not looking at the camera")
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # cv2.imshow("Frame", image)

    print(look)
    if look == "Yes":
        print("The person is looking at the camera")
        frame_number += 1
        path = f"Frame{str(frame_number)}.jpg"
        print(path)
        write_success = cv2.imwrite(os.path.join(directory_name, path) , image)
        if not write_success:
            print("Could not write the image")

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return frame_number

for image in os.listdir(directory):
    frame_number = detect_gaze(image, frame_number)
