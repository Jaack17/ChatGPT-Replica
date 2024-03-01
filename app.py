import os
import sqlite3
from flask import Flask, request, jsonify, render_template, redirect, session, g, make_response, flash
from flask_session import Session
from openai import OpenAI
from werkzeug.security import check_password_hash, generate_password_hash
from utility import login_required

os.environ["OPENAI_API_KEY"]

# Set up Flask app
app = Flask(__name__)
app.static_folder = "static"

# Set up Flask session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to SQLite database
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect("project.db")
    return db

@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

openai_client = OpenAI()

# Bot response
def generate_bot_response(user_input):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.8,
        max_tokens=400,
        messages=[{"role": "user", "content": user_input}]
    )
    return response.choices[0].message.content

# Route to render the homepage
@app.route("/")
def index():
    if "id" in session:
        logged_in = True
    else:
        logged_in = False
    return render_template("index.html", logged_in=logged_in)

# Route to render the chat page
@app.route("/chat")
@login_required
def chat():
    response = make_response(render_template("chat.html"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Route for receiving user messages
@app.route("/message", methods=["POST"])
@login_required
def message():
    user_input = request.json["message"]
    
    bot_response = generate_bot_response(user_input)
    
    return jsonify({"message": bot_response})

# Route for handling user login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Query the database to check if the user exists
        cursor = g.db.cursor()
        cursor.execute("SELECT * FROM registrations WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            session["id"] = user[0]
            session["logged_in"] = True
            return redirect("/chat")
        else:
            flash("Invalid username or password", "error")

    return render_template("login.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    """Log user out"""

    # Forget any id and logged_in session variables
    session.pop("id", None)
    session.pop("logged_in", None)

    return redirect("/")

@app.route("/change_password", methods=["POST"])
@login_required
def change_password():
    
    session.clear()
    
    return redirect("/login")

# Route for handling user registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if the username already exists in the registrations table
        cursor = g.db.cursor()
        cursor.execute("SELECT * FROM registrations WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Username already exists", "error")
        else:
            # Hash the password before storing it in the database
            hashed_password = generate_password_hash(password)

            # Insert the new user into the registrations table
            cursor.execute("INSERT INTO registrations (username, password) VALUES (?, ?)", (username, hashed_password))
            g.db.commit()

            # Set flash message for successful registration
            flash("Registration successful! You can now log in.", "success")

            return redirect("/login")

    return render_template("register.html")



@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        user_id = session.get("id")

        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")

        cursor = g.db.cursor()
        cursor.execute("SELECT password FROM registrations WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        if user and check_password_hash(user[0], current_password):
            hashed_new_password = generate_password_hash(new_password)

            cursor.execute("UPDATE registrations SET password = ? WHERE id = ?", (hashed_new_password, user_id))
            g.db.commit()

            session.clear()

            flash("Password successfully changed!", "success")

            return redirect("/login")
        else:
            flash("Current password is incorrect", "error")

    return render_template("profile.html")


if __name__ == "__main__":
    app.run(debug=True)

