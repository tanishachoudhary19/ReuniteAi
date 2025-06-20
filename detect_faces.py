# import cv2
# import os

# # ✅ Load the face detection model
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# # ✅ Define input and output folders
# frames_folder = "frames"
# output_folder = "detected_faces"
# os.makedirs(output_folder, exist_ok=True)

# # ✅ Get a sorted list of all frame images
# frame_files = sorted(os.listdir(frames_folder))

# # ✅ Set a frame processing limit
# MAX_FRAMES = 200  

# try:
#     frame_count = 0  # Track processed frames

#     for frame_file in frame_files:
#         if frame_count >= MAX_FRAMES:  # Stop at 200 frames
#             print("\n🎯 Stopped after processing 200 frames.\n")
#             break  

#         frame_path = os.path.join(frames_folder, frame_file)
#         img = cv2.imread(frame_path)

#         if img is None:
#             print(f"❌ Skipping {frame_file}: Unable to read image.")
#             continue

#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(
#             gray, 
#             scaleFactor=1.1, 
#             minNeighbors=5, 
#             minSize=(30, 30)
#         )

#         face_detected = False

#         for i, (x, y, w, h) in enumerate(faces):
#             face_img = img[y:y+h, x:x+w]
#             face_path = os.path.join(output_folder, f"{frame_file}_face_{i}.jpg")

#             if face_img.size == 0:
#                 print(f"⚠️ Skipped empty face in {frame_file}")
#                 continue

#             cv2.imwrite(face_path, face_img)
#             print(f"✅ Face saved: {face_path}")
#             face_detected = True

#         if not face_detected:
#             print(f"⚠️ No face detected in {frame_file}")

#         # ✅ Increment frame count only after processing a frame
#         frame_count += 1
#         print(f"Processing frame {frame_count}/{MAX_FRAMES}...")  

# except KeyboardInterrupt:
#     print("\n⏹️ Script interrupted by user. Exiting...\n")

# print("\n✅ Face detection completed successfully. Exiting script.\n")


import cv2
import os

def detect_faces(video_path):
    # Load the video
    cap = cv2.VideoCapture(video_path)
    detected = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Placeholder logic (replace with actual face detection)
        detected.append("Person Detected in Frame")  

    cap.release()
    return detected
