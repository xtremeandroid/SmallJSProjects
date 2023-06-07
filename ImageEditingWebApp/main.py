# pip install flask opencv-python

from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import cv2
import img2pdf
from PIL import Image

app = Flask(__name__)
app.secret_key = "the random string is here to save us from errors"

ALLOWED_EXTENSIONS = {"png", "webp", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def processImage(filename, operation):
    print(f"hello your operation is {operation} and filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            new_filename = f"static/{filename}"
            cv2.imwrite(new_filename, imgProcessed)
            return new_filename
        case "cwebp":
            new_filename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(new_filename, img)
            return new_filename
        case "cjpg":
            new_filename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(new_filename, img)
            return new_filename
        case "cpng":
            new_filename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(new_filename, img)
            return new_filename
        case "cpdf":
            new_filename = f"static/{filename.split('.')[0]}.pdf"
            imageforPDF = Image.open(f"uploads/{filename}")
            pdf_bytes = img2pdf.convert(imageforPDF.filename)
            file = open(f"static/{filename.split('.')[0]}.pdf", "wb")
            file.write(pdf_bytes)
            imageforPDF.close()
            file.close()
            return new_filename

    pass


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/how")
def how():
    return render_template("docs.html")


@app.route("/contactus")
def us():
    return render_template("contact.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return "error"
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return "error"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join("uploads", filename))
            new = processImage(filename, operation)
            flash(
                f"Your image has been processed and is available <a href='/{new}' target= '_blank'>here</a>"
            )
            return render_template("index.html")
    return render_template("index.html")


app.run(debug=True)
