import cv2
import dlib
import numpy as np
import os

directory_name = "public/eye_detection_output"

if os.path.exists(directory_name):
    for file in os.listdir(directory_name):
        file_to_remove = os.path.join(directory_name, file)
        os.remove(file_to_remove)
    os.rmdir(directory_name)

os.mkdir(directory_name)


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("src/model/shape_predictor_68_face_landmarks.dat")

def detect_eyes(frame_gray, frame, frame_number):
    faces = detector(frame_gray)

    is_eyes_open = "Unknown"

    for face in faces:
        landmarks = predictor(frame_gray, face)

        left_eye_indices = list(range(36, 42))
        right_eye_indices = list(range(42, 48))

        left_eye_points = [(landmarks.part(idx).x, landmarks.part(idx).y) for idx in left_eye_indices]
        right_eye_points = [(landmarks.part(idx).x, landmarks.part(idx).y) for idx in right_eye_indices]

        left_eye_points = np.array(left_eye_points, np.int32)
        right_eye_points = np.array(right_eye_points, np.int32)

        # cv2.polylines(frame, [left_eye_points], True, (0, 0, 255), 1)
        # cv2.polylines(frame, [right_eye_points], True, (0, 0, 255), 1)

        left_ear = eye_aspect_ratio(left_eye_points)
        right_ear = eye_aspect_ratio(right_eye_points)

        ear = (left_ear + right_ear) / 2

        # Decrease this to increase accuracy (from what I tested 0.5 - 0.7 works best)
        closed_ear_thresh = 0.65

        if ear < closed_ear_thresh:
            is_eyes_open = "Closed"
            # cv2.putText(frame, 'Closed', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            is_eyes_open = "Open"
            # cv2.putText(frame, 'Open', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    print(f"{frame_number} + {is_eyes_open}")
    return frame, is_eyes_open

def eye_aspect_ratio(eye_points):
    # calculating vertical distance helps to understand whether eye is open or not
    vertical_dist1 = abs(((eye_points[1][0] - eye_points[5][0]) * 2 + (eye_points[1][1] - eye_points[5][1]) * 2)) ** 0.5
    vertical_dist2 = abs(((eye_points[2][0] - eye_points[4][0]) * 2 + (eye_points[2][1] - eye_points[4][1]) * 2)) ** 0.5

    # horizontal distance provides better results for different eye shapes
    horizontal_dist = abs(((eye_points[0][0] - eye_points[3][0]) * 2 + (eye_points[0][1] - eye_points[3][1]) * 2)) ** 0.5

    ear = (vertical_dist1 + vertical_dist2) / (2 * horizontal_dist)

    return ear

# change the video path
def eye_detection(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    # skip_ratio = 30 // frames_to_process
    frame_number = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break
        
        frame_count += 1
        frame_number += 1

        # taking 1 frame from 30 frames for now(adjust based on video length)
        # if frame_count % skip_ratio != 0:
        #     continue 

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame, is_eye_open = detect_eyes(frame_gray, frame, frame_number)

        # saving only those image that have open eyes
        if is_eye_open == "Open":
            path = f"{str(frame_number)}.jpg"
            os.chdir(directory_name)
            write_success = cv2.imwrite(path, frame)
            os.chdir("../../")
            
        if (cv2.waitKey(30) == 27):
            break

    cap.release()
    cv2.destroyAllWindows()
    return True

# eye_detection("public/Demo Videos/dance1.webm")
