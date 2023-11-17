from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    transactions = db.execute(
        "SELECT symbol, name, SUM(shares) AS shares, price FROM transactions WHERE user_id = (?) GROUP BY symbol "
        "HAVING SUM(shares) > 0;",
        user_id)
    cash = db.execute("SELECT cash FROM users WHERE id = (?);", user_id)

    total_cash = cash[0]["cash"]
    sum = int(total_cash)

    for row in transactions:
        look = lookup(row["symbol"])
        row["price"] = look["price"]
        row["total"] = row["price"] * row["shares"]
        sum += row["total"]

    return render_template("index.html", database=transactions, users=cash, sum=sum)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        buy = lookup(symbol)

        if not buy:
            return apology("Invalid Symbol")

        user_id = session["user_id"]
        name = buy["name"]
        price = buy["price"]
        shares = request.form.get("shares")

        if not shares.isdigit():
            return apology("You cannot purchase partial shares", 400)

        shares = int(shares)
        if shares <= 0:
            return apology("Share amount not allowed")

        cash_db = db.execute("SELECT cash FROM users where id = (?)", user_id)
        user_cash = (cash_db[0]["cash"])
        purchase = price * shares
        update_user_cash = user_cash - purchase

        if user_cash < purchase:
            return apology("Insufficient fund in your account", 400)

        db.execute("UPDATE users SET cash = (?) WHERE id = (?);", update_user_cash, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price) VALUES (?, ?, ?, ?, ?)",
                   user_id, symbol, name, shares, price)
        flash("Bought!")
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions = db.execute("SELECT symbol, name, shares, price, Timestamp FROM transactions WHERE user_id = (?);",
                              user_id)
    buy_sell = []
    for row in transactions:
        if row["shares"] <= 0:
            row["buy_sell"] = "SELL"

        else:
            row["buy_sell"] = "BUY"

    return render_template("history.html", database=transactions, buy_sell=buy_sell)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("username is required", 403)

        elif not password:
            return apology("password is required", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

        flash("logged in Successfully!")
        return redirect("/")

    elif request.method == "GET":
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
        symbol = request.form.get("symbol")
        quoted = lookup(symbol)

        if not quoted:
            return apology("Quote symbol doesn't exist", 400)

        return render_template("quoted.html", quoted=quoted)

    elif request.method == "GET":
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    username = request.form.get("username")
    password = request.form.get("password")
    password2 = request.form.get("confirmation")

    if request.method == "POST":
        if not username:
            return apology("username is required", 400)

        elif not password:
            return apology("password is required", 400)

        elif password != password2:
            return apology("passwords do not match!", 400)

        try:
            password_hash = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?);", username, password_hash)
        except:
            return apology("this username already exists, please try another username", 400)

        flash("Registered Successfully!")
        return redirect("/login")

    elif request.method == "GET":
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    if request.method == "GET":
        symbols = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = (?) GROUP BY symbol HAVING SUM(shares) > 0;",
            user_id)
        return render_template("sell.html", symbol=symbols)

    if request.method == "POST":
        symbol = request.form.get("symbol")
        sell = lookup(symbol)
        shares = int((request.form.get("shares")))
        name = sell["name"]
        price = sell["price"]

        if shares <= 0:
            return apology("Share amount not allowed", 400)

        if not symbol:
            return apology("Invalid Symbol", 400)

        cash_db = db.execute("SELECT cash FROM users WHERE id = (?);", user_id)
        user_cash = (int(cash_db[0]["cash"]))

        old_shares = db.execute("SELECT symbol, SUM(shares) AS shares FROM transactions WHERE symbol = (?);", symbol)
        no_old_shares = (int(old_shares[0]["shares"]))

        sold = price * shares
        update_user_cash = user_cash + sold

        if shares > no_old_shares:
            return apology("Insufficient share units in your account", 400)

        db.execute("UPDATE users SET cash = (?) WHERE id = (?);", update_user_cash, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price) VALUES (?, ?, ?, ?, ?)",
                   user_id, symbol, name, shares * (-1), price)

        flash("Sold!")
        return redirect("/")
