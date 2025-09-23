import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from keep_alive import keep_alive
from configs import dark_humor_channel_id


# MAKE SURE YOUR TURN ON PRESENCE UPDATES FROM DISCORD DEV PORTAL



intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

class Client(commands.Bot):
  async def setup_hook(self):
    for filename in os.listdir("cogs"):
      if filename.endswith(".py"):
        cog_name = filename[:-3]
        await self.load_extension(f"{"cogs"}.{cog_name}")

    await self.tree.sync()

bot = Client(command_prefix = "-", help_command = None, intents = intents)

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user}")

@bot.event
async def on_presence_update(before: discord.Member, after: discord.Member):
  try:
    if after.bot:
        return

    channel = bot.get_channel(dark_humor_channel_id)
    print(channel.name if channel else "Channel not found")
    if not channel:
        return

    old_status, new_status = str(before.status), str(after.status)

    if old_status == "offline" and new_status != "offline":
        await channel.send(f"Welcome back, {after.display_name}.")
    elif old_status != "offline" and new_status == "offline":
        await channel.send(f"Bye, {after.display_name}.")
  except Exception as e:
    print(e)



# STARTS THE BOT
if __name__ == "__main__":
  keep_alive()
  load_dotenv()
  bot.run(os.getenv('BOT_TOKEN'))