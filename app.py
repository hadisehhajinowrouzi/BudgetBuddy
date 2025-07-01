
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from helper import usd
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        amount = request.form.get("amount")
        date = request.form.get("date")
        category = request.form.get("category")

        if name is None:
            flash("fill out the name!")
            return redirect("/")
        if amount is None:
            flash("fill out the amount!")
            return redirect("/")
        if date is None:
            flash("fill out the date!")
            return redirect("/")
        if category is None:
            flash("fill out the category!")
            return redirect("/")

        existing_category = db.execute(
            "SELECT id FROM Categories WHERE category_name = ?", category)
        category_id = existing_category[0]["id"]

        db.execute("INSERT INTO expenses(name , amount , date ,category_id) VALUES(? ,? ,? ,? )",
                   name, amount, date, category_id)

        flash("Expense added successfully!")
        return redirect("/expense")

    else:
        categories = db.execute("SELECT * FROM Categories")
        return render_template("index.html", categories=categories)


@app.route("/expense", methods=["GET"])
def expense():

    expenses = db.execute(
        " SELECT expenses.name, expenses.amount, expenses.date, Categories.category_name FROM expenses JOIN Categories ON expenses.category_id = Categories.id")
    total_money = 0
    for each in expenses:
        total_money += float(each["amount"])

    return render_template("expense.html", expenses=expenses, total_money=usd(total_money))


@app.route("/category", methods=["GET", "POST"])
def category():
    if request.method == "GET":
        return render_template("category.html")
    else:

        new_category = request.form.get("makecategory")
        if new_category is None:
            flash("make a category")
            return redirect("/category")

        exsist_category = db.execute(
            "SELECT * FROM categories WHERE category_name = ?", new_category)

        if exsist_category:
            flash(f"the category {new_category.upper()} already exsits . make a new one")
            return redirect("/category")

        db.execute("INSERT INTO Categories(category_name) VALUES(?)", new_category)
        flash(f"category: {new_category.upper()} added successfully!")

        return redirect("/")
