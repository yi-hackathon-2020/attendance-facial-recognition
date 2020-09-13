import logging
import pickle
from flask import Flask
from flask import render_template, request, redirect, url_for
import pandas as pd
from mtcnn.mtcnn import MTCNN
import face_recognition
import imageio
from form import Upload
import database as db


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config["static_url_path"] = "/static"


# Path to pickle file
loaded_model = pickle.load(open("model.sav", "rb"))


def predict_face(path, day):
    detector = MTCNN()
    img = imageio.imread(path)
    faces = detector.detect_faces(img)

    for face in faces:
        box = face["box"]
        box = (box[1], box[0] + box[2], box[1] + box[3], box[0])
        encodings = face_recognition.face_encodings(img, [box])
        predictions = loaded_model.predict_proba(encodings)
        index = loaded_model.predict(encodings)
        temp = predictions[0]
        if temp[index[0]] >= 0.60:  # Threshold
            db.update_student_attendance(int(index[0]), day)

        else:
            print(
                f"Probably {db.get_name_by_rollnum(int(index[0]))}'s face detected. "
                f"Probability: {predictions[0][index[0]]}"
            )

    db.mark_remaining_absent(day)


@app.route("/")
def home():
    return render_template("home.html", title="One-Click Attendance")


@app.route("/student")
def student():
    return render_template("student.html", title="Attendance Details")


@app.route("/staff")
def staff():
    return render_template("staff.html", title="Select class")


@app.route("/staff/first", methods=["POST", "GET"])
def first():
    uploads = Upload()
    if request.method == "POST":
        if "submit" in request.form:
            file = request.files["file"]
            day = uploads.day.data
            predict_face(file, day)

            return redirect(url_for("display"))

    return render_template("first.html", title="Select class", uploads=uploads)


@app.route("/staff/first/display")
@app.route("/student/first")
def display():
    df = pd.read_sql_table("students", db.DB_URI)
    titles = ["Roll Number", "Name"]
    titles.extend([f"{i:02d}" for i in range(1, 32)])
    df.columns = titles
    df = df.fillna(value=" ")
    df = df.applymap(
        lambda x: "<P>"
        if type(x) == bool and x == True
        else ("<A>" if type(x) == bool and x == False else x)
    )

    html = df.to_html(classes="data", index=False)
    html = html.replace("&lt;P&gt;", '<span class="present">P</span>')
    html = html.replace("&lt;A&gt;", '<span class="absent">A</span>')

    return render_template("show.html", tables=[html], titles="",)


if __name__ == "__main__":
    app.run(threaded=True)
