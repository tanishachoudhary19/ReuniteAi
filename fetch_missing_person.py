import mysql.connector
import face_recognition
import cv2
import os
import numpy as np

# ✅ Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="jaiguruji07",  # Replace with your actual MySQL password
    database="ReuniteAI"
)

cursor = conn.cursor()

# ✅ Fetch missing persons' details
cursor.execute("SELECT aadhaar, name, photo_path FROM missing_persons")
results = cursor.fetchall()

# ✅ Dictionary to store face encodings
missing_person_encodings = {}

for aadhaar, name, photo_path in results:
    if not os.path.exists(photo_path):
        print(f"⚠️ Image not found: {photo_path}")
        continue

    # ✅ Load image and get face encodings
    image = face_recognition.load_image_file(photo_path)
    encodings = face_recognition.face_encodings(image)

    if encodings:
        missing_person_encodings[aadhaar] = {
            "name": name,
            "encoding": encodings[0]  # Take the first detected face
        }
        print(f"✅ Encoded face for {name} (Aadhaar: {aadhaar})")
    else:
        print(f"⚠️ No face found in {photo_path}")

# ✅ Close the database connection
cursor.close()
conn.close()

# ✅ Save encodings for later use
np.save("missing_person_encodings.npy", missing_person_encodings)

print("\n🎯 All missing persons' face encodings stored successfully.")
