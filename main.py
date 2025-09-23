import discord
import datetime
import random
import os
import dotenv

# loading .env file
dotenv.load_dotenv(".env")

# for running the bot as a web 
from keep_alive import keep_alive
keep_alive()

# giving the permissions
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.presences = True
intents.members = True

client = discord.Client(intents=intents)

# Getting the CONST from the .env files
DARK_HUMOR_CHANNEL_ID = int(os.getenv("DARK_HUMOR_CHANNEL_ID"))
BOT_TOKEN = os.getenv("BOT_TOKEN")
TIME_FORMAT = "%Y-%m-%d -> %H:%M:%S"
QURAN_FILE = "quran.txt"
SUNNAH_FILE = "sunnah.txt"
QUOTES_FILE = "quote.txt"
QUOTE_LIST = [QURAN_FILE, SUNNAH_FILE, QUOTES_FILE]


@client.event
# when the bot starts 
async def on_ready():
    # prints a message in console when ready
    print(f"Logged in as: {client.user}")


@client.event
# when the user sends a message in server
async def on_message(message):
    # prevents the bot from replying on its own messages
    if message.author == client.user:
        return
    
    # stores every simple reply simple_commands
    message_dict = {
        "-hello": f"Good day, {message.author.mention}. Hope you are having a fantastic day. ",
        "-status": "Active."
    }

    help = "Command list:\n"
    # stores all the simple_commands name in help
    for k in message_dict.keys():
        help += f"{k}\n"
    # stores all the complex_commands name in help
    help += "-del\n-quran\n-quote\n-sunnah"
    # adding the help section to the dict
    message_dict.update({"-help": f"{help}"})

    # replies to user messages
    for msg in message_dict:
        if message.content.startswith(msg):
            await message.channel.send(message_dict[msg])

    # deletes the necessary lines as per user request
    if message.content.startswith("-del"):
        try:
            amount = message.content.replace("-del ", "")
            amount = int(amount)

            # +1 to remove the command itself
            await message.channel.purge(limit=amount+1)
        except Exception as error:
            await message.channel.send("Invalid Argument!\nCorrent syntax: -del<space>[Number of Messages to Remove].")

    if message.content.startswith("-"):
        # replying with quotes
        for x in QUOTE_LIST:
            # parsing the strings into user command style for comparing
            y = x.replace(f".txt", "")
            y = "-" + y

            if message.content == y:
                # since Bengali alphabet is in unicode, we need to open the file in unicode
                with open(x, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                    
                    # sending a random line from the user's desired type
                    await message.channel.send(lines[random.randint(0, (len(lines)-1))])


@client.event
# called when a member of the server changes their activity
# before and after represents the member that has changed presence;
async def on_presence_update(before, after):
    now = datetime.datetime.now().strftime(TIME_FORMAT)
    counter = 0

    # getting the channel id
    dark_humor_channel = client.get_channel(DARK_HUMOR_CHANNEL_ID)

    
    # preventing the bot from messaging on it's own
    if after.id != client.user:
        old_status = str(before.status)
        new_status = str(after.status)

        # if the user comes online
        if old_status == "offline" and new_status != "offline":
            # sends a greeting message
            await dark_humor_channel.send(f"Welcome, Back {after.name}.")
            
        # if the user goes offline
        elif old_status != "offline" and new_status == "offline":     
            await dark_humor_channel.send(f"Bye, {after.name}")


# starts the bot
client.run(BOT_TOKEN)