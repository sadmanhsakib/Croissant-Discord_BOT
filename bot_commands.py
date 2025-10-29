import os, json, random
import dotenv, discord
import pain_au_chocolat, config
from discord.ext import commands


class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="echo")
    async def echo(self, ctx, *, message: str=''):
        try:
            if message == '': 
                raise Exception

            await ctx.send(f"You said: {message}")
        except:
            await ctx.send(f"Invalid command. Correct Syntax: `{config.prefix}echo MESSAGE`")

    @commands.command(name="hello")
    async def hello(self, ctx):
        await ctx.send(f"Good Day, {ctx.author.mention}. Hope you are having a fantastic day. ")

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f"Ping: {round(self.bot.latency * 1000)} ms. ")

    @commands.command(name="status")
    async def status(self, ctx):
        await ctx.send(f"{self.bot.user} operational. ")

    @commands.command(name="help")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="🤖 Bot Help Menu",
            description="Here are all available commands:",
            color=0x00ff00
        )

        # adding the general commands
        embed.add_field(
            name="\n📝 General Commands: ",
            value=f"`{config.prefix}echo` - Echoes what you say.\n"
            f"`{config.prefix}hello` - Greets the user.\n"
            f"`{config.prefix}status` - Returns the status of the bot.\n"
            f"`{config.prefix}ping` - Returns the latency of the BOT in milliseconds.\n",
            inline=False
        )

        # adding the complex commands
        embed.add_field(
            name="\n🧩 Complex Commands (Takes Arguments): ",
            value=f"`;ITEM_NAME` - Returns gif/image/video of the given name if the item was added.\n"
            f"`{config.prefix}del number_of_messages_to_delete` - Deletes the number of messages given.\n"
            f"`{config.prefix}list ITEM_TYPE` - Returns the list of gif/image/video names.\n"
            f"`{config.prefix}greet USERNAME NAME` - Greets the given username with a gif/image/video.\n"
            f"`{config.prefix}reddit SUBREDDIT_NAME` - Returns gif or images from subreddit.\n"
            f"`{config.prefix}add TYPE NAME LINK` - Adds gif/image/video for later use.\n"
            f"`{config.prefix}rmv TYPE NAME` - Removes gif/image/video of the given name from the storage.\n"
            f"`{config.prefix}set VARIABLE VALUE` - Sets the value of the BOT config variable to the given value.(Must be used with caution.)\n"
            f"`{config.prefix}random-line quran/sunnah/quote` - Returns a random line from the given file.",
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(name="del")
    async def delete_messages(self, ctx, *, message: str = ''):
        try:
            if message == '':
                raise Exception

            # extracting the data from the message
            amount = int(message)
            # +1 to remove the command itself
            await ctx.channel.purge(limit=amount+1)
        except:
            await ctx.send(f"Invalid command. Correct Syntax: `{config.prefix}del number_of_messages_to_delete`")

    @commands.command(name="list")
    async def list_item(self, ctx, *, message: str = ""):
        try:
            if message == '':
                raise Exception

            item_type = message.upper()

            # proceeding if the given type is valid
            if item_type in config.TYPES:
                # getting the correct dictionary
                dictionary = get_dict(item_type)
                # getting the keys from dictionary and converting it to a list
                keys = list(dictionary.keys())

                # checking if the keys are empty or not
                if keys != []:
                    await ctx.send(f"```Available {item_type}s are:\n{keys}```")
                else:
                    await ctx.send("Empty.")
            else:
                await ctx.send(f"{item_type} not found.")
        except:
            await ctx.send(f"Invalid command. Correct Syntax: `{config.prefix}list ITEM_NAME`")

    @commands.command(name="greet")
    async def greet(self, ctx, *, message: str = ""):
        try:
            if message == '':
                raise Exception

            # extracting the data for the message
            parts = message.split(' ')
            user_name = parts[0]
            item_name = parts[1]

            # sending the correct link based on their type
            if item_name in config.gif_dict.keys():
                await ctx.send(f"Hello, {user_name}")
                await ctx.send(
                    config.gif_dict[item_name], delete_after=config.sleep_time if config.sleep_time != 0 else None
                    )
            elif item_name in config.img_dict.keys():
                await ctx.send(f"Hello, {user_name}")
                await ctx.send(
                    config.img_dict[item_name], delete_after=config.sleep_time if config.sleep_time != 0 else None
                    )
            elif item_name in config.vid_dict.keys():
                await ctx.send(f"Hello, {user_name}")
                await ctx.send(
                    config.vid_dict[item_name], delete_after=config.sleep_time if config.sleep_time != 0 else None
                    )
            # if the item_name is not found
            else:
                await ctx.send(f"There is no '{item_name}' in storage. ")
                await ctx.send("Use `-list ITEM_TYPE` to get the list of names.")
        except:
            await ctx.send(f"Invalid. Correct Syntax: `{config.prefix}greet USERNAME NAME`")

    @commands.command(name="reddit")
    async def reddit(self, ctx, *, message: str = ""):
        try:
            if message == '':
                raise Exception

            # creating a object
            fetcher = pain_au_chocolat.Fetch()

            # extracting the data from the message
            parts = message.split(' ')

            if len(parts) != 1:
                raise Exception
            subreddit_name = message

            # getting the item data
            submission = await fetcher.get_submission(subreddit_name)

            # giving the error message for permission error
            if type(submission) == str:
                await ctx.send(submission)
                return

            # removes the meme after sleep_time if the url is NSFW
            if submission.is_nsfw:
                await ctx.send(f"{submission.title} \nBy: {submission.author}")
                await ctx.send(submission.url, delete_after=config.sleep_time)
            else:
                await ctx.send(f"{submission.title} \nBy: {submission.author}")
                await ctx.send(submission.url)
        except:
            await ctx.send(f"Invalid. Correct Syntax: `{config.prefix}reddit SUBREDDIT_NAME`")

    @commands.command(name="add")
    async def add(self, ctx, *, message: str = ""):
        try:
            if message == "":
                raise Exception

            # extracting the data for the message
            parts = message.split(' ')

            item_type = parts[0].upper()
            item_name = parts[1]
            link = parts[2]

            if item_type in config.TYPES:
                # getting the correct dictionary
                dictionary = get_dict(item_type)
                # adding the items to the dictionary
                dictionary.update({item_name: link})

                # dumping the whole dict in a string
                updated = json.dumps(dictionary, ensure_ascii=False)

                # saving the data in the .env file
                dotenv.set_key(".env", item_type, updated)

                await ctx.send(
                    f"{item_type}: {item_name} added successfully."
                )
            else:
                await ctx.send(
                    f"Type not found. Available types are: {config.TYPES}"
                )
        except Exception:
            await ctx.send(
                f"Error. Correct Syntax: `{config.prefix}add TYPE NAME LINK`"
            )

    @commands.command(name="rmv")
    async def rmv(self, ctx, *, message: str = ""):
        try:
            if message == "":
                raise Exception

            # extracting the data for the message
            parts = message.split(' ')
            item_type = parts[0].upper()
            item_name = parts[1]

            # getting the correct dictionary
            dictionary = get_dict(item_type)
            # getting the keys from dictionary and converting it to a list
            keys = list(dictionary.keys())

            # checking if the item actually exists
            if item_type in config.TYPES and item_name in keys:
                # removing the item from the dictionary
                dictionary.pop(item_name)

                # dumping the whole dict in a string
                updated = json.dumps(dictionary, ensure_ascii=False)

                # adding the items to the dictionary
                dotenv.set_key(".env", item_type, updated)

                await ctx.send(f"{item_type}: {item_name} removed successfully.")
            else:
                if item_type not in config.TYPES:
                    await ctx.send(f"Type not found. Available types are: {config.TYPES}")
                else:
                    await ctx.send(f"{item_name} not found. Available names are: {keys}")
        except:
            await ctx.send(f"Error. Correct Syntax: `{config.prefix}rmv TYPE NAME`")

    @commands.command(name="set")
    async def set(self, ctx, *, message: str = ""):
        try:
            if message == "":
                raise Exception

            # extracting the data for the message
            parts = message.split(' ')
            variable = parts[0].upper()
            value = parts[1]

            shouldUpdate = False

            # checking for each case which variable to update
            match variable:
                case "PRESENCE_UPDATE_CHANNEL_ID":
                    config.presence_update_channel_id = int(value)
                    shouldUpdate = True
                case "PREFIX":
                    config.prefix = value
                    shouldUpdate = True
                case "SLEEP_TIME":
                    config.sleep_time = int(value)
                    shouldUpdate = True
                case "SEARCH_LIMIT":
                    config.search_limit = int(value)
                    shouldUpdate = True
                case "NSFW_ALLOWED":
                    # parsing the user input
                    if value.lower() == "true" :
                        value = "True"
                    elif value.lower() == "false":
                        value = "False"
                    else:
                        ValueError
                    shouldUpdate = True
                    config.nsfw_allowed = value

            if shouldUpdate:
                # updating the variable in the .env file
                dotenv.set_key(f".env", variable, value)

                await ctx.send(f"{variable} set to {value} successfully.")
            else:
                await ctx.send("Variable not found. Available variables are: PRESENCE_UPDATE_CHANNEL_ID, PREFIX, SLEEP_TIME, SEARCH_LIMIT, NSFW_ALLOWED") 
        except:
            await ctx.send(f"Error. Correct Syntax: `{config.prefix}set VARIABLE VALUE`")

    @commands.command(name="random-line")
    async def random_line(self, ctx, *, message: str = ""):
        try:
            if message == "":
                raise Exception

            # parsing the user input
            item_name = message.lower()
            file_name = item_name + ".txt"

            QUOTES = ["quran.txt", "sunnah.txt", "quote.txt"]
            folder = "assets/"

            if file_name in QUOTES:
                # since Bengali alphabet is in unicode, we need to open the file in unicode
                with open(os.path.join(folder, file_name), 'r', encoding="utf-8") as file:
                    lines = file.readlines()

                    # sending a random line from the user's desired type
                    await ctx.send(lines[random.randint(0, (len(lines)-1))])
            else:
                await ctx.send(f"{item_name} not found. Available files are: {QUOTES}")
        except:
            await ctx.send(f"Invalid. Correct Syntax: `{config.prefix}random-line quran/sunnah/quote`")

    async def send_item(self, item_name, message_channel):
        try:
            # if the input is null, then create an Error
            if item_name in config.gif_dict.keys():
                # sending the correct gif
                await message_channel.send(
                    config.gif_dict[item_name], delete_after=config.sleep_time if config.sleep_time != 0 else None
                )
            elif item_name in config.img_dict.keys():
                # sending the correct image
                await message_channel.send(
                    config.img_dict[item_name], delete_after=config.sleep_time if config.sleep_time != 0 else None
                )
            elif item_name in config.vid_dict.keys():
                # sending the correct video
                await message_channel.send(
                    config.vid_dict[item_name], delete_after=config.sleep_time if config.sleep_time != 0 else None
                )
            else:
                await message_channel.send(f"There is no '{item_name}' in storage. ")
                await message_channel.send(
                    f"Use `{config.prefix}list ITEM_TYPE` to get the list of names."
                )
        except:
            await message_channel.send(
                f"Invalid prompt! Correct syntax: `;ITEM_NAME`"
            )


def get_dict(item_type):
    # finding the right type of dictionary
    match item_type:
        case "GIF":
            dictionary = config.gif_dict
        case "IMG":
            dictionary = config.img_dict
        case "VID":
            dictionary = config.vid_dict
    return dictionary       

async def setup(bot):
    await bot.add_cog(BotCommands(bot))
