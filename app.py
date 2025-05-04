import sqlite3
from flask import Flask, redirect, url_for, render_template, abort, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
from sql import message, profiles, user
import secrets

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/register")
def register():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    check_csrf()
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

    return redirect(url_for("index", message="Account created successfully!"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    check_csrf()
    username = request.form["username"]
    password = request.form["password"]

    password_hash = user.get_user_password_hash(username)
    if password_hash and check_password_hash(password_hash, password):
        user_id = user.get_user_id_by_username(username)
        session["username"] = username
        session["user_id"] = user_id
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")
    else:
        return "Wrong username or password."

@app.route("/logout", methods=["POST"])
def logout():
    check_csrf()
    session.clear()
    return redirect("/")

@app.route("/messages", methods=["GET", "POST"])
def messages():
    if request.method == "POST":
        if "user_id" not in session:
            return redirect("/login")
        check_csrf()

        content = request.form["content"]
        selected_categories = [int(c) for c in request.form.getlist("categories")]
        message.insert_message(session["user_id"], content, selected_categories)
        return redirect("/messages")

    page = request.args.get("page", default=1, type=int)
    per_page = 50
    offset = (page - 1) * per_page

    messages_list = message.get_all_messages(limit=per_page+1, offset=offset)
    has_more = len(messages_list) > per_page
    if has_more:
        messages_list = messages_list[:per_page]
    categories = message.get_all_categories()
    return render_template("messages.html", messages=messages_list, categories=categories, page=page, has_more=has_more)

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    messages_list = message.search_messages(query)
    return render_template("messages.html", messages=messages_list)

@app.route("/edit/<int:message_id>", methods=["GET", "POST"])
def edit(message_id):
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        check_csrf()

    user_id = session["user_id"]

    if request.method == "POST":
        content = request.form["content"]
        message.update_message(message_id, user_id, content)
        return redirect("/messages")

    msg = message.get_message_by_id_and_user(message_id, user_id)
    if not msg:
        return "Message not found or you don't have permission to edit this message."

    return render_template("edit.html", message=msg[0])

@app.route("/delete/<int:message_id>", methods=["GET", "POST"])
def delete(message_id):
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        check_csrf()

    user_id = session["user_id"]

    if request.method == "POST":
        message.delete_message(message_id, user_id)
        return redirect("/messages")
    
    return render_template("delete.html", message_id=message_id)

@app.route("/reaction/<int:message_id>/<reaction_type>", methods=["POST"])
def add_reaction_route(message_id, reaction_type):
    if "user_id" not in session:
        return redirect("/login")

    check_csrf()

    user_id = session["user_id"]

    if reaction_type not in ["thumbs_up", "thumbs_down"]:
        return "Invalid reaction type.", 400

    message.add_reaction(message_id, user_id, reaction_type)
    return redirect("/messages")

@app.route("/profile/<username>")
def profile(username):
    user_id = user.get_user_id(username)
    if not user_id:
        return "User not found", 404

    total_score = profiles.get_total_score(user_id)
    message_count = profiles.get_message_count(user_id)
    favorite_category = profiles.get_favorite_category(user_id)
    user_messages = message.get_messages_by_user(user_id)

    return render_template("profile.html",
                           username=username,
                           total_score=total_score,
                           message_count=message_count,
                           favorite_category=favorite_category,
                           messages=user_messages)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)