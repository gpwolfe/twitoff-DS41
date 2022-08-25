import numpy as np
from sklearn.linear_model import LogisticRegression
from twitoff.models import User
from twitoff.twitter import vectorize_tweet


def predict(username0, username1, hypo_tweet_text):
    # returns just one tweet from the user id equal to username0
    user0 = User.query.filter(User.username == username0).one()
    user1 = User.query.filter(User.username == username1).one()

    # grab tweet vectors from each user (as np array)
    user0_vectors = np.array([tweet.vector for tweet in user0.tweets])
    user1_vectors = np.array([tweet.vector for tweet in user1.tweets])

    vectors = np.vstack([user0_vectors, user1_vectors])
    labels = np.concatenate(
        [np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))]
    )

    log_reg = LogisticRegression().fit(vectors, labels)

    hypo_tweet_vector = vectorize_tweet(hypo_tweet_text)

    return log_reg.predict(hypo_tweet_vector.reshape(1, -1))
