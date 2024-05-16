import discord
from discord import app_commands
from discord.ext import commands

class MyGroup(app_commands.Group):
    @app_commands.command(name="create")
    async def create(self, interaction: discord.Interaction):
        await interaction.response.send_message("Test")

    @app_commands.command(name="remove")
    async def remove(self, interaction: discord.Interaction):
        await interaction.response.send_message("Test")

    @app_commands.command(name="list")
    async def list(self, interaction: discord.Interaction):
        await interaction.response.send_message("cool list of events")

async def setup(bot: commands.Bot):
    bot.tree.add_command(MyGroup(name="events", description="Events"))