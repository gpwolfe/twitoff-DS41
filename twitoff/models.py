from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True)
    username = DB.Column(DB.String, nullable=True)
    newest_tweet = DB.Column(DB.BigInteger)

    def __repr__(self) -> str:
        return f"<User: {self.username}>"


class Tweet(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    vector = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(
        DB.BigInteger, DB.ForeignKey("user.id"), nullable=False
    )
    # SQLAlchemy will look up user in the "User" class? table?
    # The backref is the reverse lookup, so you can see tweets by user
    # as well as the user by tweets, ie: user.tweets, tweet.user
    user = DB.relationship("User", backref=DB.backref("tweets", lazy=True))

    def __repr__(self) -> str:
        return f"<Tweet: {self.text}>"
