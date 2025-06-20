from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Folder to save uploads
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.secret_key = 'your_secret_key'

# Database connection
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="jaiguruji07",
        database="reuniteai"
    )
    cursor = db.cursor(dictionary=True)
    print("✅ Database connected successfully!")
except mysql.connector.Error as err:
    print(f"❌ Error connecting to database: {err}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        aadhaar = request.form.get("aadhaar")
        name = request.form.get("name")
        dob = request.form.get("dob")
        phone = request.form.get("phone")
        address = request.form.get("address")
        mother = request.form.get("mother")
        father = request.form.get("father")
        lost_on = request.form.get("lost_on")
        skin_color = request.form.get("skin_color")
        guardian_email = request.form.get("guardian_email")
        location = request.form.get("location")

        photo = request.files.get("photo")
        photo_filename = None

        if photo and photo.filename:
            photo_path = os.path.join(app.config["UPLOAD_FOLDER"], photo.filename)
            photo.save(photo_path)
            photo_filename = photo_path.replace("\\", "/")

        sql = """
        INSERT INTO missing_persons 
        (aadhaar, name, dob, phone_number, residential_address, mother_name, father_name, lost_on, skin_color, photo_path, guardian_email, location) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (aadhaar, name, dob, phone, address, mother, father, lost_on, skin_color, photo_filename, guardian_email, location)

        try:
            cursor.execute(sql, values)
            db.commit()
            print("✅ Data inserted successfully!")

            sender_email = "tanishaachoudhary7@gmail.com"
            sender_password = "gvyq cbhf pxpd zhga"

            subject = "Missing Person Registration Confirmation"
            body = f"""
Dear Guardian,

This is to confirm that the missing person case for "{name}" has been successfully registered.

📍 Last Known Location: {location}
👤 Name: {name}
📅 Date of Birth: {dob}
📞 Phone: {phone}
👨 Father: {father}
👩 Mother: {mother}
📆 Missing Since: {lost_on}

We will alert you immediately if we detect a match through our system.

Regards,  
Reunite AI Team
"""

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = guardian_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
                server.quit()
                print("✅ Email sent successfully.")
            except Exception as e:
                print(f"❌ Error sending email: {e}")

            flash('✅ Person registered successfully and email sent!', 'success')
            return redirect(url_for("register"))
        except mysql.connector.Error as err:
            print(f"❌ Error inserting data: {err}")
            return f"Error: {err}"

    return render_template("register.html")

@app.route("/adminLogin")
def adminLogin():
    return render_template("adminLogin.html")

@app.route("/adminDashboard")
def admin_dashboard():
    return render_template("adminDashboard.html")

@app.route('/registered_people')
def registered_people():
    try:
        cursor.execute("SELECT aadhaar, name, dob, phone_number, residential_address, photo_path FROM missing_persons")
        data = cursor.fetchall()
        return render_template('registered_people.html', persons=data)
    except mysql.connector.Error as err:
        return f"❌ Error fetching data: {err}"

@app.route('/upload_video', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        video = request.files.get('video')
        location = request.form.get('location', 'Unknown Location')

        if video and video.filename:
            video_path = os.path.join(app.config["UPLOAD_FOLDER"], video.filename)
            video.save(video_path)

            from video_face_recognition import recognize_faces_from_video
            match_result = recognize_faces_from_video(video_path, location)

            if match_result and match_result.get('match_found'):
                matched_name = match_result.get('name')
                guardian_email = match_result.get('guardian_email')
                dob = match_result.get('dob')
                phone = match_result.get('phone')
                father = match_result.get('father')
                mother = match_result.get('mother')
                lost_on = match_result.get('lost_on')

                sender_email = "tanishaachoudhary7@gmail.com"
                sender_password = "gvyq cbhf pxpd zhga"

                subject = f"🚨 Match Found for Missing Person: {matched_name}"
                body = f"""
Dear Guardian,

We have detected a possible match for the missing person "{matched_name}" using a video uploaded through our system.

📍 Last Seen Location: {location}
👤 Name: {matched_name}
📅 Date of Birth: {dob}
📞 Phone: {phone}
👨 Father: {father}
👩 Mother: {mother}
📆 Missing Since: {lost_on}

Please verify this information and reach out to local authorities immediately.

Regards,  
Reunite AI Team
"""

                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = guardian_email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))

                try:
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.send_message(msg)
                    server.quit()
                    print("✅ Match email sent successfully.")
                except Exception as e:
                    print(f"❌ Error sending match email: {e}")

            return render_template('result.html', match=match_result)
        else:
            return "❌ No video selected."

    return render_template('upload_video.html')

if __name__ == "__main__":
    app.run(debug=True)
