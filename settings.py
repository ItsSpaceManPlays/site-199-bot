import pathlib
import os
import logging
from logging.config import dictConfig
from dotenv import load_dotenv
import discord
import json


load_dotenv()

DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")
with open("data/role.json", "r+") as f:
    COMMAND_PERMISSION_ROLE_NAME = json.load(f)["role"]

def check_role_permission(guild: discord.Guild, member: discord.Member):
    pRole: discord.Role = discord.utils.get(guild.roles, name=COMMAND_PERMISSION_ROLE_NAME)
    if member.top_role.position >= pRole.position:
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