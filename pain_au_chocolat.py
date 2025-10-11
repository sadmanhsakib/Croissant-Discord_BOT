import os
import asyncpraw
import dotenv
import random

# loading the .env file
dotenv.load_dotenv(".env")

# getting the data from the .env file
USERNAME = os.getenv("REDDIT_USERNAME")
PASSWORD = os.getenv("REDDIT_PASSWORD")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("SECRET")
USER_AGENT = "Pain au Chocolat (by u/Herr_Sakib)"

reddit = None

async def authenticate():
    global reddit
    
    # authenticating with the api with the credentials
    reddit = asyncpraw.Reddit(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        username = USERNAME,
        password = PASSWORD,
        user_agent = USER_AGENT
    )
    
    user = await reddit.user.me()
    # printing a confirmation message
    print("✅Logged in as: ", user.name)


# this class represents each submission
class Submission:
    def __init__(self, submission):
        self.url = submission.url
        self.title = submission.title
        self.author = str(submission.author) if submission.author else "[deleted]"
        self.is_nsfw = submission.over_18
        

# this class fetches data from reddit and returns to Submission
class Fetch:
    def __init__(self):
        self.reddit = reddit
        self.search_limit = int(dotenv.get_key(".env", "SEARCH_LIMIT"))
        
        # parsing the nsfw_allowed from the .env file
        if int(dotenv.get_key(".env", "NSFW_ALLOWED")) == 1:
            self.nsfw_allowed = True
        else:
            self.nsfw_allowed = False
        
    async def get_submission(self, subreddit_name):
        submission_list = []
        # getting the subreddit
        subreddit = await self.reddit.subreddit(subreddit_name)
        # fetches the actual subreddit data
        await subreddit.load()

        # returning error message for permission error
        if subreddit.over18 and not self.nsfw_allowed:
            return "NSFW content is disabled. To enable it type: `-set nsfw_allowed true`"
        else:
            # getting a random post from the subreddit
            async for submission in subreddit.new(limit=self.search_limit):
                # checking if the post is an image or gif
                # these extra parentheses creates a tuple, basically we are supplying a tuple as argument
                if submission.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    submission_list.append(Submission(submission))
                    
            # returning a random submission from the list
            return random.choice(submission_list)
