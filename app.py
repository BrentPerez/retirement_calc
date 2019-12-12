import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd, compound

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


@app.route("/")
@login_required
def index():
    """Show portfolio of current retirement stats"""
    return render_template("portfolio.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology(400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

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


@app.route("/edit", methods=["GET", "POST"])
def edit():
    """Edit user stats"""
    if request.method == "POST":
        # Import variables entered by user
        savings = int(request.form.get("savings"))
        salary = int(request.form.get("salary"))
        savingRate = float(request.form.get("savingRate"))
        age = int(request.form.get("age"))
        yieldAnnual = float(request.form.get("yieldAnnual"))
        payIncrease = float(request.form.get("payIncrease"))
        retirementAge = int(request.form.get("retirementAge"))
        expense = float(request.form.get("expense"))

        # Set up variables for growth calculation
        yearsSaving = (retirementAge - age)
        contribution = (savingRate / 100) * salary
        initialReturn = compound(savings, yieldAnnual, yearsSaving)
        totalBalance = initialReturn
        empty = 0

        # Set up arrays for graph
        ageByYear = []
        moneyByYear = []
        ageByYear.append(age)
        moneyByYear.append(savings)

        # Compounding interest while saving
        for year in range(yearsSaving):
            contribution = contribution * ((payIncrease / 100) + 1)
            totalBalance = compound(totalBalance, yieldAnnual, 1) + compound(contribution, yieldAnnual, 1)
            # Insert into array for graph
            myAge = age + year + 1
            ageByYear.append(myAge)
            moneyByYear.append(totalBalance)
        peak = totalBalance

        # Interest in retirement
        for x in range(120):
            if totalBalance > 0:
                if myAge > 120:
                    break
                else:
                    totalBalance = compound((totalBalance - expense), yieldAnnual, 1)
                    myAge = myAge + 1
                    ageByYear.append(myAge)
                    moneyByYear.append(totalBalance)

            # Years supported by retirement
            else:
                empty = myAge
                break

        principle = savings + (yearsSaving * (salary * (savingRate / 100)))
        interest = totalBalance - principle
        '''
        if empty > 0:
            print("Peak savings = " + str(usd(peak)))
            print("Retirment will run out at age " + str(empty))
        else:
            print("Retirement will last indefinitely with set expense")
            print("You will have " + str(usd(totalBalance)) + " at age 120")

        plt.plot(ageByYear, moneyByYear)
        plt.ylabel('Cash')
        plt.xlabel('Age')
        plt.show()
        '''

        return render_template("stats.html", totalBalance=usd(totalBalance), empty=empty, principle=usd(principle), interest=usd(interest), savings=savings, salary=salary, savingRate=savingRate, age=age, yieldAnnual=yieldAnnual, retirementAge=retirementAge, expense=expense)
    else:
        return render_template("portfolio.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Missing username!", 400)
        elif not request.form.get("password"):
            return apology("Missing password!", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords did not match", 400)
        else:
            username = request.form.get("username")
            hashpass = generate_password_hash(request.form.get("password"))

            insertUser = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hashpass)",
                                    username=username, hashpass=hashpass)
            if not insertUser:
                return apology("Sorry, Username already taken", 400)

        # Login user after register
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        session["user_id"] = rows[0]["id"]
        # Return to homepage
        return redirect("/", 200)

    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run(debug=True)