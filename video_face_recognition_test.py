import cv2
import face_recognition
import mysql.connector
import os
from datetime import datetime

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="jaiguruji07",  # Use your actual password here
    database="ReuniteAI"
)
cursor = db.cursor()

# Fetch missing persons from the database
cursor.execute("SELECT aadhaar, name, dob, phone_number, residential_address, mother_name, father_name, lost_on, skin_color, photo_path FROM missing_persons")
missing_persons = cursor.fetchall()

# Store known encodings and details
known_encodings = []
missing_data = {}

for person in missing_persons:
    aadhaar, name, dob, phone_number, residential_address, mother_name, father_name, lost_on, skin_color, photo_path = person

    if not os.path.exists(photo_path):
        print(f"Image not found: {photo_path}")
        continue

    image = face_recognition.load_image_file(photo_path)
    encoding = face_recognition.face_encodings(image)

    if len(encoding) > 0:
        known_encodings.append(encoding[0])
        missing_data[aadhaar] = {
            "name": name,
            "dob": dob.strftime("%Y-%m-%d"),
            "phone": phone_number,
            "address": residential_address,
            "mother": mother_name,
            "father": father_name,
            "lost_on": lost_on.strftime("%Y-%m-%d"),
            "skin_color": skin_color
        }
    else:
        print(f"Face not found in image: {photo_path}")

cursor.close()
db.close()

# Output folder
output_folder = "detected_faces"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load video
video_capture = cv2.VideoCapture("video.mp4")
match_found = False  # Track if any match is found

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)

        if True in matches:
            match_index = matches.index(True)
            matched_aadhaar = list(missing_data.keys())[match_index]
            person_details = missing_data[matched_aadhaar]

            # Draw green box & label
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, f"{person_details['name']} ({matched_aadhaar})", (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            details_text = f"DOB: {person_details['dob']}, Skin: {person_details['skin_color']}"
            cv2.putText(frame, details_text, (left, bottom + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Save detected face
            face_image = frame[top:bottom, left:right]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{output_folder}/{matched_aadhaar}_{person_details['name']}_{timestamp}.jpg"
            cv2.imwrite(filename, face_image)
            print(f"✅ Detected {person_details['name']} (Aadhaar: {matched_aadhaar}) - Saved as {filename}")

            match_found = True
            break  # Stop loop on first match

    cv2.imshow("Video", frame)

    if match_found:
        print("✅ Match found. Stopping video.")
        cv2.waitKey(2000)  # Wait for 2 seconds to show result
        break

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
