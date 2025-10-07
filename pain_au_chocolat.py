import os
import praw
import dotenv
import random

# loading the .env file
dotenv.load_dotenv(".env")

# getting the constants from the .env file
USERNAME = os.getenv("REDDIT_USERNAME")
PASSWORD = os.getenv("REDDIT_PASSWORD")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("SECRET")
COUNTER = int(os.getenv("COUNTER"))
USER_AGENT = "Pain au Chocolat (by u/Herr_Sakib)"

reddit = None

def authenticate():
    global reddit
    
    # starting the bot with the credentials
    reddit = praw.Reddit(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        username = USERNAME,
        password = PASSWORD,
        user_agent = USER_AGENT
    )
    
    # printing a confirmation message
    print("✅Logged in as: ", reddit.user.me())

def get_meme(subreddit_name):
    urls = []
    
    # getting the subreddit
    subreddit = reddit.subreddit(subreddit_name)
    
    # getting a random post from the subreddit
    for submission in subreddit.new(limit=COUNTER):
        # checking if the post is an image or gif
        if submission.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            urls.append(submission.url)
            
    # getting a random meme url from the list
    meme_url = urls[random.randint(0, len(urls) - 1)]
    return meme_url

def is_nsfw(subreddit_name):
    # getting the subreddit
    subreddit = reddit.subreddit(subreddit_name)
    
    return subreddit.over18