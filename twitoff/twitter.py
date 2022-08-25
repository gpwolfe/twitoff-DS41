from twitoff.models import DB, Tweet, User
import os
import spacy
import tweepy

key = os.getenv("TWITTER_API_KEY")
secret = os.getenv("TWITTER_API_KEY_SECRET")

twitter_auth = tweepy.OAuthHandler(key, secret)
twitter_api = tweepy.API(twitter_auth)

NLP = spacy.load("my_model")


def vectorize_tweet(tweet_text):
    return NLP(tweet_text).vector


def add_or_update_user(username):
    try:
        twitter_user = twitter_api.get_user(screen_name=username)

        # Either gather existing user or create new user
        db_user = (User.query.get(twitter_user.id)) or (
            User(id=twitter_user.id, username=username)
        )
        DB.session.add(db_user)
        # DB.session.commit()

        # Get tweets belonging to user id
        tweets = twitter_user.timeline(
            count=200,
            exclude_replies=True,
            include_rts=False,
            tweet_mode="extended",
            since_id=db_user.newest_tweet,
        )

        # These tweets are already in the database, so we can check back
        existing_tweets = Tweet.query.filter(Tweet.id == twitter_user.id).all()
        db_tweets_ids = [tweet.id for tweet in existing_tweets]

        # update the most recent tweet id, used as a start point for the
        # twitter api timeline
        if tweets:
            db_user.newest_tweet = tweets[0].id

        # add tweets to database using Tweet class object
        for tweet in tweets:
            if tweet.id not in db_tweets_ids:
                db_tweet = Tweet(
                    id=tweet.id,
                    text=tweet.full_text,
                    vector=vectorize_tweet(tweet.full_text[:300]),
                )
                # Adding tweet to the database user
                db_user.tweets.append(db_tweet)
                DB.session.add(db_tweet)

    except Exception as e:
        print(f"Error processing {username}: {e}")
        raise e

    else:
        DB.session.commit()
