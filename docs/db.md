# `Database` Class Documentation

The `Database` class serves as a singleton interface for interacting with the MySQL database and TiDB vector store. It manages user data, movie recommendations, and vector embeddings.

## Overview

- **Singleton Pattern:** The `Database` class follows the Singleton pattern to ensure that only one instance of the database connection is maintained throughout the application.
- **Dependencies:**
  - `mysql.connector` for MySQL database connections.
  - `SentenceTransformer` from the `sentence_transformers` package for generating vector embeddings.
  - `TiDBVectorClient` from `tidb_vector.integrations` for vector search operations.
  - `Cinemagoer` from `imdb` for fetching movie data.
  - `dotenv` for loading environment variables.

## Methods

### `__new__(cls, *args, **kwargs)`

- **Description:** Implements the Singleton pattern by ensuring only one instance of the `_Database` class is created.
- **Returns:** An instance of `_Database`.

### `_Database` Class

#### `__init__(self)`

- **Description:** Initializes the database by establishing a connection and setting the current timestamp. Also initializes the embedding model and IMDb client.
- **Calls:**
  - `establish_connection()`: Establishes the database and vector store connections.

#### `establish_connection(self)`

- **Description:** Establishes a connection to the MySQL database and TiDB vector store using credentials from environment variables.
- **Parameters:** None
- **Returns:** None

#### `text_to_embedding(text: str) -> list`

- **Description:** Generates vector embeddings for the given text using the SentenceTransformer model.
- **Parameters:**
  - `text`: The input text to generate embeddings for.
- **Returns:** A list representing the vector embedding of the input text.

#### `add_user_data(self, data: tuple = None, movies: tuple = None) -> None`

- **Description:** Adds or updates user data in the database, including user preferences and selected movies.
- **Parameters:**
  - `data`: A tuple containing user data (email, password, genres, languages).
  - `movies`: A tuple of movie IDs associated with the user.
- **Returns:** None

#### `get_user_data(self, username: str) -> str | None`

- **Description:** Retrieves the stored password for the given username from the database.
- **Parameters:**
  - `username`: The email or username to look up.
- **Returns:** The stored password as a string if found, otherwise `None`.

#### `get_recommendations(self, query: str, username: str = None) -> list`

- **Description:** Generates movie recommendations based on a text query and optionally the user's preferences.
- **Parameters:**
  - `query`: The search query for generating recommendations.
  - `username`: (Optional) The username to fetch user-specific preferences.
- **Returns:** A list of movie IDs that match the query and user preferences.

#### `get_movie_data(self, movieid: int) -> tuple`

- **Description:** Fetches movie data from IMDb, including the poster URL, title, and plot.
- **Parameters:**
  - `movieid`: The IMDb ID of the movie to fetch.
- **Returns:** A tuple containing the movie's poster URL, title, and plot.

## Dependencies

- **Environment Variables:**

  - `TIDB_HOST`: Hostname for the TiDB database.
  - `TIDB_USER`: Username for the TiDB database.
  - `TIDB_PASSWORD`: Password for the TiDB database.
  - `CONNECTION_STR`: Connection string for the TiDB vector store.
  - `EMBED_MODEL_DIMS`: Dimensionality of the embedding model.

- **External Libraries:**
  - `mysql.connector`: For MySQL database connectivity.
  - `SentenceTransformer`: For generating vector embeddings.
  - `TiDBVectorClient`: For querying vector data.
  - `Cinemagoer`: For fetching movie data from IMDb.
  - `dotenv`: For loading environment variables from a `.env` file.

---

This documentation provides an essential understanding of the `Database` class and its role in managing user data and generating recommendations within the Flask application.
