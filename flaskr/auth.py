import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("core.index"))




@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        email = request.form["email"]
        name = request.form["name"]
        password = request.form["password"]
        db, cur = get_db()
        error = None

        if not email:
            error = "email is required."
        elif not name:
            error = "name is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                # Nickname inserted the same as username
                cur.execute(
                    "INSERT INTO users (email, name, password) VALUES (%s, %s, %s)"

                )
                db.commit()
            except Exception as e:
                # The username was already taken, which caused the
                # commit to fail. Show a validation error.
                print(e)
                error = f"name {name} is already registered, try again!"
            else:
                # Success, go to the login page.
                flash("Thank you for registration!")
                return redirect(url_for("login"))

        flash(error)

    return render_template("register.html")
