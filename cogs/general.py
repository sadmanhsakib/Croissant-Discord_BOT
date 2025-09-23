import discord
from discord.ext import commands
from discord import app_commands

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def build_help_pages(self):
        pages = []
        for cog_name, cog in self.bot.cogs.items():
            lines = [
                f"**{self.bot.command_prefix}{cmd.name}** - {cmd.help or 'No description provided'}"
                for cmd in cog.get_commands()
                if not cmd.hidden
            ]
            embed = discord.Embed(
                color= 0x0d0d0d,
                title=f"{cog_name} Commands",
                description="\n".join(lines) or "No commands"
            )
            pages.append(embed)
        return pages

    @app_commands.command(name="help", description="Shows list of all commands present")
    async def _help_slash(self, interaction: discord.Interaction):
        pages = await self.build_help_pages()
        await self.paginate(interaction, pages)

    @commands.command(name="help", help="Shows list of all commands present")
    async def _help_legacy(self, ctx: commands.Context):
        pages = await self.build_help_pages()
        await self.paginate(ctx, pages)

    async def paginate(self, origin, pages):
        if not pages:
            if isinstance(origin, commands.Context):
                await origin.send("No commands available.")
            else:
                await origin.response.send_message("No commands available.", ephemeral=True)
            return

        index = 0

        def make_embed(i):
            e = pages[i].copy()
            e.set_footer(text=f"Page {i+1}/{len(pages)}")
            return e

        view = discord.ui.View()

        if len(pages) > 1:
            async def prev_btn_callback(interaction: discord.Interaction):
                nonlocal index
                index = (index - 1) % len(pages)
                await interaction.response.edit_message(embed=make_embed(index), view=view)

            async def nxt_btn_callback(interaction: discord.Interaction):
                nonlocal index
                index = (index + 1) % len(pages)
                await interaction.response.edit_message(embed=make_embed(index), view=view)

            prev_btn = discord.ui.Button(label="◀", style=discord.ButtonStyle.primary)
            prev_btn.callback = prev_btn_callback
            view.add_item(prev_btn)

            nxt_btn = discord.ui.Button(label="▶", style=discord.ButtonStyle.primary)
            nxt_btn.callback = nxt_btn_callback
            view.add_item(nxt_btn)

        if isinstance(origin, commands.Context):
            await origin.send(embed=make_embed(index), view=view if len(pages) > 1 else None)
        else:
            await origin.response.send_message(embed=make_embed(index), view=view if len(pages) > 1 else None)

async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))