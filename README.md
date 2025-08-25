 # ReuniteAI - Missing Person Detection System
ReuniteAI is a web-based application that leverages AI, computer vision, and facial recognition to assist in locating missing persons. The system allows users to register missing individuals, upload videos for face detection, and automatically alerts guardians via email when a match is found.

🚀 Features:
1. Register Missing Persons – Store personal details and photos in a secure database.
2. Video Upload & Analysis – Extract frames from uploaded videos and run face recognition.
3. AI-Powered Matching – Detect and encode faces using the face_recognition library (dlib-based).
4. Automated Alerts – Send real-time email notifications to guardians if a match is detected.
5.Admin Dashboard – View, update, and manage missing persons’ records.

🛠️ Tech Stack:
1.Backend: Python (Flask)
2.Frontend: HTML, CSS, Bootstrap
3.Database: MySQL
4.Libraries: OpenCV, dlib, face_recognition
5.Other Tools: SMTP (for email alerts)

⚙️ Workflow:
1.User/Guardian registers a missing person with details & photo.
2.Uploaded video is processed → frames are extracted using OpenCV.
3.Faces are detected, encoded, and compared with the database.
4.If a match is found → system notifies guardian via email with details & last seen location.
5.Admin can view and manage all registered records.

