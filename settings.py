import pathlib
import os
import logging
from logging.config import dictConfig
from dotenv import load_dotenv
import discord
import json


load_dotenv()

if not os.path.exists("data"):
    os.mkdir("data")

if not os.path.exists("data/role.json"):
    with open("data/role.json", "w+") as f:
        f.write("{\"role\": \"\"}")

DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")
with open("data/role.json", "r+") as f:
    COMMAND_PERMISSION_ROLE_NAME = json.load(f)["role"]

async def check_role_permission(interaction: discord.Interaction):
    pRole: discord.Role = discord.utils.get(interaction.guild.roles, name=COMMAND_PERMISSION_ROLE_NAME)
    if pRole == None:
        alert_embed = discord.Embed(color=0xfca100, title="ALERT", description="No role is configured for the bot (do this by using /permissionsrole [ROLE]), defaulting to administrator permissions")

        await interaction.channel.send(embed=alert_embed)
        if interaction.user.guild_permissions.administrator:
            return True
        else:
            return False

    if interaction.user.top_role.position >= pRole.position:
        return True
    else:
        return False

BASE_DIR = pathlib.Path(__file__).parent

CMDS_DIR = BASE_DIR / "cmds"

LOGGING_CONFIG  = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard": {
            "format": "%(levelname)-10s - %(name)-15s : %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard"
        },
        "console2": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "standard"
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/info.log",
            "mode": "w",
            "formatter": "verbose"
        }
    },
    "loggers": {
        "bot": {
            "handlers": ["console"],
            "level": "INFO",
            "propogate": False
        },
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propogate": False
        }
    }
}

dictConfig(LOGGING_CONFIG)