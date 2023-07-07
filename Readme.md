Flask Application
=================

This is a Flask application for user registration, login, and note-taking.

Features
--------

-   User registration and login functionality
-   Add and delete notes functionality
-   Contact form to send messages
-   Secure password storage using hashing
-   MySQL database integration
-   Flask session management

Installation
------------

1.  Clone the repository to your local machine:

    `git clone https://github.com/your-username/flask-application.git`

2.  Navigate to the project directory:

    `cd flask-application`

3.  Create a virtual environment:

    `python -m venv venv`

4.  Activate the virtual environment:

    -   For Windows:

        `venv\Scripts\activate`

    -   For macOS/Linux:

        `source venv/bin/activate`

5.  Install the required dependencies:

    `pip install -r requirements.txt`

6.  Set up the MySQL database:

    -   Create a new MySQL database with flask.

    -   Update the database configuration in the `app.py` file:

        `app.config["MYSQL_HOST"] = "localhost"
        app.config["MYSQL_USER"] = "your-username"
        app.config["MYSQL_PASSWORD"] = "your-password"
        app.config["MYSQL_DB"] = "your-database-name"`

7.  Run the application:

    `python app.py`

8.  Open your web browser and navigate to `http://127.0.0.1:5000/` to access the application.

Usage
-----

-   Register a new user account by providing a username and password.
-   Login with your credentials to access the main dashboard.
-   Add new notes and view existing notes on the "Notes" page.
-   Delete notes by clicking the delete button next to each note.
-   Use the "Contact" page to send messages to the application owner.

Contributing
------------

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
