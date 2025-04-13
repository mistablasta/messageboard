import sqlite3
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import user
import message

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
        user.create_user(username, password_hash)
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

    password_hash = user.get_user_password_hash(username)
    if password_hash and check_password_hash(password_hash, password):
        user_id = db.query("SELECT id FROM users WHERE username = ?", [username])[0][0]
        session["username"] = username
        session["user_id"] = user_id
        return redirect("/")
    else:
        return "Wrong username or password."

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/messages", methods=["GET", "POST"])
def messages():
    if request.method == "POST":
        if "user_id" not in session:
            return redirect("/login")

        content = request.form["content"]
        message.insert_message(session["user_id"], content)
        return redirect("/messages")

    messages_list = message.get_all_messages()
    return render_template("messages.html", messages=messages_list)

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    messages_list = message.search_messages(query)
    return render_template("messages.html", messages=messages_list)

@app.route("/edit/<int:message_id>", methods=["GET", "POST"])
def edit(message_id):
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    if request.method == "POST":
        content = request.form["content"]
        message.update_message(message_id, user_id, content)
        return redirect("/messages")

    msg = message.get_message_by_id_and_user(message_id, user_id)
    if not msg:
        return "Message not found or you don't have permission to edit this message."

    return render_template("edit.html", message=msg[0])

@app.route("/delete/<int:message_id>", methods=["POST"])
def delete(message_id):
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    message.delete_message(message_id, user_id)
    return redirect("/messages")

@app.route("/reaction/<int:message_id>/<reaction_type>", methods=["POST"])
def add_reaction_route(message_id, reaction_type):
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    if reaction_type not in ['thumbs_up', 'thumbs_down']:
        return "Invalid reaction type.", 400

    message.add_reaction(message_id, user_id, reaction_type)
    return redirect("/messages")