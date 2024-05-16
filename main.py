import settings
import discord
from discord.ext import commands
from discord import app_commands
import json

logger = settings.logging.getLogger("bot")

def run():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="/", intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

        # load extensions
        await bot.load_extension("cmds.events")
        logger.info("Loaded extension cmds.events")
        
        # discord.Object(id=1238923068651343882)
        # bot.tree.copy_global_to(guild=discord.Object(id=1238923068651343882))
        # await bot.tree.sync(guild=discord.Object(id=1238923068651343882))
        await bot.tree.sync()
        logger.info("Synced command tree")


    @bot.tree.command(name="ping", description="Ping the bot")
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! `{round(bot.latency * 1000)}ms`")

    @bot.tree.command(name="permissionrole", description="Set the role needed to use the bot")
    @commands.has_permissions(administrator=True)
    async def setrole(interaction: discord.Interaction, role: discord.Role):
        settings.COMMAND_PERMISSION_ROLE_NAME = role.name
        with open("data/role.json", "w+") as f:
            json.dump({"role": role.name}, f)
        await interaction.response.send_message(f"Changed role to {role.name}")

    bot.run(settings.DISCORD_API_SECRET, log_handler=None, root_logger=True)

if __name__ == "__main__":
    run()