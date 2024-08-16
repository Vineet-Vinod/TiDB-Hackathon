import mysql.connector

from sentence_transformers import SentenceTransformer
from tidb_vector.integrations import TiDBVectorClient
from imdb import Cinemagoer

import os
from dotenv import load_dotenv
load_dotenv()


# Connect to Database
print("Connecting to DB")
connection = mysql.connector.connect(
    host = os.getenv("TIDB_HOST"),
    port = 4000,
    user = os.getenv("TIDB_USER"),
    password = os.getenv("TIDB_PASSWORD"),
    database = "app_main",
    ssl_ca = 'cert.pem'
)


# Model to create vector embeddings
print("Loading embedding model")
embed_model = SentenceTransformer("all-mpnet-base-v2")

# Generates vector embeddings for the given text
def text_to_embedding(text):
    embedding = embed_model.encode(text)
    return embedding.tolist()


# Connect to Vector Database to store movie plots
print("Connecting to Vector DB Table")
vector_store = TiDBVectorClient(
   table_name='movie_plots',
   connection_string=os.getenv("CONNECTION_STR"),
   vector_dimension=int(os.getenv("EMBED_MODEL_DIMS"))
)


# Use cinemagoer library to load movie data
# Add movie data to SQL database and plot data to vector DB
print("Loading and adding movie data")

ia = Cinemagoer() 
genres = ["Action", "Adventure", "Animation", "Comedy", "Crime",
          "Documentary", "Drama", "Family", "Fantasy", "Film-Noir",
          "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "Western"]
movie_ids = set() # Local store of movie IDs

for genre in genres:
    documents = [] # Store movie data for genre
    search = ia.get_top50_movies_by_genres(genre) # Get popular movies in genre
    
    for mov in search:
        ia.update(mov) # Load all movie info
        id = int(ia.get_imdbID(mov)) # Get movie ID

        if id not in movie_ids:
            movie_ids.add(id) # Add movie ID to local store

            doc = {} # Reset movie data dictionary

            doc["id"] = id # Store ID

            title = mov["title"].lower() # Store title
            doc["title"] = title

            plot = ' '.join(mov["plot"]) # Store plot embedding
            doc["embedding"] = text_to_embedding(plot)

            doc["metadata"] = {} # Store movie metadata
            genres = "None"
            langs = "None"
            try:
                doc["metadata"]["genres"] = mov["genres"]
                genres = ','.join(mov["genres"]) # Store all genres in a string
            except: # If the movie does not have a genres field, skip it without throwing an error
                pass

            try:
                doc["metadata"]["languages"] = mov["languages"]
                langs = ','.join(mov["languages"]) # Store all languages in a string
            except: # If the movie does not have a languages field, skip it without throwing an error
                pass

            documents.append(doc) # Add movie data dictionary to list
            connection.cursor().execute("INSERT INTO movies (movieid, title, plot, genres, langs) VALUES (%s, %s, %s, %s, %s)", (doc["id"], doc["title"], plot, genres, langs))

    vector_store.insert(
        ids=[doc["id"] for doc in documents],
        texts=[doc["title"] for doc in documents],
        embeddings=[doc["embedding"] for doc in documents],
        metadatas=[doc["metadata"] for doc in documents],
    )


print("Done adding movie data to DBs!")