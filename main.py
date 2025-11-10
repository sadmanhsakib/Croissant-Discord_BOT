import discord
import config, pain_au_chocolat
from discord.ext import commands
from database import db

# for running the bot as a web
from keep_alive import keep_alive

keep_alive()

# giving the permissions
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.messages = True
intents.members = True
intents.guilds = True


async def get_prefix(bot, message):
    # returning the prefix for this server
    return config.prefix_cache[message.guild.id]


bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)
cog = None

@bot.event
# when the bot starts
async def on_ready():
    global cog

    # connecting to the database
    await db.connect()
    # loading the data from the database
    await config.load_all_data()

    # authenticating the reddit api
    await pain_au_chocolat.authenticate()

    # loading the command script
    await bot.load_extension("bot_commands")

    # importing and creating a cog object
    from bot_commands import BotCommands
    cog = BotCommands(bot)

    # this won't actually start until before_scheduler completes
    # the scheduler only starts after wait_until_ready() completes
    # scheduler is a background task, not a coroutine, so no need to await
    cog.scheduler.start()

    # prints a message in console when ready
    print(f"✅Logged in as: {bot.user}")


@bot.event
async def on_guild_join(guild):
    config.prefix_cache.update({guild.id: "-"})

    # setting the default values
    await config.set_default(guild.id)
    # loading the data from the database
    await config.load_all_data()

    # getting the general channel of the server that the BOT just joined
    channel = discord.utils.get(guild.text_channels, name="general")

    if channel and channel.permissions_for(guild.me).send_messages:
        # sending greeting messages
        await channel.send("Thank you for adding Croissant!")
        await channel.send(f"Type: `{config.prefix_cache[guild.id]}help` to get the command list.")
        await channel.send("It's recommended for to try all the commands at least for once. ")
        await channel.send(f"You can learn more about the BOT from here: {config.REPO_URL}")

        # instructing the users on how to set up the channel
        await channel.send("By default, this bot sends greeting to members when they come online and goes offline. ")
        await channel.send(
            f"If you want to use this feature, use the '{config.prefix_cache[guild.id]}set<space>PRESENCE_UPDATE_CHANNEL_ID<space>channel_id' command. "
        )
        await channel.send("If you don't want to use this feature, you can ignore it. ")

@bot.event
# when the user sends a message in server
async def on_message(message):
    # prevents the bot from replying on its own messages
    if message.author == bot.user:
        return
    
    # reacting to hate messages
    if message.content.lower().__contains__("clanker"):
        await message.add_reaction("💢")
    # replying to item requests
    if message.content.__contains__(';'):
        item_names = []
        parts = message.content.split(' ')
            
        # for every word in the message
        for part in parts: 
            if part[0] == ';':
                try:
                    # checking if the item name is an actual request
                    if part[1] == ' ':
                        return
                    else:
                        # removing the ; from the item name
                        item_names.append(part[1:])
                except IndexError:  
                    return
        
        if item_names:
            # sending items if applicable
            await cog.send_item(item_names, message.channel)

    # processing the commands
    await bot.process_commands(message)


@bot.event
# called when a member of the server changes their activity
# before and after represents the member that has changed presence;
async def on_presence_update(before, after):
    presence_update_channel_id = config.notify_channel_id_cache[after.guild.id]
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
bot.run(config.BOT_TOKEN)
