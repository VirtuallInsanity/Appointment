import cs50
import csv
import os
import smtplib

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///list.db")

@app.route("/")
def get_index():
    return render_template("index.html")

@app.route("/appointment", methods=["GET","POST"])
def get_appointment():
    if request.method == "POST":

        new_patient = db.execute("INSERT INTO clients (name, last_name, age, date_of_birth, policy_number, doctor, email, apptdatetime) VALUES(:name, :lastname, :age, :dateofbirth, :policynumber, :doctor, :email, :apptdatetime)",
         name=request.form.get("name"), lastname = request.form.get("lastname"), age = request.form.get("age"), dateofbirth = request.form.get("dateofbirth"), policynumber = request.form.get("policynumber"), doctor = request.form.get("doctor"), email = request.form.get("email"), apptdatetime = request.form.get("apptdatetime"))

        if not new_patient:
            flash("Policy number must be unique and contains only numbers!")
            return redirect("/appointment")

        flash("You're appointed!")



        #email = request.form.get("email")
        #message = "You are registered!"
        #server = smtplib.SMTP("smtp.gmail.com", 587)
        #server.starttls()
        #server.login("jharvard@cs50.net", os.getenv("PASSWORD"))
        #server.sendmail("jharvard@cs50.net", email, message)

        return redirect("/list")
    else:
        return render_template("appointment.html")

@app.route("/list", methods=["GET"])
def get_list():
    table_rows = db.execute("SELECT * FROM clients ORDER BY created_at ASC")
    return render_template("list.html",table_rows=table_rows)

