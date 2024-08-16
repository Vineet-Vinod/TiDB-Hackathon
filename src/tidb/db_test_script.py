from sentence_transformers import SentenceTransformer
from tidb_vector.integrations import TiDBVectorClient
from imdb import Cinemagoer
from dotenv import load_dotenv
import os

load_dotenv()

print("Loading embedding model")
# Model to create vector embeddings
embed_model = SentenceTransformer("all-mpnet-base-v2")
embed_model_dims = embed_model.get_sentence_embedding_dimension()

# Generates vector embeddings for the given text.
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


# Print search results
def print_result(seen: set, result):
    for r in result:
      if r.document.lower() not in seen:
        seen.add(r.document.lower())
        print(f"\"{r.document}\"", end=", ")


# Main application
def app():
    ia = Cinemagoer()
    # Movie IDs of movies you have seen
    # To get movie IDs, go to IMDb.com and search for movie
    # Look at URL (sample for Skyfall): https://www.imdb.com/title/tt1074638/
    # The number after the tt, 1074638 here, is the ID
    seen_movs = set([120338, 109830, 1074638])
    seen = set(["titanic", "forrest gump", "skyfall"]) 
    print("You should watch: ")

    for s in seen_movs:
        mov = ia.get_movie(s)
        ia.update(mov)
        query = ' '.join(mov["plot"])
        query_embedding = text_to_embedding(query)
        search_result = vector_store.query(query_embedding, k=7)
        print_result(seen, search_result)


if __name__ == "__main__":
    app()