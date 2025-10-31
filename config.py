import os, json
import dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
REPO_URL = os.getenv("REPO_URL")
DATABASE_URL = os.getenv("DATABASE_URL")
USERNAME = os.getenv("REDDIT_USERNAME")
PASSWORD = os.getenv("REDDIT_PASSWORD")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("SECRET")

prefix = None
search_limit = None
nsfw_allowed = None
delete_after = None
presence_update_channel_id = None
storage_dict = None


from database import db

async def load_data():
    global prefix, search_limit, nsfw_allowed, delete_after, presence_update_channel_id, storage_dict

    # getting the variable value for the database
    prefix = await db.get_variable("PREFIX")
    
    search_limit = await db.get_variable("SEARCH_LIMIT")
    search_limit = int(search_limit)

    nsfw_allowed = await db.get_variable("NSFW_ALLOWED")
    nsfw_allowed = True if nsfw_allowed.lower() == "true" else False

    delete_after = await db.get_variable("DELETE_AFTER")
    delete_after = int(delete_after)
    
    presence_update_channel_id = await db.get_variable("PRESENCE_UPDATE_CHANNEL_ID")
    presence_update_channel_id = int(presence_update_channel_id)
    
    storage_dict = json.loads(await db.get_variable("STORAGE"))


async def set_default():
    await db.set_variable("PREFIX", "-")
    await db.set_variable("SEARCH_LIMIT", "50")
    await db.set_variable("NSFW_ALLOWED", "false")
    await db.set_variable("DELETE_AFTER", "10")
    await db.set_variable("PRESENCE_UPDATE_CHANNEL_ID", "0")
    await db.set_variable("STORAGE", "{}")

    print("✅Successfully set the default values for this server!")
