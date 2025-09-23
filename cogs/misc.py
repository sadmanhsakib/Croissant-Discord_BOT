import discord
from discord.ext import commands
from discord import app_commands

class Misc(commands.Cog):
  def __init__(self,bot):
    self.bot = bot
    
  async def hello(self,user):
    return f"Good day, {user}. Hope you are having a fantastic day. "
    
  @commands.command(name = "hello", help = "A pleasant greeting from me")
  async def hello_legacy(self,ctx: commands.Context):
    msg = await self.hello(ctx.author)
    await ctx.send(msg)
    
  @app_commands.command(name = "hello", description = "A pleasant greeting from me")
  async def hello_slash(self, interaction: discord.Interaction):
    msg = await self.hello(interaction.user)
    await ctx.response.send_message(msg)
    
  async def ping(self):
    return round(self.bot.latency * 1000)
    
  @commands.command(name = "ping", help = "Check bot's response time")
  async def ping_legacy(self, ctx: commands.Context):
    latency = await self.ping()
    await ctx.send(f"Pong! Latency {latency} ms")
    
  @app_commands.command(name = "ping", description = "Check bot's response time")
  async def ping_slash(self,interaction:discord.Interaction):
    latency = await self.ping()
    await interaction.response.send_message(f"Pong! Latency {latency} ms")
    
async def setup(bot: commands.Bot):
  await bot.add_cog(Misc(bot))