# THIS IS A TEMPLATE IN CASE NEEDED FOR EXPANSION, IT ALSO HAS A GIF COMMAND SAMPLE

# import discord
# from discord.ext import commands
# from discord import app_commands
# 
# class Template(commands.Cog):
#   def __init__(self,bot):
#     self.bot = bot
#     
#   GIFS = {}  # FILL {"gif_name": "url"} LATER
# 
#   @commands.command(name="gif")
#   async def gif_legacy(self, ctx: commands.Context, gif_name: str):
#       gif_url = GIFS.get(gif_name)
#       if gif_url:
#           await ctx.send(gif_url)
#       else:
#           await ctx.send("No GIFs available yet.")
#   
#   @app_commands.command(name="gif", description="Send a GIF by name")
#   async def gif_slash(self, interaction: discord.Interaction, gif_name: str):
#       gif_url = GIFS.get(gif_name)
#       if gif_url:
#           await interaction.response.send_message(gif_url)
#       else:
#           await interaction.response.send_message("No GIFs available yet.")
#           
# async def setup(bot):
#   await bot.add_cog(Template(bot))