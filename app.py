import os
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "flask"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

mysql = MySQL(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return render_template("No Username Given")
        if not password:
            return render_template("No Password Given")
        if not confirmation:
            return render_template("Passwords do not Match")

        if password != confirmation:
            return render_template("Password and confirmation do not match")

        cur = mysql.connection.cursor()
        hash = generate_password_hash(password)
        cur.execute("INSERT INTO user (username, hash) VALUES (%s, %s)", (username, hash))
        mysql.connection.commit()

        session["user_id"] = cur.lastrowid

        cur.close()

        return redirect("/")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return render_template("apology.html", message="Make sure to enter a username"), 403
        elif not password:
            return render_template("apology.html", message="Make sure to enter a password"), 403

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE username = %s", (username,))
        rows = cur.fetchall()

        if len(rows) != 1 or not check_password_hash(rows[0][2], password):
             return render_template("apology.html", message="Invalid username and/or password"), 403

        session["user_id"] = rows[0][0]
        cur.close()


        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/notes")
@login_required
def notes():
    user_id = session["user_id"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM note WHERE user_id = %s", (user_id,))
    notes = cur.fetchall()
    cur.close()
    return render_template("stuff.html", notes=notes)

@app.route("/notes/add-note", methods=["GET", "POST"])
@login_required
def add_note():
    
    if request.method == "GET":
        return render_template("add.html")
    else:
        new_note = request.form.get("new_note")
        
        user_id = session["user_id"]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO note (notes, user_id) VALUES (%s, %s)", (new_note, user_id))

        mysql.connection.commit()
        cur.close()
        flash("Added note!")
        return redirect("/notes")

@app.route("/notes/delete-note", methods=["POST"])
def delete_note():
    note_id = request.form.get("note-id")
    if note_id:
        cur = mysql.connection.cursor()
        cur.execute("DELETE from note WHERE id = %s", (note_id,))
        mysql.connection.commit()
        cur.close()
    return redirect("/notes")

@app.route("/contact", methods=["GET", "POST"])
@login_required
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        with open("messages.txt", "a") as messageFile:
            messageFile.write(f"Message by {name}\n")
            messageFile.write(f"User email: {email}\n")
            messageFile.write(f"User message: {message}\n")
            messageFile.write("\n")

        flash("Your message has been sent!")
        return redirect("/contact")

    else:
        return render_template("contact.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run()
