import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, lookupmoon, rover, marsweather, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///space.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Mdust provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Must provide username", 400)
        elif not request.form.get("password"):
            return apology("Must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("Please confirm password", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords must match", 400)
        elif request.form.get("username") in [list(i) for i in db.execute("SELECT username FROM users")]:
            return apology("Username is taken", 400)
        rows = db.execute("SELECT * FROM users WHERE username=:username", username=request.form.get("username"))
        if len(rows) != 0:
            return apology("Username is taken", 400)
        hashedpassword = generate_password_hash(request.form.get("password"))
        insertuser = db.execute("INSERT INTO 'users' ('username','hash') VALUES (:username, :hash)", username=request.form.get("username"), hash=hashedpassword)
        afterregister = db.execute("SELECT * FROM users WHERE username=:username", username=request.form.get("username"))
        session["user_id"] = afterregister[0]["id"]
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/planet", methods=["POST"])
def planet():
    
    if request.method == "POST":
        planet = lookup(request.form.get("planetname"))
        name = planet["englishName"]
        mass = planet["mass"]["massValue"]
        massExponent = planet["mass"]["massExponent"]
        vol = planet["vol"]["volValue"]
        volExponent = planet["vol"]["volExponent"]
        density = planet["density"]
        gravity = planet["gravity"]
        avgTemp = round(planet["avgTemp"] - 273.15, 1)
        if mass == 1.98900:
            vol = 1.4
            volExponent = 18
            density = 1.41
            gravity = 274
            avgTemp = 5505
        if planet["moons"] is None:
            moons = "None"
            all_moonsrel = []
            all_moonsnames = []
        else:
            moons = len(planet["moons"])
            all_moonsrel = []
            all_moonsnames = []
            for i in planet['moons']:
                all_moonsrel.append(i['rel'])
                all_moonsnames.append(i['moon'])
        if all_moonsnames == ['La Lune']:
                all_moonsnames = ["Luna"]
        marstemp = marsweather()
        if name == "Sun":
            img = "https://i.imgur.com/8sSunWe.png"
            planetclass = 'Sun'
            style = 'right: -250px; top: -150px; width: 1610px; height: 1265px;'
        elif name ==  "Venus":
            img = "https://i.imgur.com/AOL4xwu.png"
            planetclass = 'Venus'
            style = 'right: -150px; top: 100px; width: 1400px; height: 800px;'
        elif name ==  "Mercury":
            img = "https://i.imgur.com/7WxyM0B.png"
            planetclass = 'Mercury'
            style = 'right: 150px; top: 100px; width: 800px; height: 800px;'
        elif name ==  "Earth":
            img = "https://i.imgur.com/H6orFKh.png"
            planetclass = 'Earth'
            style = 'right: 150px; top: 100px; width: 800px; height: 800px;'
        elif name ==  "Mars":
            img = "https://i.imgur.com/QuxVvmB.png"
            planetclass = 'Mars'
            style = 'right: 150px; top: 100px; width: 850px; height: 850px;'
        elif name ==  "Jupiter":
            img = "https://i.imgur.com/dqtdYJC.png"
            planetclass = 'Jupiter'
            style = 'right: 150px; top: 100px; width: 800px; height: 800px;'
        elif name ==  "Saturn":
            img = "https://i.imgur.com/1bRKZwf.png"
            planetclass = 'Saturn'
            style = 'right: 125px; top: 75px; width: 900px; height: 900px;'
        elif name ==  "Uranus":
            img = "https://i.imgur.com/YB4Kil1.png"
            planetclass = 'Uranus'
            style = 'right: 150px; top: 100px; width: 800px; height: 800px;'
        elif name ==  "Neptune":
            img = "https://i.imgur.com/xGnAfVf.png"
            planetclass = 'Neptune'
            style = 'right: -200px; top: 100px; width: 1575px; height: 770px;'
        elif name ==  "Pluto":
            img = "https://i.imgur.com/b8hQMuU.png"
            planetclass = 'Pluto'
            style = 'right: 50px; top: 0px; width: 1000px; height: 1000px;'
        if len(all_moonsnames) == 2:
            return render_template("planetmars.html", all_moonsrel = all_moonsrel, all_moonsnames = all_moonsnames, img = img, planetclass = planetclass, style = style, mass = mass, massExponent = massExponent, vol = vol, volExponent = volExponent, density = density, gravity = gravity, avgTemp = avgTemp, moons = moons)
        else:
            return render_template("planet.html", marstemp = marstemp, all_moonsrel = all_moonsrel, all_moonsnames = all_moonsnames, img = img, planetclass = planetclass, style = style, mass = mass, massExponent = massExponent, vol = vol, volExponent = volExponent, density = density, gravity = gravity, avgTemp = avgTemp, moons = moons)

@app.route("/moon", methods=["POST"])
def moon():
    
    if request.method == "POST":
        planet = lookupmoon(request.form.get("moonname"))
        mass = planet["mass"]["massValue"]
        massExponent = planet["mass"]["massExponent"]
        semimajorAxis = planet["semimajorAxis"]
        meanRadius = planet["meanRadius"]
        sideralOrbit = round(planet["sideralOrbit"], 2)
        discoveredBy = planet["discoveredBy"]
        discoveryDate = planet["discoveryDate"]

        return render_template("moon.html", mass = mass, massExponent = massExponent, semimajorAxis = semimajorAxis, meanRadius = meanRadius, sideralOrbit = sideralOrbit, discoveredBy = discoveredBy, discoveryDate = discoveryDate)

@app.route("/photo", methods=["POST"])
def photo():
    
    if request.method == "POST":
        photo = rover(request.form.get("rover"), request.form.get("sol"))
        cameraname = request.form.get("camera")
        listofphotos = []
        for i in range(len(photo["all"])):
            if cameraname == photo["all"][i]["camera"]["name"]:
                listofphotos.append(photo["all"][i]["img_src"])
            else:
                continue

        return render_template("photo.html", apology = apology, listofphotos = listofphotos, photo = photo)

@app.route("/weather", methods=["POST"])
def weather():
    
    if request.method == "POST":
        marstemp = marsweather()
        avtemp = marstemp[0]["av"]
        mintemp = marstemp[0]["mn"]
        maxtemp = marstemp[0]["mx"]
        avhws = marstemp[1]["av"]
        minhws = marstemp[1]["mn"]
        maxhws = marstemp[1]["mx"]
        avpre = marstemp[2]["av"]
        minpre = marstemp[2]["mn"]
        maxpre = marstemp[2]["mx"]
        wd = marstemp[3]["most_common"]["compass_point"]
    return render_template("weather.html", marstemp = marstemp, avtemp = avtemp, mintemp = mintemp, maxtemp = maxtemp, avhws = avhws, minhws = minhws, maxhws = maxhws, avpre = avpre, minpre = minpre, maxpre = maxpre, wd = wd)

@app.route("/quizz", methods=["GET", "POST"])
@login_required
def quizz():
    
    if request.method == "POST":
        q1answer = request.form.get("q1")
        q2answer = request.form.get("q2")
        q3answer = request.form.get("q3")
        q4answer = request.form.get("q4")
        q5answer = request.form.get("q5")
        q6answer = request.form.get("q6")
        q7answer = request.form.get("q7")
        q8answer = request.form.get("q8")
        q9answer = request.form.get("q9")
        q10answer = request.form.get("q10")
        qbonusanswer = request.form.get("bonus")
        insert = db.execute("INSERT INTO answers ('id', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'bonus') VALUES (:id, :q1, :q2, :q3, :q4, :q5, :q6, :q7, :q8, :q9, :q10, :bonus)", id = session["user_id"], q1 = q1answer, q2 = q2answer, q3 = q9answer, q4 = q4answer, q5 = q5answer, q6 = q6answer, q7 = q7answer, q8 = q8answer, q9 = q9answer, q10 = q10answer, bonus = qbonusanswer)
        a = 0
        if request.form.get("q1") == "8":
            a = a + 1
        else:
            a = a
        if request.form.get("q2") == "Saturn":
            a = a + 1
        else:
            a = a
        if request.form.get("q3") == "14.9":
            a = a + 1
        else:
            a = a
        if request.form.get("q4") == "Phobos and Deimos":
            a = a + 1
        else:
            a = a
        if request.form.get("q5") == "Number of times Mars has completed a full rotation around its own axis since the rover landed":
            a = a + 1
        else:
            a = a
        if request.form.get("q6") == "No":
            a = a + 1
        else:
            a = a
        if request.form.get("q7") == "Mercury":
            a = a + 1
        else:
            a = a
        if request.form.get("q8") == "It is the hottest planet":
            a = a + 1
        else:
            a = a
        if request.form.get("q9") == "5":
            a = a + 1
        else:
            a = a
        if request.form.get("q10") == "InSight":
            a = a + 1
        else:
            a = a
        if request.form.get("bonus") == "1":
            a = a +1
        else:
            a = a +1

        return render_template("quizzresult.html", a = a, q1answer = q1answer, q2answer = q2answer, q3answer = q3answer, q4answer = q4answer, q5answer = q5answer, q6answer = q6answer, q7answer = q7answer, q8answer = q8answer, q9answer = q9answer, q10answer = q10answer, qbonusanswer = qbonusanswer,)
    else:
        return render_template("quizz.html")

@app.route("/about")
def about():
    return render_template("about.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
