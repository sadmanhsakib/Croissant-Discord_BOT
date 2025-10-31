import os, json, random
import discord
import pain_au_chocolat, config
from discord.ext import commands
from database import db

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
            f"`{config.prefix}ping` - Returns the latency of the BOT in milliseconds.\n"
            f"`{config.prefix}list` - Returns all the available item names from the storage.\n",
            inline=False
        )

        # adding the complex commands
        embed.add_field(
            name="\n🧩 Complex Commands (Takes Arguments): ",
            value=f"`;ITEM_NAME` - Returns gif/image/video of the given name if the item was added.\n"
            f"`{config.prefix}del number_of_messages_to_delete` - Deletes the number of messages given.\n"
            f"`{config.prefix}greet USERNAME ITEM_NAMES(for multiple items, separate each with space)` - Greets the given username with a gif/image/video.\n"
            f"`{config.prefix}reddit SUBREDDIT_NAME` - Returns gif or images from subreddit.\n"
            f"`{config.prefix}add NAME LINK` - Adds gif/image/video for later use.\n"
            f"`{config.prefix}rmv NAME` - Removes gif/image/video of the given name from the storage.\n"
            f"`{config.prefix}set VARIABLE VALUE` - Sets the value of the BOT config prefixlue.(Must be used with caution.)\n"
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
    async def list_item(self, ctx):
        try:
            await ctx.send(f"Available items in storage are: {config.storage_dict.keys()}")
        except:
            await ctx.send(f"Invalid command. Correct Syntax: `{config.prefix}list`")

    @commands.command(name="greet")
    async def greet(self, ctx, *, message: str = ''):
        try:
            if message == '':
                raise Exception

            # extracting the data for the message
            parts = message.split(' ')
            user_name = parts[0]
            item_names = []

            # getting the item names
            for part in parts[1:]:
                if part == "":
                    continue
                item_names.append(part)

            # sending the messages
            ctx.send(f"Hello {user_name}")
            self.send_item(item_names, ctx)
        except:
            await ctx.send(f"Invalid. Correct Syntax: `{config.prefix}greet USERNAME ITEM_NAME(for multiple items, separate each with space)`")

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

            # removes the meme after delete_after if the url is NSFW
            if submission.is_nsfw:
                await ctx.send(f"{submission.title} \nBy: {submission.author}")
                await ctx.send(submission.url, delete_after=config.delete_after if config.delete_after != 0 else None)
            else:
                await ctx.send(f"{submission.title} \nBy: {submission.author}")
                await ctx.send(submission.url)
        except:
            await ctx.send(f"Invalid. Correct Syntax: `{config.prefix}reddit SUBREDDIT_NAME`")

    @commands.command(name="add")
    async def add(self, ctx, *, message: str = ''):
        try:
            if message == '':
                raise Exception

            # extracting the data for the message
            parts = message.split(' ')
            item_name = parts[0]
            item_url = parts[1]

            # adding the item to the dictionary
            config.storage_dict.update({item_name: item_url})
            # dumping the whole dict in a string for saving
            updated = json.dumps(config.storage_dict, ensure_ascii=False)
            # updating the database
            await db.set_variable("STORAGE_DICT", updated)

            await ctx.send(f"{item_name} added successfully.")

        except Exception:
            await ctx.send(
                f"Error. Correct Syntax: `{config.prefix}add NAME LINK`"
            )

    @commands.command(name="rmv")
    async def rmv(self, ctx, *, message: str = ''):
        try:
            if message == '':
                raise Exception

            # extracting the data for the message
            parts = message.split(' ')
            item_name = parts[0]

            # checking if the item is in the dictionary
            if item_name not in config.storage_dict.keys():
                await ctx.send(f"There is no '{item_name}' in storage. ")
                await ctx.send(f"Use `{config.prefix}list` to get the list of names.")
            else:
                # removing the item from the dictionary
                config.storage_dict.pop(item_name)
                # dumping the whole dict in a string for saving
                updated = json.dumps(config.storage_dict, ensure_ascii=False)
                # updating the database
                await db.set_variable("STORAGE_DICT", updated)

                await ctx.send(f"{item_name} removed successfully.")
        except:
            await ctx.send(f"Error. Correct Syntax: `{config.prefix}rmv NAME`")

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
                    shouldUpdate = True
                    config.presence_update_channel_id = int(value)
                case "PREFIX":
                    shouldUpdate = True
                    config.prefix = value
                case "DELETE_AFTER":
                    shouldUpdate = True
                    config.delete_after = int(value)
                case "SEARCH_LIMIT":
                    shouldUpdate = True
                    config.search_limit = int(value)
                case "NSFW_ALLOWED":
                    # parsing the user input
                    if value.lower() == "true" :
                        value = True
                    elif value.lower() == "false":
                        value = False
                    else:
                        await ctx.send("Invalid value for NSFW_ALLOWED. Acceptable values are: true, false")
                        return
                    shouldUpdate = True
                    config.nsfw_allowed = value

            if shouldUpdate:
                # updating the variable in the .env file
                await db.set_variable(variable, str(value))

                await ctx.send(f"{variable} set to {value} successfully.")
            else:
                await ctx.send(
                    "Variable not found. Available variables are: PREFIX, DELETE_AFTER, SEARCH_LIMIT, NSFW_ALLOWED, PRESENCE_UPDATE_CHANNEL_ID"
                )
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

    async def send_item(self, item_names, message_channel):
        for item_name in item_names:
            # sending the correct link for each type
            if item_name in config.storage_dict.keys():
                await message_channel.send(config.storage_dict[item_name], delete_after = config.delete_after if config.delete_after != 0 else None)
            else:
                await message_channel.send(f"There is no '{item_name}' in storage. Use `{config.prefix}list` to get the list of names.")

async def setup(bot):
    await bot.add_cog(BotCommands(bot))
