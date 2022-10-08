import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    cash = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])
    portfoliosymbols = db.execute("SELECT shares, symbol FROM portfolio WHERE id = :id", id=session["user_id"])
    for portfoliosymbol in portfoliosymbols:
        symbol = portfoliosymbol["symbol"]
        shares = portfoliosymbol["shares"]
        stock = lookup(symbol)
        total = shares * stock["price"]
        db.execute("UPDATE portfolio SET price = :price, total = :total WHERE id=:id AND symbol=:symbol", price=usd(stock["price"]), total=total, id=session["user_id"], symbol=symbol)
    portfolio = db.execute("SELECT * FROM portfolio WHERE id = :id", id = session["user_id"])
    totalsum = db.execute("SELECT SUM(total) FROM portfolio WHERE id = :id", id = session["user_id"])[0]["SUM(total)"]
    if totalsum is None:
        totalcash = cash[0]["cash"]
    else:
        totalcash = totalsum + cash[0]["cash"]
    return render_template("index.html", totalcash = usd(totalcash), stocks = portfolio, cash = usd(cash[0]["cash"]))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Must provide symbol", 403)
        if lookup(request.form.get("symbol")) == None:
            return apology("Must provide valid symbol", 400)
        if not request.form.get("shares"):
            return apology("Must provide number of shares", 403)
        shares = request.form.get("shares")
        if not shares.isdigit():
            return apology("You cannot purchase partial shares", 400)
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])
        totalprice = lookup(request.form.get("symbol"))["price"] * float(request.form.get("shares"))
        cashbalance = float(cash[0]["cash"])
        checkportfolio = db.execute("Select * FROM portfolio WHERE symbol = :symbol AND id = :id", symbol = request.form.get("symbol"), id = session["user_id"])
        if cashbalance >= totalprice:
            buy = db.execute("INSERT INTO transactions ('symbol', 'shares', 'price', 'id', 'type', 'name', 'total') VALUES (:symbol, :shares, :price, :id, 'buy', :name, :total)", symbol = request.form.get("symbol"), shares = request.form.get("shares"), price = lookup(request.form.get("symbol"))["price"], id = session["user_id"], name = lookup(request.form.get("symbol"))["name"], total = float(request.form.get("shares")) * lookup(request.form.get("symbol"))["price"])
            updatebalance = db.execute("UPDATE users SET cash = :newcashbalance WHERE id = :id", newcashbalance = cashbalance - totalprice, id = session["user_id"])
            if len(checkportfolio) == 0:
                insert = db.execute ("INSERT INTO portfolio ('symbol', 'name', 'shares', 'price', 'total', 'id') VALUES (:symbol, :name, :shares, :price, :total, :id)", symbol = request.form.get("symbol"), name = lookup(request.form.get("symbol"))["name"], shares = request.form.get("shares"), price = usd(lookup(request.form.get("symbol"))["price"]), total = float(request.form.get("shares")) * lookup(request.form.get("symbol"))["price"], id = session["user_id"])
            else:
                selectshares = db.execute ("SELECT SUM(shares) FROM portfolio WHERE symbol = :symbol AND id = :id", symbol = request.form.get("symbol"), id = session["user_id"])
                selecttotal = db.execute ("SELECT SUM(total) FROM portfolio WHERE symbol = :symbol AND id = :id", symbol = request.form.get("symbol"), id = session["user_id"])
                update = db.execute ("UPDATE portfolio SET shares = :shares, total = :total  WHERE symbol = :symbol AND id = :id", shares = int(selectshares[0]["SUM(shares)"]) + int(request.form.get("shares")), total = float(selecttotal[0]["SUM(total)"]) + int(request.form.get("shares")) * lookup(request.form.get("symbol"))["price"], symbol = request.form.get("symbol"), id = session["user_id"])
        else:
            return apology("You do not have enough cash", 403)

        return redirect("/")
    else:
        return render_template("buy.html")
@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    histories = db.execute("SELECT symbol, name, shares, price, Abs(total) AS absnum FROM transactions WHERE id = :id", id = session["user_id"])
    return render_template("history.html", histories = histories)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

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
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if quote == None:
            return apology("Symbol does not exist", 400)
        return render_template("quoteresult.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Must provide symbol", 400)
        if lookup(request.form.get("symbol")) == None:
            return apology("Must provide valid symbol", 400)
        if not request.form.get("shares"):
            return apology("Must provide number of shares", 400)
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])
        totalprice = lookup(request.form.get("symbol"))["price"] * float(request.form.get("shares"))
        cashbalance = float(cash[0]["cash"])
        ownedshares = db.execute("SELECT SUM(shares) FROM transactions WHERE id = :id AND symbol = :symbol", id = session["user_id"], symbol = request.form.get("symbol"))
        if ownedshares[0]["SUM(shares)"] >= int(request.form.get("shares")):
            sell = db.execute("INSERT INTO transactions ('symbol', 'shares', 'price', 'id', 'type', 'name', 'total') VALUES (:symbol, :shares, :price, :id, 'sell', :name, :total)", symbol = request.form.get("symbol"), shares = -1 * int(request.form.get("shares")), price = lookup(request.form.get("symbol"))["price"], id = session["user_id"], name = lookup(request.form.get("symbol"))["name"], total = -1 * float(request.form.get("shares")) * lookup(request.form.get("symbol"))["price"])
            updatebalance = db.execute("UPDATE users SET cash = :newcashbalance WHERE id = :id", newcashbalance = cashbalance + totalprice, id = session["user_id"])
            selectshares = db.execute ("SELECT SUM(shares) FROM portfolio WHERE symbol = :symbol AND id = :id", symbol = request.form.get("symbol"), id = session["user_id"])
            selecttotal = db.execute ("SELECT SUM(total) FROM portfolio WHERE symbol = :symbol AND id = :id", symbol = request.form.get("symbol"), id = session["user_id"])
            update = db.execute ("UPDATE portfolio SET shares = :shares, total = :total  WHERE symbol = :symbol AND id = :id", shares = int(selectshares[0]["SUM(shares)"]) - int(request.form.get("shares")), total = (int(selectshares[0]["SUM(shares)"]) - int(request.form.get("shares"))) * lookup(request.form.get("symbol"))["price"], symbol = request.form.get("symbol"), id = session["user_id"])
            selectagain = db.execute("SELECT SUM(shares) FROM portfolio WHERE symbol = :symbol AND id = :id", symbol = request.form.get("symbol"), id = session["user_id"])
            if int(selectagain[0]["SUM(shares)"]) == 0:
                delete = db.execute("DELETE FROM portfolio WHERE symbol = :symbol AND id = :id", symbol = request.form.get("symbol"), id = session["user_id"])
                return redirect("/")
            else:
                return redirect("/")
        else:
            return apology("You do not have enough shares", 400)
    else:
        selectshares = db.execute ("SELECT symbol FROM portfolio WHERE id = :id", id = session["user_id"])
        return render_template("sell.html", selectshares = selectshares)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
