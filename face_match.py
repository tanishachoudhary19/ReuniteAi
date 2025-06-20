import face_recognition
import cv2
import os
import smtplib
import ssl
from email.message import EmailMessage

# ✅ Email Configuration
EMAIL_SENDER = "choudharytanisha752@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "PBL123"   # Replace with an App Password
EMAIL_RECEIVER = "smridhi1603@gmail.com"  # Replace with recipient's email

# ✅ Define folders
database_folder = "missing_persons"  # Folder with stored missing persons' images
detected_faces_folder = "detected_faces"

# ✅ Load missing persons' encodings
missing_person_encodings = []
missing_person_names = []

print("\n🔍 Loading missing persons' data...")

for file in os.listdir(database_folder):
    img_path = os.path.join(database_folder, file)
    image = face_recognition.load_image_file(img_path)
    encodings = face_recognition.face_encodings(image)

    if encodings:
        missing_person_encodings.append(encodings[0])
        missing_person_names.append(file.split(".")[0])  # Extract name
        print(f"✅ Loaded: {file}")
    else:
        print(f"⚠️ No face found in {file}, skipping.")

if not missing_person_encodings:
    print("\n❌ No valid faces found in the database! Exiting...")
    exit()

print("\n🔍 Matching detected faces...\n")

# ✅ Function to send an email alert with an attached image
def send_email_alert(person_name, image_path):
    try:
        msg = EmailMessage()
        msg["Subject"] = f"🚨 Missing Person Detected: {person_name}"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg.set_content(f"A match has been found for {person_name}. Check the attached image.")

        # Attach image
        with open(image_path, "rb") as img:
            msg.add_attachment(img.read(), maintype="image", subtype="jpeg", filename=os.path.basename(image_path))

        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            print("🔄 Connecting to SMTP server...")
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            print("✅ Logged in successfully.")
            server.send_message(msg)

        print(f"📧 Alert sent: {person_name} detected in {image_path}")

    except smtplib.SMTPAuthenticationError:
        print("❌ SMTP Authentication Error: Check your email & app password.")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

# ✅ Compare detected faces (Stops after first match & shows frame)
match_found = False

for file in os.listdir(detected_faces_folder):
    if match_found:
        break  # Stop processing after first match

    img_path = os.path.join(detected_faces_folder, file)
    image = face_recognition.load_image_file(img_path)
    encodings = face_recognition.face_encodings(image)

    if not encodings:
        print(f"⚠️ No face detected in {file}, skipping.")
        continue

    for i, missing_encoding in enumerate(missing_person_encodings):
        match = face_recognition.compare_faces([missing_encoding], encodings[0], tolerance=0.5)

        if match[0]:  # If a match is found
            print(f"🎯 MATCH FOUND! {missing_person_names[i]} detected in {file}")

            # ✅ Display the matched frame
            frame = cv2.imread(img_path)
            cv2.imshow(f"Match Found: {missing_person_names[i]}", frame)
            cv2.waitKey(5000)  # Display for 5 seconds
            cv2.destroyAllWindows()

            # ✅ Send an email alert with the attached image
            send_email_alert(missing_person_names[i], img_path)

            match_found = True  # Set flag to stop further processing
            break  # Exit inner loop

if not match_found:
    print("\n❌ No match found in any frame.")

print("\n✅ Face matching & alert system completed.\n")
