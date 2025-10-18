import os
import discord, dotenv
from discord.ext import commands
import pain_au_chocolat

# loading the universal .env file
dotenv.load_dotenv(".env")

# giving the permissions
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.messages = True
intents.members = True
intents.guilds = True

# getting the universal data from the .env files
BOT_TOKEN = "MTQyNTcxMTA2OTI2NzIzNDkxMg.GFi-Tg.Iwa15PFrCdpSpyKnvTlEAZJonkZCiu7tQSy_eY"
# BOT_TOKEN = os.getenv("BOT_TOKEN")
REPO_URL = os.getenv("REPO_URL")

# getting the server specific data from their .env files
prefix = os.getenv("PREFIX")

bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)

TIME_FORMAT = "%Y-%m-%d -> %H:%M:%S"

@bot.event
# when the bot starts
async def on_ready():
    # authenticating the reddit api
    await pain_au_chocolat.authenticate()

    # loading the command script
    await bot.load_extension("commands")

    # prints a message in console when ready
    print(f"✅Logged in as: {bot.user}")


@bot.event
async def on_guild_join(guild):
    # getting the general channel of the server that the BOT just joined
    channel = discord.utils.get(guild.text_channels, name="general")

    if channel and channel.permissions_for(guild.me).send_messages:
        # sending greeting messages
        await channel.send("Thank you for adding Croissant!")
        await channel.send(f"Type: `{prefix}help` to get the command list.")
        await channel.send("It's recommended for to try all the commands at least for once. ")
        await channel.send(f"You can learn more about the BOT from here: {REPO_URL}")

        # instructing the users on how to set up the channel
        await channel.send("By default, this bot sends greeting to members when they come online and goes offline. ")
        await channel.send(
            f"If you want to use this feature, use the '{prefix}set<space>PRESENCE_UPDATE_CHANNEL_ID' command. "
        )
        await channel.send("If you don't want to use this feature, you can ignore it. ")

@bot.event
# when the user sends a message in server
async def on_message(message):
    # prevents the bot from replying on its own messages
    if message.author == bot.user:
        return
    # reacting to hate messages
    elif message.content.lower().__contains__("clanker"):
        await message.add_reaction("💢")
    # replying to item requests
    elif message.content.startswith(';'):
        from commands import BotCommands
        cog = BotCommands(bot)
        await cog.send_item(message)
        
    # processing the commands
    await bot.process_commands(message)
    

@bot.event
# called when a member of the server changes their activity
# before and after represents the member that has changed presence;
async def on_presence_update(before, after):
    # getting the channel id from the .env file
    dotenv.load_dotenv(".env", override=True)
    presence_update_channel_id = int(os.getenv("PRESENCE_UPDATE_CHANNEL_ID"))
    channel = bot.get_channel(presence_update_channel_id)

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
bot.run(BOT_TOKEN)
