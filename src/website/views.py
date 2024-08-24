from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from .scripts import preferenceTuningPosters
from .config import USE_TIDB

# Conditionally import and initialize the database if USE_TIDB is True
# Used for debugging
if USE_TIDB:
    from .db_interface import Database     
    db = Database()

# Used to render website content
views = Blueprint("views", __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/info')
def info():
    return render_template("info.html")

# Used after a new account is created
@views.route("/welcome")
def welcome():
    return render_template("welcome.html")

# Used after preferences are submitted
@views.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

# Collects selected languages and genres from the form
@views.route("/get-language", methods=["GET", "POST"])
def get_language():
    if request.method == "POST":
        # Collect selected languages and genres from the form
        languages = ','.join(request.form.getlist("languages"))
        genres = ','.join(request.form.getlist("genres"))
        
        # Prepare user data for saving
        userdata = (session["email"], session["password"], genres, languages)

        # Map session responses to movie IDs
        movies = []
        movie_ids = [15398776, 120338, 110357, 68646, 107290, 1745960, 111161, 468569]
        for res in session["responses"]:
            movies.append(movie_ids[int(res)])

        # Add user data and movie preferences to the database
        db.add_user_data(userdata, tuple(movies))

        return redirect(url_for("views.thankyou"))

    return render_template("preferences.html")


@views.route("/tune-preferences", methods=["GET", "POST"])
def tune_preferences(): # They should get this page only when they create an account
    # Get movie poster URLs for preference tuning
    template_movies = preferenceTuningPosters()
    
    # Initialize session variables if not already set
    if "responses" not in session:
        session["responses"] = []
    if "tuning_idx" not in session:
        session["tuning_idx"] = 0
    if session["tuning_idx"] == len(template_movies):
        session["tuning_idx"] = 0

    if request.method == "POST":
        # Record the user's response to the current poster
        response = request.form.get("response")
        if response == "right":
            session["responses"].append(session["tuning_idx"])
        session['tuning_idx'] += 1
    
     # Display the current poster URL or redirect to language preferences
    idx = session["tuning_idx"]
    if idx < len(template_movies):
        template_movie = template_movies[idx]
        return render_template("swipe.html", poster_url=template_movie[0], movie_title=template_movie[1], movie_plot=template_movie[2])
    else:
        return redirect(url_for("views.get_language"))

# Global variables for storing recommendation data
# These must be global to maintain static state
choosing_urls = []
choosing_movies = []
@views.route("/get-recommendations", methods=["GET", "POST"])
def get_recommendations():
    global choosing_urls
    global choosing_movies
    if request.method == "POST":
        if "prompt" in request.form:
            query = request.form["prompt"]
            username = None
            
            try:
                username = session["email"]
            except:
                pass
            
            choosing_movies = [db.get_movie_data(r) for r in db.get_recommendations(query, username)]
            choosing_urls = [r[0] for r in choosing_movies]
            if "choosing_idx" in session: session["choosing_idx"] = 0

    # Initialize session variables if not already set
    if "choosing_idx" not in session:
        session["choosing_idx"] = 0
    if session["choosing_idx"] == len(choosing_urls):
        session["choosing_idx"] = 0

    if request.method == "POST":
        # Record the user's response to the current recommendation
        response = request.form.get("response")
        if response == "right":
            return render_template("home.html")
        session["choosing_idx"] += 1

    # Display the current recommendation poster or render the home page
    idx = session["choosing_idx"]
    if idx == len(choosing_urls):
        return render_template("home.html")
    poster_url = choosing_urls[idx]
    if request.method == "POST":
        return render_template("swipe.html", poster_url=poster_url, movie_title=choosing_movies[idx][1], movie_plot=choosing_movies[idx][2])
    else:
        return render_template("home.html")