import mysql.connector
from sentence_transformers import SentenceTransformer
from tidb_vector.integrations import TiDBVectorClient
from imdb import Cinemagoer
from dotenv import load_dotenv
import os
import ast
import time

load_dotenv()

class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.db = _Database()
        return cls._instance

    @classmethod
    def get_db(cls):
        return cls._instance.db
    

class _Database:
    curr_time = 0
    embed_model = SentenceTransformer("all-mpnet-base-v2")
    ia = Cinemagoer()
    # Generates vector embeddings for the given text.
    @staticmethod
    def text_to_embedding(text: str) -> list:
        embedding = _Database.embed_model.encode(text)
        return embedding.tolist()
    

    def __init__(self) -> None:
        self.establish_connection()
        self.curr_time = int(time.time())


    def establish_connection(self) -> None:
        self.sql_connection = mysql.connector.connect(
            host = os.getenv("TIDB_HOST"),
            port = 4000,
            user = os.getenv("TIDB_USER"),
            password = os.getenv("TIDB_PASSWORD"),
            database = "app_main",
            autocommit = True,
            ssl_ca = os.path.join(os.getcwd(), "website/cert.pem")
        )

        self.vector_store = TiDBVectorClient(
            table_name='movie_plots',
            connection_string=os.getenv("CONNECTION_STR"),
            vector_dimension=int(os.getenv("EMBED_MODEL_DIMS"))
        )


    def add_user_data(self, data: tuple = None, movies: tuple = None) -> None:
        if data:
            if int(time.time()) - self.curr_time > 300:
                self.sql_connection.close()
                self.establish_connection()
                self.curr_time = int(time.time())

            with self.sql_connection.cursor() as cursor:
                if len(data) == 4:
                    cursor.execute("INSERT INTO users (username, password, genres, langs) VALUES (%s, %s, %s, %s)", data)
                    self.curr_time = int(time.time())

                if movies:
                    insert_usermovies_query = "INSERT INTO UserMovies (username, movieid) VALUES (%s, %s)"
                    usermovies_values = [(data[0], mov) for mov in movies]
                    cursor.executemany(insert_usermovies_query, usermovies_values)
                    self.curr_time = int(time.time())


    def get_user_data(self, username: str) -> str | None:
        if int(time.time()) - self.curr_time > 300:
            self.sql_connection.close()
            self.establish_connection()
            self.curr_time = int(time.time())

        with self.sql_connection.cursor() as cursor:
            cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()

            return result[0] if result else None


    def get_recommendations(self, query: str, username: str = None)  -> list:
        query_embedding = _Database.text_to_embedding(query)

        if int(time.time()) - self.curr_time > 300:
                self.sql_connection.close()
                self.establish_connection()
                self.curr_time = int(time.time())

        # Get user preferences - genres, languages from user database
        genres, languages = set(["Drama", "Thriller", "Action"]), set(["Malayalam"])
        if username:
            with self.sql_connection.cursor() as cursor:
                sql_query = """SELECT genres, langs
                                FROM users
                                WHERE username = %s"""
                cursor.execute(sql_query, (username,))
                result = cursor.fetchone()
                self.curr_time = int(time.time())

                if result:
                    gen, lang = result
                    genres = set(gen.split(","))
                    languages = set(lang.split(","))

        search_result = self.vector_store.query(query_embedding, k=15)

        recommendations = []
        for result in search_result:
            res_dict = ast.literal_eval(str(result.metadata))
            mov_genres = set(res_dict.get('genres'))
            mov_languages = set(res_dict.get('languages'))
            if genres.intersection(mov_genres) and languages.intersection(mov_languages):
                recommendations.append(result.document)
        
        return recommendations
        

if __name__ == "__main__":
    pass