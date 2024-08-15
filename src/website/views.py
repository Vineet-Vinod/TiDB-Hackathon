from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from flask_login import login_required, current_user
from .scripts import preferenceTuningPosters
import time

views = Blueprint("views", __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route("/welcome")
def welcome():
        return render_template("welcome.html")

@views.route("/tune-preferences", methods=["GET", "POST"])
def tune_preferences():
    # implement a more sophisticated means of choosing movies
    poster_urls = preferenceTuningPosters()

    if "tuning_idx" not in session:
        session["tuning_idx"] = 0
    if session["tuning_idx"] == len(poster_urls):
        session["tuning_idx"] = 0

    if request.method == "POST":
        response = request.form.get("response")

        # logic to handle response
        if response == "yes":
            pass
        elif response == "no":
            pass

        session['tuning_idx'] += 1
    
    idx = session["tuning_idx"]
    if idx < len(poster_urls):
        poster_url = poster_urls[idx]
        if request.method == "POST":
            time.sleep(0.2)
        return render_template("swipe.html", poster_url=poster_url)
    else:
        return redirect(url_for("views.home"))