# Movie Data Processing and Database Setup

## Overview

This script performs the following tasks:

1. **Connects to a MySQL database** to store movie data.
2. **Loads and processes movie data** using the Cinemagoer library.
3. **Generates vector embeddings** for movie plots using the SentenceTransformer model.
4. **Stores movie data and embeddings** in a MySQL database and a vector database.

## Prerequisites

- Python 3.x
- Required libraries: `mysql-connector-python`, `sentence-transformers`, `tidb-vector`, `IMDbPY`, `python-dotenv`
- MySQL database
- TiDB vector database
- `.env` file with the following environment variables:
  - `TIDB_HOST`: Host for TiDB
  - `TIDB_USER`: User for TiDB
  - `TIDB_PASSWORD`: Password for TiDB
  - `CONNECTION_STR`: Connection string for TiDB vector database
  - `EMBED_MODEL_DIMS`: Dimension of the embedding model

## Script Execution

### Database Connection

Connects to the TiDB database using credentials from the `.env` file:

```python
connection = mysql.connector.connect(
    host=os.getenv("TIDB_HOST"),
    port=4000,
    user=os.getenv("TIDB_USER"),
    password=os.getenv("TIDB_PASSWORD"),
    database="app_main",
    autocommit=True,
    ssl_ca='cert.pem'
)
```
