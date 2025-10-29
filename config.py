import os, json
import dotenv

dotenv.load_dotenv(".env", override=True)

BOT_TOKEN = os.getenv("BOT_TOKEN")
REPO_URL = os.getenv("REPO_URL")
DATABASE_URL = os.getenv("DATABASE_URL")
TYPES = os.getenv("TYPE").split(",")
USERNAME = os.getenv("REDDIT_USERNAME")
PASSWORD = os.getenv("REDDIT_PASSWORD")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("SECRET")
prefix = os.getenv("PREFIX")
search_limit = int(os.getenv("SEARCH_LIMIT"))
nsfw_allowed = os.getenv("NSFW_ALLOWED")
# getting the value 
if nsfw_allowed.lower() == "true":
    nsfw_allowed = True
else:
    nsfw_allowed = False
delete_after = int(os.getenv("DELETE_AFTER"))
presence_update_channel_id = int(os.getenv("PRESENCE_UPDATE_CHANNEL_ID"))
gif_dict = json.loads(os.getenv("GIF"))
img_dict = json.loads(os.getenv("IMG"))
vid_dict = json.loads(os.getenv("VID"))