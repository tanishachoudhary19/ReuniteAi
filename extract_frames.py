import cv2
import os

video_path = "video.mp4"  # Path to your input video
output_folder = "frames"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

cap = cv2.VideoCapture(video_path)
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
    cv2.imwrite(frame_path, frame)
    frame_count += 1

cap.release()
cv2.destroyAllWindows()
print(f"Extracted {frame_count} frames from {video_path}")
