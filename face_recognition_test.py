import face_recognition
import cv2
import numpy as np

# Load the missing person's image
image_path = r"C:\Users\HP\Downloads\ReuniteAI\smridhi.jpg"  # Use raw string (r"") to handle backslashes
image = face_recognition.load_image_file(image_path)

# Get facial encodings
face_encodings = face_recognition.face_encodings(image)

if face_encodings:
    print("Face encoding successful! Encoded face found in the image.")
else:
    print("No face detected in the image.")
