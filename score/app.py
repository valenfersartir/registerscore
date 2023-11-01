from flask import Flask, render_template, request, redirect
from cs50 import SQL
import os
from flask import Flask, flash, redirect, render_template, request, session #import tools untuk website
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.update(SECRET_KEY=os.urandom(24))
db = SQL("sqlite:///score.db")
# udb = SQL("sqlite:///user.db")
@app.route("/", methods=["GET", "POST"])
def index():
        if request.method == "POST": 
            name = request.form.get("name")
            score = request.form.get("score")

            db.execute("INSERT INTO score (name, score) VALUES(?, ?)", name, score)

            return redirect("/")
        else:

            students = db.execute("SELECT * FROM score")
            return render_template("index.html", students=students)
            
@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_data(id):
    if request.method == "GET":
        score = db.execute("SELECT * FROM score WHERE id = ?", id)[0]
        print(score)
        return render_template("edit.html", score=score)
    elif request.method == "POST":
        score_name = request.form.get("name")
        score_score = request.form.get("score")
        db.execute('UPDATE score set name = ?, score = ? where id = ?', score_name, score_score, id)
        return redirect("/") 
               
@app.route("/delete/<id>", methods=["GET"])
def delete_id(id):
    db.execute("delete from score where id = ?", id)
    return redirect("/")    

@app.route("/register", methods=["GET", "POST"])
def register_data():
     
     """Register user"""
     # access from data (sesuaikan dengan form register masing-masing)
     if request.method == "POST":
          if not request.form.get("username"):
               return "must provide username"
          elif not request.form.get("password"):
               return "must provide password"
          # baca data username yang sudah terdaftar
          rows = db.execute("SELECT * FROM user WHERE username = ?", request.form.get("username"))
          # baca data isian member baru dari form
          username = request.form.get("username")
          password = request.form.get("password")
          email = request.form.get("email")
          password_repeat = request.form.get("password_repeat")
          # enkripsi password
          hash = generate_password_hash(password)
          if len(rows) == 1: # jika ditemukan username yang sama 
               return "username already taken"
          if password == password_repeat : # jika password = ulang password 
               # masukkan data member baru
               db.execute("INSERT INTO user (username, password, email, password_repeat) VALUES(?, ?, ?, ?)", username, hash, email, password_repeat)

               # ambil data user baru dan simpan pada session
               register_user = db.execute("select * from user where username = ?", username)
               print(register_user)
               session["id"] = register_user[0]["id"]
               flash('You were successfully registered') # notifikasi
               return redirect("/")
          else:

            return render_template("register.html")
        
     else:
         return render_template("register.html")
        
@app.route("/login", methods=["GET", "POST"])

def login():

    """Log user in"""

    session.clear()


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted 
        if not request.form.get("username"): 
            return "must provide username"

        # Ensure password was submitted 
        elif not request.form.get("password"):
            return "must provide password"

        # Query database for username 
        rows= db.execute("SELECT * FROM user WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct 
        if len(rows) != 1 or not check_password_hash (rows[0]["hash"], request.form.get("password")): 
            return "invalid username and/or password" 
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