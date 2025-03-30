import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "Passwords do not match."
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "Username already taken."

    return "Account created."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    sql = "SELECT password_hash FROM users WHERE username = ?"
    password_hash = db.query(sql, [username])[0][0]

    if check_password_hash(password_hash, password):
        session["username"] = username
        return redirect("/")
    else:
        return "Wrong username or password."

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/messages", methods=["GET", "POST"])
def messages():
    if request.method == "POST":
        if "username" not in session:
            return redirect("/login")
    
        content = request.form["content"]
        username = session["username"]
        sql = "INSERT INTO messages (username, content) VALUES (?, ?)"
        db.execute(sql, [username, content])
        return redirect("/messages")

    sql = "SELECT id, username, content, timestamp FROM messages ORDER BY timestamp DESC"
    messages = db.query(sql)
    return render_template("messages.html", messages=messages)

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    sql = "SELECT username, content, timestamp FROM messages WHERE content LIKE ? ORDER BY timestamp DESC"
    messages = db.query(sql, ['%' + query + '%'])
    return render_template("messages.html", messages=messages)

@app.route("/edit/<int:message_id>", methods=["GET", "POST"])
def edit(message_id):
    if "username" not in session:
        return redirect("/login")

    if request.method == "POST":
        content = request.form["content"]
        sql = "UPDATE messages SET content = ? WHERE id = ? AND username = ?"
        db.execute(sql, [content, message_id, session["username"]])
        return redirect("/messages")

    sql = "SELECT id, content FROM messages WHERE id = ? AND username = ?"
    message = db.query(sql, [message_id, session["username"]])
    if not message:
        return "Message not found or you don't have permission to edit this message."

    return render_template("edit.html", message=message[0])

@app.route("/delete/<int:message_id>", methods=["POST"])
def delete(message_id):
    if "username" not in session:
        return redirect("/login")

    sql = "DELETE FROM messages WHERE id = ? AND username = ?"
    db.execute(sql, [message_id, session["username"]])
    return redirect("/messages")