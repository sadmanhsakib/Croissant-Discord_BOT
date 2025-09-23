import discord
import random
import os
import dotenv
import json

# loading .env file
dotenv.load_dotenv(".env")
# config stores all the values inside the .env file
config = dotenv.dotenv_values(".env")

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
SLEEP_TIME = int(os.getenv("SLEEP_TIME"))
BOT_TOKEN = os.getenv("BOT_TOKEN")
QURAN_FILE = "quran.txt"
SUNNAH_FILE = "sunnah.txt"
QUOTES_FILE = "quote.txt"
QUOTE_LIST = [QURAN_FILE, SUNNAH_FILE, QUOTES_FILE]
TIME_FORMAT = "%Y-%m-%d -> %H:%M:%S"
GIFS = config.get("GIFS")
gif_dict = json.loads(GIFS)


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

    # deletes previous lines as per user request
    if message.content.startswith("-del"):
        try:
            amount = message.content.replace("-del ", "")
            amount = int(amount)

            # +1 to remove the command itself
            await message.channel.purge(limit=amount+1)
        except Exception:
            await message.channel.send("Invalid Argument!\nCorrent syntax: -del<space>[Number of Messages to Remove].")

    if message.content.startswith("-gif"):
        try:
            gif_name = message.content.replace("-gif ", "")

            gif_names = []
            for key in gif_dict.keys():
                gif_names.append(key)

            if gif_name in gif_names:
                await message.channel.send(gif_dict[gif_name], delete_after=SLEEP_TIME)
            elif gif_name not in gif_names:
                await message.channel.send(f"There is no {gif_name} in gif_storage. ")
                await message.channel.send(f"Available gifs are: {gif_names}")

        except Exception:
            await message.channel.send("Invalid prompt! Corrent syntax: -gif<space>GIF_NAME")

    if message.content.startswith("-greet"):
        try:
            gif_names = []
            for key in gif_dict.keys():
                gif_names.append(key)
            
            parts = message.content.split(' ')
            if len(parts) == 3:
                gif_name = parts[2]
                user_name = parts[1]
            elif len(parts) == 2:
                gif_name = "greet1"
                user_name = parts[1]
            
            if gif_name in gif_names:
                await message.channel.send(f"Hello, {user_name}")
                await message.channel.send(gif_dict[gif_name], delete_after=SLEEP_TIME)
            elif gif_name not in gif_names:
                await message.channel.send("There is no {gif_name} in gif_storage.")
                await message.channgel.send(f"Available gifs are: {gif_names}")
        except Exception:
            await message.channel.send("Invalid. Syntax: -greet<space>USERNAME<space><GIF_NAME")

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
    # getting the channel id
    dark_humor_channel = client.get_channel(DARK_HUMOR_CHANNEL_ID)

    # prevents replying to bot's presence update
    # also doesn't sends the messages if it's PERSONAL server
    if not after.bot and after.guild.id != 1297961145440931882:
        old_status = str(before.status)
        new_status = str(after.status)

        # if the user comes online
        if old_status == "offline" and new_status != "offline":
            # sends a greeting message
            await dark_humor_channel.send(f"Welcome back, {after.name}.")
            
        # if the user goes offline
        elif old_status != "offline" and new_status == "offline":     
            await dark_humor_channel.send(f"Bye, {after.name}")


# starts the bot
client.run(BOT_TOKEN)