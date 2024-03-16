import cv2
from ultralytics import YOLO

# Load your model
model = YOLO("src\model\yolov8m-pose.pt")

# Open the video
cap = cv2.VideoCapture("public/Demo Videos/dance1.webm")

# Process each frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run model prediction
    results = model(frame, show=False)

    # Example: Count people and add text annotation
    people_count = sum(1 for *_, cls in results.xyxy[0] if cls == 0)  # Assuming class 0 is 'person'
    cv2.putText(frame, f"People Count: {people_count}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Show the frame
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()