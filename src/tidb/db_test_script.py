from sentence_transformers import SentenceTransformer
from tidb_vector.integrations import TiDBVectorClient
from imdb import Cinemagoer
import copy


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
   connection_string="mysql://3xMre5xoM4BvLzW.root:<PASSWORD>@gateway01.us-west-2.prod.aws.tidbcloud.com:4000/app_main",
   vector_dimension=embed_model_dims
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
    seen = set([120338, 109830, 1684562]) 
    seen_cpy = copy.deepcopy(seen)
    print("You should watch: ")

    for s in seen_cpy:
        mov = ia.get_movie(s)
        ia.update(mov)
        query = ' '.join(mov["plot"])
        query_embedding = text_to_embedding(query)
        search_result = vector_store.query(query_embedding, k=7)
        print_result(seen, search_result)


if __name__ == "__main__":
    app()