from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from email_validator import validate_email, EmailNotValidError
import re
from .config import USE_TIDB

# Conditionally import and initialize the database if USE_TIDB is True
# Used for debugging
if USE_TIDB:
    from .db_interface import Database     
    db = Database()

# Used for user authentication (login, logout, new account)
auth = Blueprint("auth", __name__)

# Responsible for validating login information and returning the correct page
@auth.route("/login", methods=["GET", "POST"])
def login():
    # Used for debugging, always false for production
    if not USE_TIDB and request.method == "POST":
        session["loggedin"] = True
        flash("Logged in successfully!", category="success")
        return redirect(url_for("views.home"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Current password
        # Will implement a hashing algorithm
        pw = db.get_user_data(email)

        if pw:
            if pw == password:
                # correct email and password, login
                session["email"] = email
                session["loggedin"] = True
                flash("Logged in successfully!", category="success")
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Email does not exist.", category="error")

    # return to the login page if anything fails
    return render_template("login.html")

# Responsible for validating sign-up information and rendering the correct page
@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    # Used for debugging, always false for production
    if not USE_TIDB and request.method == "POST":
        flash("Account created!", category="success")
        return redirect(url_for("views.welcome"))
    
    if request.method == "POST":
        # Fetch form responses
        email = request.form.get("email")
        password = request.form.get("password")
        password_confirm = request.form.get("confirm")

        # Valid == True by default
        valid_email = True
        password_error = password_authenticator(password)

        # Validate email
        try:
            email_info = validate_email(email, check_deliverability=False)
            email = email_info.normalized
        except EmailNotValidError as e:
            valid_email = False
        
        # if all is valid, return to welcome page
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
            session["loggedin"] = True
            return redirect(url_for("views.welcome"))

    return render_template("signup.html")

@auth.route("/logout")
def logout():
    # Clear session and return to login page
    session.clear()
    return redirect(url_for("auth.login"))

# DECOMMISSIONED
'''
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
            db.update_password(session["email"], new_password)
            flash("Password reset successfully!", category="success")
            return redirect(url_for("auth.login"))

    return render_template("reset-password.html")
'''
    
# May want to consider moving this to "crypto.py"
def password_authenticator(password: str):
    #return 0 # Used for debugging - be sure to comment out for prod
    if len(password) < 8: return "too short"
    if not re.search(r"[a-z]", password): return "missing a lowercase letter"
    if not re.search(r"[A-Z]", password): return "missing an uppercase letter"
    if not re.search(r"\d", password): return "missing a number"
    return 0
