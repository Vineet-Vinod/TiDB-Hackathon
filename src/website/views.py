from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from .scripts import preferenceTuningPosters
from .config import USE_TIDB
if USE_TIDB:
    from .db_interface import Database     
    db = Database()

views = Blueprint("views", __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/info')
def info():
    return render_template("info.html")

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

        userdata = (session["email"], session["password"], genres, languages)

        movies = []
        movie_ids = [15398776, 120338, 110357, 68646, 107290, 1745960, 111161, 468569]
        for res in session["responses"]:
            movies.append(movie_ids[int(res)])

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
        if response == "right":
            session["responses"].append(session["tuning_idx"])
        session['tuning_idx'] += 1
    
    idx = session["tuning_idx"]
    if idx < len(poster_urls):
        poster_url = poster_urls[idx]
        return render_template("swipe.html", poster_url=poster_url)
    else:
        return redirect(url_for("views.get_language"))

choosing_urls = []
@views.route("/get-recommendations", methods=["GET", "POST"])
def get_recommendations():
    global choosing_urls
    if request.method == "POST":
        if "prompt" in request.form:
            query = request.form["prompt"]
            choosing_movies = db.get_movie_data([r for r in db.get_recommendations(query, session["email"])])
            choosing_urls = [r[0] for r in choosing_movies]

    if "choosing_idx" not in session:
        session["choosing_idx"] = 0
    if session["choosing_idx"] == len(choosing_urls):
        session["choosing_idx"] = 0
    
    if request.method == "POST":
        response = request.form.get("response")
        if response == "right":
            return render_template("home.html")
        session["choosing_idx"] += 1

    idx = session["choosing_idx"] % len(choosing_urls)
    poster_url = choosing_urls[idx]
    return render_template("swipe.html", poster_url=poster_url)