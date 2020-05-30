import api
import agent
if __name__ == "__main__":
    # api.app.run(debug=True)
    tweets = agent.run_query("peru")
    for tweet in tweets:
        print(tweet.tweet)
