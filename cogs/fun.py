import discord
from discord.ext import commands
from discord import app_commands
import random
from configs import quran_file, sunnah_file, quotes_file

class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def get_random_line(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return random.choice(lines).strip()
        
    @commands.command(name="quran")
    async def quran_legacy(self, ctx: commands.Context):
        await ctx.send(await self.get_random_line(quran_file))

    @commands.command(name="sunnah")
    async def sunnah_legacy(self, ctx: commands.Context):
        await ctx.send(await self.get_random_line(sunnah_file))

    @commands.command(name="quote")
    async def quote_legacy(self, ctx: commands.Context):
        await ctx.send(await self.get_random_line(quotes_file))

    @app_commands.command(name="quran", description="Random Quran line")
    async def quran_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(await self.get_random_line(quran_file))

    @app_commands.command(name="sunnah", description="Random Sunnah line")
    async def sunnah_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(await self.get_random_line(sunnah_file))

    @app_commands.command(name="quote", description="Random motivational quote")
    async def quote_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(await self.get_random_line(quotes_file))

async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))