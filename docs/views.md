# Flask Application Routes Documentation

This document provides an overview and explanation of the routes defined in the Flask application.

## Overview

The Flask application consists of several routes for rendering pages, handling user input, and managing session data. These routes are part of a Blueprint named `views`.

## Routes

### Home (`/`)

- **URL:** `/`
- **Methods:** `GET`
- **Description:** Renders the `home.html` template, which serves as the landing page of the application.

### Info (`/info`)

- **URL:** `/info`
- **Methods:** `GET`
- **Description:** Renders the `info.html` template to provide users with information about the application.

### Welcome (`/welcome`)

- **URL:** `/welcome`
- **Methods:** `GET`
- **Description:** Renders the `welcome.html` template, which is displayed after a user successfully creates an account.

### Thank You (`/thankyou`)

- **URL:** `/thankyou`
- **Methods:** `GET`
- **Description:** Renders the `thankyou.html` template after the user submits their preferences.

### Get Language (`/get-language`)

- **URL:** `/get-language`
- **Methods:** `GET`, `POST`
- **Description:** Handles the submission of selected languages and genres. On `POST`, the selected data is saved to the database, and the user is redirected to the "Thank You" page. On `GET`, the `preferences.html` form is displayed.
- **Session Data:**
  - `email`: User's email.
  - `password`: User's password.
  - `responses`: List of responses from the preference tuning stage.
- **Database Interaction:** Saves user data and movie preferences.

### Tune Preferences (`/tune-preferences`)

- **URL:** `/tune-preferences`
- **Methods:** `GET`, `POST`
- **Description:** Handles the process of tuning user preferences through a series of movie posters. On `POST`, the user's response to a movie poster is recorded, and the next poster is displayed. If all posters have been shown, the user is redirected to the language and genre selection page.
- **Session Data:**
  - `responses`: Stores the indices of liked movies.
  - `tuning_idx`: Tracks the current poster index.
- **Template:** Renders `swipe.html` with the current movie poster, title, and plot.

### Get Recommendations (`/get-recommendations`)

- **URL:** `/get-recommendations`
- **Methods:** `GET`, `POST`
- **Description:** Retrieves movie recommendations based on the user's input. On `POST`, a search query is processed, and recommended movies are fetched from the database. On `GET`, the user can swipe through recommendations. Liked movies are saved to the database.
- **Session Data:**
  - `choosing_idx`: Tracks the current recommendation index.
- **Global Variables:**
  - `choosing_urls`: Stores URLs of the movie posters.
  - `choosing_movies`: Stores movie data for the recommendations.
  - `movie_ids`: Stores IDs of the recommended movies.

## Database Initialization (Conditional)

- **Condition:** If `USE_TIDB` is set to `True`.
- **Action:** Imports and initializes the `Database` class from `db_interface`. The database instance (`db`) is then used for user data and movie preference storage throughout the application.

## Global Variables

- **`choosing_urls`**: Stores URLs of the movie posters for the recommendation system.
- **`choosing_movies`**: Stores the data of the movies being recommended.
- **`movie_ids`**: Stores the IDs of the recommended movies.

---

This document should help developers understand the purpose and flow of each route within the Flask application.
