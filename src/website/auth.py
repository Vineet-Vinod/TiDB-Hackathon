from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from email_validator import validate_email, EmailNotValidError
import re
from flask_login import login_user, login_required, logout_user, current_user
from .db_interface import Database     

db = Database()

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        pw = db.get_user_data(email)

        if pw:
            if pw == password:
                session["email"] = email
                flash("Logged in successfully!", category="success")
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Email does not exist.", category="error")

    return render_template("login.html")

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")
        password_confirm = request.form.get("confirm")

        valid_email = True
        password_error = password_authenticator(password)

        try:
            email_info = validate_email(email, check_deliverability=False)
            email = email_info.normalized
        except EmailNotValidError as e:
            valid_email = False
        
        user = db.get_user_data(email)
        if user:
            flash("Email already exists, try logging in instead.", category="error")
        elif not valid_email:
            flash("Please enter a valid email.", category="invalid-input")
        elif password_error != 0:
            flash(f"Password is {password_error}.", category="invalid-input")
        elif password != password_confirm:
            flash("Passwords do not match.", category="invalid-input")
        else:
            flash("Account created!", category="success")
            session["email"] = email
            session["password"] = password
            return redirect(url_for("views.welcome"))

    return render_template("signup.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        email = request.form.get("email")
        new_password = request.form.get("password")
        password_confirm = request.form.get("confirm")
        valid_email = True
        password_error = password_authenticator(new_password)

        user = db.get_user_data(email)

        if not user:
            flash("Email does not exist.", category="error")
        elif not valid_email:
            flash("Please enter a valid email.", category="invalid-input")
        elif password_error != 0:
            flash(f"Password is {password_error}.", category="invalid-input")
        elif new_password != password_confirm:
            flash("Passwords do not match.", category="invalid-input")
        else:
            flash("Password reset successfully!", category="success")
            return redirect(url_for("auth.login"))

    return render_template("reset-password.html")

def password_authenticator(password: str):
    #return 0 # Used for debugging - be sure to comment out for prod
    if len(password) < 8: return "too short"
    if not re.search(r"[a-z]", password): return "missing a lowercase letter"
    if not re.search(r"[A-Z]", password): return "missing an uppercase letter"
    if not re.search(r"\d", password): return "missing a number"
    return 0
