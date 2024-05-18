import tweepy
# BEARER_TOKEN="AAAAAAAAAAAAAAAAAAAAAKwLtwEAAAAAbgnrqQKgl7RVuIODpK0MmQyRcM8%3DHMllkXk1cDBGtIgwGI3Jwxs64LBn0hZsO8SZfvtSzB1f7I1Rqw"
ACCESS_TOKEN="1789616702780477442-UlBCwMZj4cMfJIonUxih0bvoFKw10Y"
ACCESS_TOKEN_SECRET="C0Xk8WK5MpQ5vN2mJwlnySYRfY6g6nkndhz8X3Vzhl5hn"
API_KEY="pqvqKvWaK2ELMnejuH6TPicL4"
API_SECRET_KEY="aW7HPJSzROLFVvX9UVI1wN8ltgNgT1bRvtxeaeMA3uI69zOIvG"


auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth)

# The content you want to post as a tweet
tweet_content = "Hello, world! This is my first automated tweet using Python and Tweepy!"

# Post the tweet
api.update_status(tweet_content)

print("Tweet posted successfully!")
