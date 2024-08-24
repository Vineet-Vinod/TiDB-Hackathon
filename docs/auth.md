# Flask Authentication Routes Documentation

This document provides an overview and explanation of the authentication-related routes in the Flask application. These routes handle user login, sign-up, and logout functionalities.

## Overview

The authentication routes are part of a Blueprint named `auth`. These routes handle user authentication tasks, including login, sign-up, and logout. The application conditionally initializes a database interface depending on the configuration.

## Routes

### Login (`/login`)

- **URL:** `/login`
- **Methods:** `GET`, `POST`
- **Description:** Handles user login. Validates the user's email and password against the database. If the credentials are correct, the user is logged in, and session data is updated. If validation fails, an error message is flashed, and the user is returned to the login page.
- **Session Data:**
  - `email`: Stores the user's email.
  - `loggedin`: A flag indicating whether the user is logged in.
- **Database Interaction:** Retrieves user data (password) for the provided email.

### Sign Up (`/sign-up`)

- **URL:** `/sign-up`
- **Methods:** `GET`, `POST`
- **Description:** Handles user account creation. Validates the email, password, and password confirmation. If all validations pass and the email is not already in use, the account is created, and the user is redirected to the welcome page.
- **Session Data:**
  - `email`: Stores the user's email.
  - `password`: Stores the user's password.
  - `loggedin`: A flag indicating whether the user is logged in.
- **Database Interaction:** Checks if the email already exists in the database.

### Logout (`/logout`)

- **URL:** `/logout`
- **Methods:** `GET`
- **Description:** Logs the user out by clearing the session data and redirecting them to the login page.

### Password Authentication Function

- **Function Name:** `password_authenticator(password: str)`
- **Description:** Validates a password based on specific criteria, such as length, presence of uppercase and lowercase letters, and inclusion of a number.
- **Returns:**
  - `0`: If the password is valid.
  - A string describing the reason for invalidation (e.g., "too short", "missing a lowercase letter").

## Conditional Database Initialization

- **Condition:** If `USE_TIDB` is set to `True`.
- **Action:** Imports and initializes the `Database` class from `db_interface`. The `db` instance is used for authentication-related database operations.

---

This documentation provides an essential understanding of the authentication system within the Flask application.
