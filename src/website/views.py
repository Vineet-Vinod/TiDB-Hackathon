from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from flask_login import login_required, current_user
from .scripts import preferenceTuningPosters
import time
from .db_interface import Database     

db = Database().get_db()

views = Blueprint("views", __name__)

@views.route('/')
def home(): # Add a filters option to select genre and languages
    return render_template("home.html")

@views.route("/welcome")
def welcome():
    return render_template("welcome.html")

@views.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

@views.route("/get-language", methods=["GET", "POST"])
def get_language():
    if request.method == "POST":
        languages = ','.join(request.form.getlist("languages"))
        genres = ','.join(request.form.getlist("genres"))

        userdata = (session["name"], session["password"], genres, languages)

        movies = []
        movie_ids = [15398776, 120338, 110357, 68646, 107290, 1745960, 111161, 468569]
        for mov, res in zip(movie_ids, session["responses"]):
            if res == "yes":
                movies.append(mov)

        db.add_user_data(userdata, tuple(movies))

        return redirect(url_for("views.thankyou"))

    return render_template("preferences.html")


@views.route("/tune-preferences", methods=["GET", "POST"])
def tune_preferences(): # They should get this page only when they create an account
    poster_urls = preferenceTuningPosters()
    if "responses" not in session:
        session["responses"] = []

    if "tuning_idx" not in session:
        session["tuning_idx"] = 0
    if session["tuning_idx"] == len(poster_urls):
        session["tuning_idx"] = 0

    if request.method == "POST":
        response = request.form.get("response")
        session["responses"].append(response)
        session['tuning_idx'] += 1
    
    idx = session["tuning_idx"]
    if idx < len(poster_urls):
        poster_url = poster_urls[idx]
        if request.method == "POST":
            time.sleep(0.2)
        return render_template("swipe.html", poster_url=poster_url)
    else:
        return redirect(url_for("views.get_language"))
    
@views.route("/get-recommendations", methods=["GET", "POST"])
def get_recommendations():
    if request.method == "POST":
        query = request.form["prompt"]
        result = db.get_recommendations(query)

    return render_template("preferences.html", messages=result)