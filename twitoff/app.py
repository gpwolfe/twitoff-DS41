from flask import Flask, render_template, request
import os
from twitoff.predict import predict
from twitoff.models import DB, User, Tweet
from twitoff.twitter import add_or_update_user


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

    # The <> allows flask to parse the URL, where it will pass
    # <name> into the following function
    @app.route("/user/<name>")
    def user(name=None):
        print(f"name is {name}")

    # This changes the method from GET to POST for info submission/upload
    @app.route("/user", methods=["POST"])
    def add_user():
        # The key values come from the base.html in this case
        username = request.values["user_name"]
        add_or_update_user(username)
        # Here we return a web page, adding in necessary info according
        #  to user.html
        user = User.query.filter(User.username == username).one()
        return render_template(
            "user.html",
            title=username,
            message="User added successfully",
            tweets=user.tweets,
        )

    @app.route("/update")
    def update():
        users = User.query.all()
        for user in users:
            add_or_update_user(user.username)
        return """Users have been updated
        <a href='/'>Go to Home</a>
        <a href='/reset'>Go to Reset</a>
        <a href='/update'>Go to Update</a>
        """

    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        return """The DB has been reset
        <a href='/'>Go to Home</a>
        <a href='/reset'>Go to Reset</a>
        <a href='/update'>Go to Update</a>
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

    @app.route("/compare", methods=["POST"])
    def compare():
        username0 = request.values["user0"]
        username1 = request.values["user1"]
        hypo_text_tweet = request.values["tweet_text"]

        if username0 == username1:
            message = "Cannot compare a user to themselves"
        else:

            prediction = predict(username0, username1, hypo_text_tweet)
            if prediction:
                predicted_user = username1
            else:
                predicted_user = username0
            message = f"This tweet was more likely written by {predicted_user}"
        return render_template(
            "prediction.html", title="Prediction", message=message
        )

    return app
