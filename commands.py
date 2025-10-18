import os, json, random
import dotenv, discord
import pain_au_chocolat
from discord.ext import commands

# loading the .env file
dotenv.load_dotenv(".env")

# loading the dictionary into json format
gif_dict = json.loads(os.getenv("GIF"))
img_dict = json.loads(os.getenv("IMG"))
vid_dict = json.loads(os.getenv("VID"))

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = self.bot.command_prefix
        self.sleep_time = int(os.getenv("SLEEP_TIME"))
        self.TYPES = os.getenv("TYPE").split(',')

    @commands.command()
    async def echo(self, ctx, *, message: str=''):
        try:
            if message == '': 
                raise Exception

            await ctx.send(f"You said: {message}")
        except:
            await ctx.send(f"Invalid command. Correct Syntax: `{self.prefix}echo MESSAGE`")

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f"Good Day, {ctx.author.mention}. Hope you are having a fantastic day. ")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Ping: {round(self.bot.latency * 1000)} ms. ")

    @commands.command()
    async def status(self, ctx):
        await ctx.send(f"{self.bot.user} operational. ")

    @commands.command(name="help")
    async def help_messages(self, ctx):

        embed = discord.Embed(
            title="🤖 Bot Help Menu",
            description="Here are all available commands:",
            color=0x00ff00
        )

        # adding the general commands
        embed.add_field(
            name="\n📝 General Commands: ",
            value=f"`{self.prefix}echo` - Echoes what you say.\n"
            f"`{self.prefix}hello` - Greets the user.\n"
            f"`{self.prefix}ping` - Returns the latency of the BOT in milliseconds.\n"
            f"`{self.prefix}status` - Returns the status of the bot.\n",
            inline=False
        )

        # adding the complex commands
        embed.add_field(
            name="\n🧩 Complex Commands (Takes Arguments): ",
            value=f"`;ITEM_NAME` - Returns gif/image/video of the given name if the item was added.\n"
            f"`{self.prefix}del number_of_messages_to_delete` - Deletes the number of messages given.\n"
            f"`{self.prefix}list ITEM_TYPE` - Returns the list of gif/image/video names.\n"
            f"`{self.prefix}greet USERNAME NAME` - Greets the given username with a gif/image/video.\n"
            f"`{self.prefix}reddit SUBREDDIT_NAME` - Returns gif or images from subreddit.\n"
            f"`{self.prefix}add TYPE NAME LINK` - Adds gif/image/video for later use.\n"
            f"`{self.prefix}rmv TYPE NAME` - Removes gif/image/video of the given name from the storage.\n"
            f"`{self.prefix}set VARIABLE VALUE` - Sets the value of the BOT config variable to the given value.(Must be used with caution.)\n"
            f"`{self.prefix}random-line quran/sunnah/quote` - Returns a random line from the given file.",
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
            await ctx.send(f"Invalid command. Correct Syntax: `{self.prefix}del number_of_messages_to_delete`")

    @commands.command(name="list")
    async def list_item(self, ctx, *, message: str = ""):
        try:
            if message == '':
                raise Exception

            item_type = message.upper()

            # proceeding if the given type is valid
            if item_type in self.TYPES:
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
            await ctx.send(f"Invalid command. Correct Syntax: `{self.prefix}list ITEM_NAME`")

    @commands.command()
    async def greet(self, ctx, *, message: str = ""):
        try:
            if message == '':
                raise Exception

            # extracting the data for the message
            parts = message.split(' ')
            user_name = parts[0]
            item_name = parts[1]

            # sending the correct link based on their type
            if item_name in gif_dict.keys():
                await ctx.send(f"Hello, {user_name}")
                await ctx.send(gif_dict[item_name], delete_after=self.sleep_time)
            elif item_name in img_dict.keys():
                await ctx.send(f"Hello, {user_name}")
                await ctx.send(img_dict[item_name], delete_after=self.sleep_time)
            elif item_name in vid_dict.keys():
                await ctx.send(f"Hello, {user_name}")
                await ctx.send(vid_dict[item_name], delete_after=self.sleep_time)
            # if the item_name is not found
            else:
                await ctx.send(f"There is no '{item_name}' in storage. ")
                await ctx.send("Use `-list ITEM_TYPE` to get the list of names.")
        except:
            await ctx.send(f"Invalid. Correct Syntax: `{self.prefix}greet USERNAME NAME`")

    @commands.command()
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
                await ctx.send(submission.url, delete_after=self.sleep_time)
            else:
                await ctx.send(f"{submission.title} \nBy: {submission.author}")
                await ctx.send(submission.url)
        except:
            await ctx.send(f"Invalid. Correct Syntax: `{self.prefix}reddit SUBREDDIT_NAME`")

    @commands.command()
    async def add(self, ctx, *, message: str = ""):
        try:
            if message == "":
                raise Exception

            # extracting the data for the message
            parts = message.split(' ')

            item_type = parts[0].upper()
            item_name = parts[1]
            link = parts[2]

            if item_type in self.TYPES:
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
                    f"Type not found. Available types are: {self.TYPES}"
                )
        except Exception:
            await ctx.send(
                f"Error. Correct Syntax: `{self.prefix}add TYPE NAME LINK`"
            )

    @commands.command()
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
            if item_type in self.TYPES and item_name in keys:
                # removing the item from the dictionary
                dictionary.pop(item_name)

                # dumping the whole dict in a string
                updated = json.dumps(dictionary, ensure_ascii=False)

                # adding the items to the dictionary
                dotenv.set_key(".env", item_type, updated)

                await ctx.send(f"{item_type}: {item_name} removed successfully.")
            else:
                if item_type not in self.TYPES:
                    await ctx.send(f"Type not found. Available types are: {self.TYPES}")
                else:
                    await ctx.send(f"{item_name} not found. Available names are: {keys}")
        except:
            await ctx.send(f"Error. Correct Syntax: `{self.prefix}rmv TYPE NAME`")

    @commands.command()
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
                case "PREFIX":
                    self.prefix = value
                    shouldUpdate = True
                case "SLEEP_TIME":
                    self.sleep_time = int(value)
                    shouldUpdate = True
                case "SEARCH_LIMIT":
                    shouldUpdate = True
                case "NSFW_ALLOWED":
                    # parsing the user input
                    if value.lower() == "true" :
                        value = '1'
                    elif value.lower() == "false":
                        value = '0'
                    else:
                        ValueError
                    shouldUpdate = True

            if shouldUpdate:
                # updating the variable in the .env file
                dotenv.set_key(f".env", variable, value)

                await ctx.send(f"{variable} set to {value} successfully.")
            else:
                await ctx.send("Variable not found. Available variables are: PRESENCE_UPDATE_CHANNEL_ID, PREFIX, SLEEP_TIME, SEARCH_LIMIT, NSFW_ALLOWED") 
        except:
            await ctx.send(f"Error. Correct Syntax: `{self.prefix}set VARIABLE VALUE`")

    @commands.command()
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
            await ctx.send(f"Invalid. Correct Syntax: `{self.prefix}random-line quran/sunnah/quote`")

    async def send_item(self, message):
        try:
            item_name = message.content.replace(';', '')

                # if the input is null, then create an Error
            if item_name in gif_dict.keys():
                # sending the correct gif
                await message.channel.send(gif_dict[item_name], delete_after=self.sleep_time)
            elif item_name in img_dict.keys():
                # sending the correct image
                await message.channel.send(img_dict[item_name], delete_after=self.sleep_time)
            elif item_name in vid_dict.keys():
                    # sending the correct video
                    await message.channel.send(vid_dict[item_name], delete_after=self.sleep_time)
            else:
                await message.channel.send(f"There is no '{item_name}' in storage. ")
                await message.channel.send(
                    f"Use `{self.prefix}list ITEM_TYPE` to get the list of names."
                )
        except:
            await message.channel.send(f"Invalid prompt! Correct syntax: `;ITEM_NAME`")


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

async def setup(bot):
    await bot.add_cog(BotCommands(bot))
