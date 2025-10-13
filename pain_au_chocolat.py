import os
import asyncpraw, asyncprawcore
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

async def authenticate() -> bool:
    global reddit
    
    # if already authenticated
    if reddit is not None:
        return True
    
    try:
        # authenticating with the api with the credentials
        reddit = asyncpraw.Reddit(
            client_id = CLIENT_ID,
            client_secret = CLIENT_SECRET,
            username = USERNAME,
            password = PASSWORD,
            user_agent = USER_AGENT
        )
        
        # verify authentication
        user = await reddit.user.me()
        print("✅Logged in as: ", user.name)
        return True
    except Exception as e:
        print(f"❌ Reddit authentication failed: {e}")
        reddit = None
        return False

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
        global reddit
        
        if reddit is None:
            raise RuntimeError("Reddit not authenticated. Call authenticate() first. ")
        
        self.reddit = reddit
        # reloads the .env file and overrides any changes
        dotenv.load_dotenv(".env", override=True)
        self.search_limit = int(os.getenv("SEARCH_LIMIT"))
        
        # parsing the nsfw_allowed from the .env file
        if int(os.getenv("NSFW_ALLOWED")) == 1:
            self.nsfw_allowed = True
        else:
            self.nsfw_allowed = False
        
    async def get_submission(self, subreddit_name):
        # getting the subreddit
        subreddit = await self.reddit.subreddit(subreddit_name)
        # fetches the actual subreddit data
        try:
            await subreddit.load()
        except asyncprawcore.exceptions.NotFound:
            return f"❌ Subreddit r/{subreddit_name} not found"
        except asyncprawcore.exceptions.Forbidden:
            return f"❌ Access to r/{subreddit_name} is restricted"

        # returning error message for permission error
        if subreddit.over18 and self.nsfw_allowed == False:
            return "🔞 NSFW content is disabled. To enable itm type: `-set nsfw_allowed true`"

        submission_list = []
        try:
            # getting a random post from the subreddit
            async for submission in subreddit.new(limit=self.search_limit):
                # checking if the post is an image or gif and not stickied
                # these extra parentheses creates a tuple, basically we are supplying a tuple as argument
                if not submission.stickied and submission.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    submission_list.append(Submission(submission))
        except asyncprawcore.exceptions.Forbidden:
            return f"❌ Cannot fetch posts from r/{subreddit_name} (possibly quarantined)."
        except Exception as e:
            return f"❌ Error fetching posts: {e}"
        
        if not submission_list:
            return f"🖼️ No image/GIF posts found in r/{subreddit_name} (checked {self.search_limit} posts)."
        
        # returning a random submission from the list
        return random.choice(submission_list)