#Project title: Contextual Prompting
#Name: Patrick Karlsen
#City: Aalborg
#Country: Denmark

from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from helpers import login_required
import os
from llama_index import VectorStoreIndex, SimpleDirectoryReader

app = Flask(__name__)

os.environ["OPENAI_API_KEY"] = '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'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///FinalProject.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        if not os.path.exists(("./data/" + str(session["user_id"]))):
            os.makedirs(("./data/" + str(session["user_id"])))

        files = request.files["file"]
        if files:
            filename = secure_filename(files.filename)
            files.save(os.path.join(("./data/" + str(session["user_id"])), filename))
            return redirect("/chat")
        return render_template("error.html", message="Error during file upload")
    
    else:     
        return render_template("index.html")


@app.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    if request.method == "POST":
        question = request.form.get("question")
        db.execute("INSERT INTO paragraphs (user_id, paragraph, type, time) VALUES(?, ?, ?, time())", session["user_id"], question, "question")
        
        documents = SimpleDirectoryReader(('./data/' + str(session["user_id"]))).load_data()
        index = VectorStoreIndex.from_documents(documents)
        query_engine = index.as_query_engine()
        response = query_engine.query(question)
        
        db.execute("INSERT INTO paragraphs (user_id, paragraph, type, time) VALUES(?, ?, ?, time())", session["user_id"], str(response), "answer")
        paragraphs = db.execute("SELECT * FROM paragraphs WHERE user_id = ? ORDER BY time", session["user_id"])
        return render_template("chat.html", paragraphs=paragraphs)
    else:
        return render_template("chat.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return render_template("error.html", message="Must enter username")

        elif not request.form.get("password"):
            return render_template("error.html", message="Must enter password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("error.html", message="Invalid username/password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users = db.execute("SELECT username FROM users")
        if not request.form.get("username"):
            return render_template("error.html", message="must enter username")
        elif request.form.get("username") in users:
            return render_template("error.html", message="username already take")
        elif request.form.get("password") != request.form.get("confirmation"):
            return render_template("error.html", message="passwords do not match")
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return render_template("error.html", message="must provide password")
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")))
        return redirect("/login")
    else:
       return render_template("register.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")