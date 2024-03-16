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

    is_looking_in_camera = "idk"
    for face in faces:
        shape = predictor(gray, face)

        # to calculate the center of the eyes
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

        gaze_angle_deg = abs(gaze_angle_deg)
        # cv2.putText(image, f"Angle {gaze_angle_deg}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        if (65.5 <= gaze_angle_deg < 83):
            is_looking_in_camera = "Yes"
            # print("Person is looking at the camera")
        # elif (81 <= gaze_angle_deg < 95):
        #     look = "Yes"
        elif (110 <= gaze_angle_deg < 120):
            is_looking_in_camera = "Yes"
        else:
            is_looking_in_camera = "No"
            # print("Person is not looking at the camera")
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # cv2.imshow("Frame", image)

    print(is_looking_in_camera)
    if is_looking_in_camera == "Yes":
        frame_number += 1
        path = f"Frame{str(frame_number)}.jpg"
        print(path)
        write_success = cv2.imwrite(os.path.join(directory_name, path) , image)
        if not write_success:
            print("Could not write the image")

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return frame_number

# for image in os.listdir(directory):
#     frame_number = detect_gaze(image, frame_number)