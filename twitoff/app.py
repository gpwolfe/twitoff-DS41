from flask import Flask, render_template
import os
from twitoff.models import DB, User, Tweet


def create_app():
    app = Flask(__name__)

    # Configure database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    @app.route("/")
    def root():
        # query for DB users (all)
        users = User.query.all()
        return render_template("base.html", title="Home", users=users)

    app_title = "Twitoff DS41"

    @app.route("/test")
    def test():
        return f"<p>Another {app_title} page</p>"

    @app.route("/hola")
    def hola():
        return "Hola, Twitoff!"

    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        return """The DB has been reset
        <a href='/'>Go to Home</a>
        <a href='/reset'>Go to Reset</a>
        <a href='/populate'>Go to Populate</a>
        """

    @app.route("/populate")
    def populate():
        sam = User(id=1, username="sam")
        DB.session.add(sam)
        tom = User(id=2, username="tom")
        DB.session.add(tom)
        tweet1 = Tweet(id=1, user=sam, text="This is my first tweet")
        tweet2 = Tweet(id=2, user=tom, text="This is mine!")
        tweet3 = Tweet(id=3, user=sam, text="This is my second tweet")
        tweet4 = Tweet(id=4, user=tom, text="Okay. That's a boring tweet.")
        tweet5 = Tweet(id=5, user=sam, text="What else can we write?")
        tweet6 = Tweet(id=6, user=sam, text="Hellooooo???")

        DB.session.add_all([tweet1, tweet2, tweet3, tweet4, tweet5, tweet6])
        DB.session.commit()
        return """The DB has been reset
            <a href='/'>Go to Home</a>
            <a href='/reset'>Go to Reset</a>
            <a href='/populate'>Go to Populate</a>
            """

    return app
