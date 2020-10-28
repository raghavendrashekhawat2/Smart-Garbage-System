# import mysql.connector
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sessions import Session
from tempfile import mkdtemp
from functools import wraps


app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def apology(message, code=400):
    return render_template("apology.html", msg=message, code=code)


@app.route("/")
def index():
    conn = sqlite3.connect('garbage.db')
    db = conn.execute("SELECT * FROM loc")
    conn.commit()
    complete_list = db.fetchall()
    print("true")
    return render_template("map.html", latt=30.326738, lngg=78.025269, l=complete_list)


@app.route("/login", methods=["POST", "GET"])
def login():
    conn = sqlite3.connect('garbage.db')

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            print("n1")
            return apology("\nEnter username and password", 400)
        db = conn.execute("SELECT * FROM users WHERE user_name = :username ", {"username": username})
        rows = db.fetchone()
        print(generate_password_hash(password))

        if not check_password_hash(rows[3], password):
            print("n2")
            return apology("\n Invalid username or password!!! :(", 400)
        session["user_id"] = rows[0]
        # Implementation of main homepage

        return render_template("home.html")
    else:
        return render_template("login.html")


# Register for an account for the system
@app.route("/register", methods=["POST", "GET"])
def register():
    conn = sqlite3.connect('garbage.db')
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        repassword = request.form.get("repassword")
        name = request.form.get("name")
        gender = request.form.get("acc_type")
        print(username)
        print(password)
        print(repassword)
        if not username or not password or not repassword:
            print("n1")
            return apology("Please enter all details", 400)

        if not repassword == password:
            print("n2")
            return apology("Passwords do not match :(", 400)

        db = conn.execute("SELECT * FROM users WHERE user_name = :user_name", {"user_name": username})
        conn.commit()
        row = db.fetchall()
        print(row)
        if len(row) > 0:
            print("n3")
            return apology("Username is already taken :O", 404)
        hash_pass = generate_password_hash(password)
        print(hash_pass)
        # Incrementing the value of primary key.
        db = conn.execute("INSERT INTO users(user_id, name, user_name, password, gender)"
                   " VALUES(NULL, :name, :username, :hash_p, :g )",
                   {"name": name, "username": username, "hash_p": hash_pass, "g": gender})
        conn.commit()
        print(db.fetchall())
        flash("Registered")
        return render_template("login.html")
    else:
        return render_template("register.html")


# Insert bins to the existing system
@app.route("/Insert_bins", methods=["POST", "GET"])
@login_required
def Insert_bins():
    if request.method == "POST":
        conn = sqlite3.connect('garbage.db')
        country = request.form.get("country")
        state = request.form.get("state")
        city = request.form.get("city")
        lat = request.form.get("lat")
        lng = request.form.get("lng")

        if request.form.get("imp_loc"):
            p1 = 10
        else:
            p1 = 0

        if not country or not state or not city or not lat or not lng:
            return apology("Enter all details !!", 404)
        db = conn.execute("INSERT INTO loc (bin_id, country, state, city, lat, lng, imp_location)"
                   " VALUES (NULL, :country, :state, :city, :lat, :lng, :p )",
                   {"country": country, "state": state, "city": city, "lat": lat, "lng": lng, "p": p1})
        conn.commit()
        flash("Inserted")
        return render_template("Insert_bins.html")
    else:
        return render_template("Insert_bins.html")


# Function to logout
@app.route("/logout", methods=["GET"])
@login_required
def logout():
    session.clear()
    return redirect("/")


# Function to remove bins and displaying all bins with all their details
@app.route("/home", methods=["POST", "GET"])
@login_required
def remove_bins():
    conn = sqlite3.connect('garbage.db')
    db = conn.execute("SELECT * FROM loc")
    conn.commit()
    rows = db.fetchall()
    db.execute("SELECT * FROM g_list")
    conn.commit()
    r = db.fetchall()
    if request.method == 'POST':
        bin_id = int(request.form.get("binid"))
        if not bin_id:
            return apology("Enter bin_id")
        db.execute("DELETE from loc WHERE bin_id = :bin", {"bin": bin_id})
        conn.commit()
        db.execute("DELETE from g_list WHERE bin_id = :bin", {"bin": bin_id})
        conn.commit()
        return render_template("home.html", data=rows, data_2=r)
    else:
        print(rows, "\n", r)
        return render_template("home.html", data=rows, data_2=r)


@app.route("/maps", methods=["POST", "GET"])
def maps():
    conn = sqlite3.connect('garbage.db')
    # conn = mysql.connector.connect(user='root', password='', host='localhost', database='garbage1')
    country = request.form.get("country")
    state = request.form.get("state")
    city = request.form.get("city")
    lat = request.form.get('lat')
    lng = request.form.get('lng')
    # Receiving AJAX request
    if lat is not None and lng is not None:
        lat = float(lat)
        lng = float(lng)
        db = conn.execute("SELECT bin_id FROM loc WHERE lat = :lat and lng = :lng ", {"lat": lat, "lng": lng})
        conn.commit()
        r = db.fetchone()
        bin_id = r[0]
        print(bin_id)
        db.execute("SELECT * FROM g_list WHERE bin_id = :bin_id", {"bin_id": bin_id})
        conn.commit()
        bin_details = db.fetchone()
        print(bin_details)
        return jsonify({"g_array": bin_details})

    if not country:
        return apology("Enter Country")
    if not state:
        return apology("Enter State")
    if not city:
        return apology("Enter city")

    db = conn.execute("SELECT * FROM loc WHERE country = :country and state = :state and city = :city",
               {"country": country, "state": state, "city": city})
    conn.commit()
    row = db.fetchone()
    db.execute("SELECT * FROM loc")
    conn.commit()
    complete_list = db.fetchall()
    if request.method == "POST":
        if not row:
            return apology("Smart garbage system has not been initiated in the specified location ")
        else:
            return render_template("map.html", latt=row[4], lngg=row[5], l=complete_list)

    else:
        return render_template("map.html", latt=row[4], lngg=row[5], l=complete_list)


@app.route("/analysis", methods=["POST","GET"])
def analysis():
    conn = sqlite3.connect('garbage.db')
    db = conn.execute("SELECT * FROM history")
    conn.commit()
    data1 = db.fetchall()
    db = conn.execute("SELECT * FROM loc")
    conn.commit()
    data2 = db.fetchall()
    if request.method == "POST":
        print("");

    else:
        return render_template("Analysis.html", d1=data1, d2=data2)


if __name__ == '___main__':
    app.run()
