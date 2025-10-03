import discord
import random
import os
import dotenv
import json

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
intents.guilds = True

client = discord.Client(intents=intents)

# Getting the data from the default .env files
BOT_TOKEN = os.getenv("BOT_TOKEN")
REPO_LINK = os.getenv("REPO_LINK")

# declaring the variables for the server specific datas
presence_update_channel_id = int(os.getenv("PRESENCE_UPDATE_CHANNEL_ID"))
initial = os.getenv("INITIAL")
TYPES = os.getenv("TYPE").split(',')
SLEEP_TIME = int(os.getenv("SLEEP_TIME"))
# loading the dictionary into json format
gif_dict = json.loads(os.getenv("GIF"))
img_dict = json.loads(os.getenv("IMG"))
vid_dict = json.loads(os.getenv("VID"))

QUOTES = ["quran.txt", "sunnah.txt", "quote.txt"]
TIME_FORMAT = "%Y-%m-%d -> %H:%M:%S"


def get_dict(item_type):
    # finding the right type of dictionary
    match item_type:
        case "GIF":
            dictionary = gif_dict
        case "IMG":
            dictionary = img_dict
        case "VID":
            dictionary = vid_dict
    return dictionary


@client.event
# when the bot starts 
async def on_ready():
    # prints a message in console when ready
    print(f"Logged in as: {client.user}")

    guilds = client.guilds
    


@client.event
async def on_guild_join(guild):
    # getting the general channel of the server that the BOT just joined
    channel = discord.utils.get(guild.text_channels, name="general")

    if channel and channel.permissions_for(guild.me).send_messages:
        # sending greeting messages
        await channel.send("Thank you for adding Croissant!")
        await channel.send(f'Type: "{initial}help" to get the command list.')
        await channel.send(f"You can learn more about the BOT from here: {REPO_LINK}")

        # instructing the users on how to set up the channel
        await channel.send("By default, this bot sends greeting to members when they come online and goes offline. ")
        await channel.send("If you want to use this feature, use the '-set<space>CHANNEL_ID' command. ")


@client.event
# when the user sends a message in server
async def on_message(message):
    # prevents the bot from replying on its own messages
    if message.author == client.user:
        return
    
    gif_names = list(gif_dict.keys())
    img_names = list(img_dict.keys())
    vid_names = list(vid_dict.keys())

    # stores the simple_commands
    message_dict = {
        f"{initial}hello": f"Good day, {message.author.mention}. Hope you are having a fantastic day. ",
        f"{initial}status": "Active."
    }

    # stores all the command guides
    help = f"""```Command List:
{initial}hello
{initial}status
;ITEM_NAME
{initial}del number_of_messages_to_delete
{initial}list ITEM_NAME
{initial}greet USERNAME NAME
{initial}add TYPE NAME LINK
{initial}rmv TYPE NAME
{initial}set VARIABLE VALUE
{initial}randomline quran/sunnah/quote```"""
    
    # adding the help section to the dict
    message_dict.update({f"{initial}help": help})

    # replies to user messages
    for msg in message_dict:
        if message.content.startswith(msg):
            await message.channel.send(message_dict[msg])

    # reacting to hate messages
    if message.content.__contains__("clanker"):
        await message.add_reaction("💢")

    # deletes previous messages as per user request
    if message.content.startswith(f"{initial}del"):
        try:
            # extracting the data from the message
            parts = message.content.split(' ')
            amount = int(parts[1])

            # +1 to remove the command itself
            await message.channel.purge(limit=amount+1)
        except:
            await message.channel.send(f"Invalid command. Correct Syntax: `{initial}del number_of_messages_to_delete`")

    # replies with the list of objects as per user request
    elif message.content.startswith(f"{initial}list"):
        try:
            # extracting the data from the message
            parts = message.content.split(' ')
            item_type = parts[1].upper()
            
            if item_type in TYPES:
                # getting the correct dictionary
                dictionary = get_dict(item_type)
                # getting the keys from dictionary and converting it to a list
                keys = list(dictionary.keys())
                
                # checking if the keys are empty or not
                if keys != []:
                    await message.channel.send(f"```Available {item_type}s are:\n{keys}```")
                else:
                    await message.channel.send("Empty.")
            else:
                await message.channel.send(f"{item_type} doesn't exist.")
        except:
            await message.channel.send(f"Invalid command. Correct Syntax: `{initial}list ITEM_NAME`")
    
    # greets user with an item in TYPES
    elif message.content.startswith(f"{initial}greet"):
        try:
            # extracing the data for the message
            parts = message.content.split(' ')

            # checking if the user has given any item_name
            if len(parts) == 3:
                user_name = parts[1]
                item_name = parts[2]
            elif len(parts) == 2:
                user_name = parts[1]
                item_name = "greet1"

            await message.channel.send(f"Hello, {user_name}")
            
            if item_name in gif_names:
                # sending the correct gif 
                await message.channel.send(gif_dict[item_name], delete_after=SLEEP_TIME)
            elif item_name in img_names:
                # sending the correct image
                await message.channel.send(img_dict[item_name], delete_after=SLEEP_TIME)
            elif item_name in vid_names:
                # sending the correct video
                await message.channel.send(vid_dict[item_name], delete_after=SLEEP_TIME)
            else:
                await message.channel.send(f"There is no '{item_name}' in storage. ")
                await message.channel.send("Use `-list ITEM_TYPE` to get the list of names.")
        except:
            await message.channel.send(f"Invalid. Correct Syntax: `{initial}greet USERNAME NAME`")

    # adds items based on their type
    elif message.content.startswith(f"{initial}add"):
        try:
            # extracing the data for the message
            parts = message.content.split(' ')
            item_type = parts[1].upper()
            item_name = parts[2]
            link = parts[3]

            if item_type in TYPES:
                # getting the correct dictionary
                dictionary = get_dict(item_type)
                # adding the items to the dictionary
                dictionary.update({item_name: link})

                # dumping the whole dict in a string
                updated = json.dumps(dictionary, ensure_ascii=False)
                
                # saving the data in the .env file
                dotenv.set_key(".env", item_type, updated)
                
                await message.channel.send(f"{item_type}: {item_name} added successfully.")
            else:
                await message.channel.send(f"Type not found. Available types are: {TYPES}")
        except Exception as error:
            print(error)
            await message.channel.send(f"Error. Correct Syntax: `{initial}add TYPE NAME LINK`")

    # removes items based on their type
    elif message.content.startswith(f"{initial}rmv"):
        try:
            # extracing the data for the message
            parts = message.content.split(' ')
            item_type = parts[1].upper()
            item_name = parts[2]

            # getting the correct dictionary
            dictionary = get_dict(item_type)
            # getting the keys from dictionary and converting it to a list
            keys = list(dictionary.keys())

            # checking if the item actually exists
            if item_type in TYPES and item_name in keys:
                # removing the item from the dictionary
                dictionary.pop(item_name)

                # dumping the whole dict in a string
                updated = json.dumps(dictionary, ensure_ascii=False)

                # adding the items to the dictionary
                dotenv.set_key(".env", item_type, updated)
                
                await message.channel.send(f"{item_type}: {item_name} removed successfully.")
            else:
                if item_type not in TYPES:
                    await message.channel.send(f"Type not found. Available types are: {TYPES}")
                else:
                    await message.channel.send(f"{item_name} not found. Available names are: {keys}")
        except:
            await message.channel.send(f"Error. Correct Syntax: `{initial}rmv TYPE NAME`")

    # changes the .env data as per user request
    elif message.content.startswith(f"{initial}set"):
        try:
            # extracting the data from the message
            parts = message.content.split(' ')
            variable = parts[1]
            value = parts[2]

            # adding it to the dotenv file
            dotenv.set_key(f"{message.guild.id}.env", variable, value)

            await message.channel.send("Presence Update Channel set successfully.")
        except:
            await message.channel.send(f"Error. Correct Syntax: `{initial}set VARIABLE VALUE`")

    # replying with quotes
    elif message.content.startswith(f"{initial}randomline"):
        try:
            # extracting the data from user message
            parts = message.content.split(' ')
            item_name = parts[1]
            file_name = item_name + ".txt"

            if file_name in QUOTES:
                # since Bengali alphabet is in unicode, we need to open the file in unicode
                with open(file_name, 'r', encoding="utf-8") as file:
                    lines = file.readlines()
            
                    # sending a random line from the user's desired type
                    await message.channel.send(lines[random.randint(0, (len(lines)-1))])
            else:
                await message.channel.send(f"{item_name} not found. Available files are: {QUOTES}")
        except:
            await message.channel.send(f"Invalid. Correct Syntax: `{initial}randomline quran/sunnah/quote`")

    # replying to item requests
    elif message.content.startswith(';'):
        try:
            # extracting the item_name from the message
            item_name = message.content.replace(';', '')

            # if the input is null, then create an Error
            if item_name == "":
                Exception
            elif item_name in gif_names:
                # sending the correct gif 
                await message.channel.send(gif_dict[item_name], delete_after=SLEEP_TIME)
            elif item_name in img_names:
                # sending the correct image
                await message.channel.send(img_dict[item_name], delete_after=SLEEP_TIME)
            elif item_name in vid_names:
                # sending the correct video
                await message.channel.send(vid_dict[item_name], delete_after=SLEEP_TIME)
            else:
                await message.channel.send(f"There is no '{item_name}' in storage. ")
                await message.channel.send("Use `-list ITEM_TYPE` to get the list of names.")
        except:
            await message.channel.send(f"Invalid prompt! Correct syntax: `';'ITEM_NAME`")

@client.event
# called when a member of the server changes their activity
# before and after represents the member that has changed presence;
async def on_presence_update(before, after):
    # getting the channel id
    channel = client.get_channel(presence_update_channel_id)

    # prevents replying to bot's presence update
    # doesn't update presence if the presence_update_channel is none
    if not after.bot and int(presence_update_channel_id) != 0:
        old_status = str(before.status)
        new_status = str(after.status)

        # if the user comes online
        if old_status == "offline" and new_status != "offline":
            # sends a greeting message
            await channel.send(f"Welcome back, {after.name}.")
        # if the user goes offline
        elif old_status != "offline" and new_status == "offline":     
            await channel.send(f"Bye, {after.name}")


# starts the bot
client.run(BOT_TOKEN)