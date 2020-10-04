from app import app
from flask import render_template, request, redirect, jsonify, make_response


@app.template_filter('clean_date')
def clean_date(dt):
    return dt.strftime('%d %b %Y')


@app.route('/')
def index():
    return render_template('public/index.html')


@app.route('/map')
def map():
    return render_template('public/map2.html')


@app.route('/fire')
def fire():
    return render_template('public/full.html')

@app.route('/draw')
def draw():
    return render_template('public/full1.html')


@app.route('/login', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        req = request.form
        username = req["username"]
        email = req.get("email")
        message = request.form["message"]

        print(username, email, message)
        return redirect('/login')

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
