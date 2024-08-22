from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from flask_login import login_required, current_user
from .scripts import preferenceTuningPosters
import time
from sentence_transformers import SentenceTransformer
from tidb_vector.integrations import TiDBVectorClient
from dotenv import load_dotenv
import os


load_dotenv()

embed_model = SentenceTransformer("all-mpnet-base-v2")
embed_model_dims = embed_model.get_sentence_embedding_dimension()

# Generates vector embeddings for the given text.
def text_to_embedding(text):
    embedding = embed_model.encode(text)
    return embedding.tolist()


views = Blueprint("views", __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route("/welcome")
def welcome():
    return render_template("welcome.html")

@views.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

@views.route("/tune-preferences", methods=["GET", "POST"])
def tune_preferences():
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
        return redirect(url_for("views.thankyou"))
    
@views.route("/get-recommendations", methods=["GET", "POST"])
def get_recommendations():
    if request.method == "POST":
        # Connect to Vector Database to retrieve movie recommendations
        vector_store = TiDBVectorClient(
        table_name='movie_plots',
        connection_string=os.getenv("CONNECTION_STR"),
        vector_dimension=int(os.getenv("EMBED_MODEL_DIMS"))
        )
        query = request.form["prompt"]
        query_embedding = text_to_embedding(query)
        search_result = vector_store.query(query_embedding, k=7)
        result = [r.document for r in search_result]

    return render_template("home.html", messages=result)