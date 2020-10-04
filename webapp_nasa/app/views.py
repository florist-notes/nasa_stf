from app import app
from flask import render_template, request, redirect, jsonify, make_response
from datetime import datetime
#import image_slicer
import os
#import numpy
from werkzeug.utils import secure_filename


@app.template_filter('clean_date')
def clean_date(dt):
    return dt.strftime('%d %b %Y')


@app.route('/')
def index():
    return render_template('public/index.html')


@app.route('/map')
def map():
    return render_template('public/map2.html')

@app.route('/upload')
def upload():
    return render_template('public/upload.html')

@app.route('/fire')
def fire():
    return render_template('public/full.html')

@app.route('/draw')
def draw():
    return render_template('public/full1.html')

@app.route('/inform')
def inform():
    return render_template('public/inform.html')

@app.route('/thankyou2')
def thankyou2():
    return render_template('public/thankyou2.html')

@app.route('/thankyou')
def thankyou():
    return render_template('public/thankyou.html')

@app.route('/help')
def help():
    return render_template('public/help.html')

@app.route('/augment')
def augment():
    return render_template('public/locationar.html')

@app.route('/login', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        req = request.form
        username = req["username"]
        email = req.get("email")
        password = request.form["password"]

        print(username, email, password)
        return redirect('/thankyou')

    return render_template('public/login.html')


@app.route("/json", methods=["POST"])
def json():
    if request.is_json:
        req = request.get_json()
        response = {
            "message": "JSON Received!",
            "name": req.get("name")
        }
        res = make_response(jsonify(response), 200)
        return res
    else:
        res = make_response(jsonify({"message": "No JSON received"}), 400)
        return res


app.config["IMAGE_UPLOADS"] = "./app/static/img/uploads/"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG", " GIF"]

app.config["IMAGE_UPLOADS"] = "./app/static/img/uploads/" 
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPG", "JPEG", " GIF"]


def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route('/upload-image', methods=["GET","POST"])
def upload_image():
    if request.method == "POST":

        if request.files:
            image = request.files["image"]
            if image.filename == "":
                print("Image must have a filename")
                return redirect(request.url)

            if not allowed_image(image.filename):
                print("That image extension is not allowed")
                return redirect(request.url)
            else:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                #image_cut(filename)
            print("Image saved")
            filename = secure_filename(image.filename)
            #return redirect(request.url)
            return redirect('/thankyou2')

    return render_template("public/upload_image.html")