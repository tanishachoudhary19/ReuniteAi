import cv2
import face_recognition
import mysql.connector
import os
import numpy as np
import smtplib
from email.message import EmailMessage

# ✉️ Send Email Function
def send_email(to_email, person_name, location):
    msg = EmailMessage()
    msg['Subject'] = f"Missing Person {person_name} Found!"
    msg['From'] = "tanishaachoudhary7@gmail.com"  # Replace with your sender email
    msg['To'] = to_email

    msg.set_content(
        f"""Good news!

The missing person "{person_name}" has potentially been identified.

📍 Last Detected Location: {location}

Please contact authorities or check the ReuniteAI portal for more info.

Regards,  
ReuniteAI Team
"""
    )

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("tanishaachoudhary7@gmail.com", "gvyq cbhf pxpd zhga")  # Use your App Password
            smtp.send_message(msg)
        print("✅ Email sent successfully to guardian.")
    except Exception as e:
        print("❌ Failed to send email:", e)

# 🎥 Face Recognition Function
def recognize_faces_from_video(video_path, location):
    # Database connection
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="jaiguruji07",
        database="reuniteai"
    )
    cursor = db.cursor()

    # Fetch missing person records
    cursor.execute("SELECT aadhaar, name, dob, phone_number, residential_address, mother_name, father_name, lost_on, skin_color, photo_path, guardian_email FROM missing_persons")
    missing_persons = cursor.fetchall()

    known_encodings = []
    missing_data = {}

    for person in missing_persons:
        aadhaar, name, dob, phone_number, residential_address, mother_name, father_name, lost_on, skin_color, photo_path, guardian_email = person
        if not os.path.exists(photo_path):
            continue

        image = face_recognition.load_image_file(photo_path)
        encoding = face_recognition.face_encodings(image)
        if len(encoding) > 0:
            known_encodings.append(encoding[0])
            missing_data[aadhaar] = {
                "aadhaar": aadhaar,
                "name": name,
                "dob": dob.strftime("%Y-%m-%d"),
                "phone": phone_number,
                "address": residential_address,
                "mother": mother_name,
                "father": father_name,
                "lost_on": lost_on.strftime("%Y-%m-%d"),
                "skin_color": skin_color,
                "email": guardian_email
            }

    cursor.close()
    db.close()

    # Load video
    video_capture = cv2.VideoCapture(video_path)
    matched_person = None
    frame_count = 0

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % 3 != 0:
            continue

        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if face_distances[best_match_index] < 0.55:
                matched_aadhaar = list(missing_data.keys())[best_match_index]
                matched_person = missing_data[matched_aadhaar]

                top *= 2
                right *= 2
                bottom *= 2
                left *= 2

                # 🟩 Draw green box around matched face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, matched_person["name"], (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                start_time = cv2.getTickCount()  
                while True:
                    elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
                    if elapsed_time > 5:  
                        break
                    cv2.imshow('Video', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'): 
                        break

                # ✉️ Send alert with location
                send_email(matched_person["email"], matched_person["name"], location)

                matched_person["last_seen_location"] = location  
                video_capture.release()
                cv2.destroyAllWindows()
                return matched_person

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return None
