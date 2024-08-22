# DO NOT RUN!!!
# Running will reset the database


import mysql.connector
from tidb_vector.integrations import TiDBVectorClient
import os
from dotenv import load_dotenv
load_dotenv()

x = 1 / 0 # Error to ensure file does not execute (comment out to run file)

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


# Create Tables to store users and movie data
print("Creating Tables")
with connection.cursor() as cur:
    cur.execute("DROP TABLE IF EXISTS UserMovies;")
    cur.execute("DROP TABLE IF EXISTS users;")
    cur.execute("DROP TABLE IF EXISTS movies;")

    cur.execute(
        """
        CREATE TABLE users (
            username VARCHAR(150) PRIMARY KEY NOT NULL,
            password VARCHAR(150) NOT NULL,
            genres VARCHAR(150),
            langs VARCHAR(150)
        );
    """
    )

    cur.execute(
        """
        CREATE TABLE movies (
            movieid INT PRIMARY KEY NOT NULL,
            title VARCHAR(100) NOT NULL,
            plot TEXT NOT NULL,
            genres VARCHAR(150),
            langs VARCHAR(150)
        );
    """
    )

    cur.execute(
        """
        CREATE TABLE UserMovies (
            username VARCHAR(150),
            movieid INT,
            PRIMARY KEY (username, movieid),
            FOREIGN KEY (username) REFERENCES users(username),
            FOREIGN KEY (movieid) REFERENCES movies(movieid)
        );
    """
    )


# Create Vector Database to store movie plots
print("Creating Vector DB Table")
vector_store = TiDBVectorClient(
   table_name='movie_plots',
   connection_string=os.getenv("CONNECTION_STR"),
   vector_dimension=int(os.getenv("EMBED_MODEL_DIMS")),
   drop_existing_table=True
)

print("Database setup complete!")