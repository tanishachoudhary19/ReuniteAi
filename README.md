#🔎 ReuniteAI - Missing Person Detection System
ReuniteAI is a web-based application that leverages AI, computer vision, and facial recognition to assist in locating missing persons. The system allows users to register missing individuals, upload videos for face detection, and automatically alerts guardians via email when a match is found.

🚀 Features
1. Register Missing Persons – Store personal details and photos in a secure database.
2. Video Upload & Analysis – Extract frames from uploaded videos and run face recognition.
3. AI-Powered Matching – Detect and encode faces using the face_recognition library (dlib-based).
4. Automated Alerts – Send real-time email notifications to guardians if a match is detected.
5.Admin Dashboard – View, update, and manage missing persons’ records.

🛠️ Tech Stack
Backend: Python (Flask)
Frontend: HTML, CSS, Bootstrap
Database: MySQL
Libraries: OpenCV, dlib, face_recognition
Other Tools: SMTP (for email alerts)

⚙️ Workflow
User/Guardian registers a missing person with details & photo.
Uploaded video is processed → frames are extracted using OpenCV.
Faces are detected, encoded, and compared with the database.
If a match is found → system notifies guardian via email with details & last seen location.
Admin can view and manage all registered records.


🔗 Integration with national/police databases for broader reach.

🎯 Multimodal AI (voice, clothing, gesture recognition) for better accuracy.
