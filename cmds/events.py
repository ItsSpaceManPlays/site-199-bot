import discord
from discord import app_commands
from discord.ext import commands

import settings

import database
import event
from event import Event

logger = settings.logging.getLogger("bot")

class MyGroup(app_commands.Group):
    @app_commands.command(name="create", description="Create an event")
    async def create(self, interaction: discord.Interaction, event_type: str, event_name: str, event_host: discord.Member):
        logger.info(f"@{interaction.user.display_name} ran create command")
        if not settings.check_role_permission(interaction.guild, interaction.user):
            await interaction.response.send_message("You dont have permission to use this command", ephemeral=True)
            logger.info("They did not have permission to use the command")
            return

        if event_type.lower() != event.EVENT_SSD and event_type.lower() != event.EVENT_SSU:
            await interaction.response.send_message("Please enter a valid event type, e.g. \"ssu\" or \"ssd\"")
            logger.info("They did not enter a valid event type")
            return

        new_event = Event(event_name, "This is the starter description, change it with /events description this_events_id your_description", event_host.id, event_type.lower())

        database.insert_event(new_event)

        logger.info(f"Created the event successfully and it was added to database, Params: type=\"{event_type}\" name=\"{event_name}\" host=\"{event_host.name}\"")
        await interaction.response.send_message(f"Created {event_type} {event_name} for {event_host.display_name} successfully")

    @app_commands.command(name="remove", description="Remove an already existing event")
    async def remove(self, interaction: discord.Interaction, event_id: int):
        logger.info(f"@{interaction.user.display_name} ran remove command")
        if not settings.check_role_permission(interaction.guild, interaction.user):
            await interaction.response.send_message("You dont have permission to use this command", ephemeral=True)
            logger.info("They did not have permission to use the command")
            return
        
        try:
            id, type, name, description, hostid = database.get_event_by_id(event_id)
        except TypeError as e:
            await interaction.response.send_message(f"There is not event with the id {event_id}")
            logger.info(f"Event id {event_id} is not associated with an event")
            return
        
        event_to_remove: Event = Event(name, description, hostid, type)
        database.remove_event(event_to_remove)

        logger.info(f"Event id {event_id} was successfully removed from the database")
        await interaction.response.send_message(f"Removed event {name}")

    @app_commands.command(name="list", description="Lists all active events")
    async def list(self, interaction: discord.Interaction):
        logger.info(f"@{interaction.user.display_name} ran list command")
        if not settings.check_role_permission(interaction.guild, interaction.user):
            await interaction.response.send_message("You dont have permission to use this command", ephemeral=True)
            logger.info("They did not have permission to use the command")
            return

        events = database.get_all_events()

        responseText = "# Events: \n"
        if events:
            
            for id, type, name, description, hostid in events:
                responseText += "## " + type.upper() + ": " + name + "\n"
                responseText += "EventId: " + str(id) + "\n"
                responseText += "Host: " + str(hostid) + "\n"
                responseText += "Description: \n" + description + "\n"
            
            responseText += ""
            logger.info("Responded with events list")
        else:
            responseText = "No active events"
            logger.info("No events exist")

        await interaction.response.send_message(responseText)

    @app_commands.command(name="description", description="Change the description of an event")
    async def setdescription(self, interaction: discord.Interaction, event_id: int, event_description: str):
        logger.info(f"@{interaction.user.display_name} ran description command")
        if not settings.check_role_permission(interaction.guild, interaction.user):
            await interaction.response.send_message("You dont have permission to use this command", ephemeral=True)
            logger.info("They did not have permission to use the command")
            return

        if not database.get_event_by_id(event_id):
            await interaction.response.send_message(f"There is no event with the id {event_id}")
            logger.info(f"Event id {event_id} is not associated with an event")
            return
        
        id, type, name, description, hostid = database.get_event_by_id(event_id)

        event_to_edit: Event = Event(name, description, hostid, type)

        database.update_description(event_to_edit, event_description)

        logger.info(f"Updated event {event_id} with description \"{description}\"")
        await interaction.response.send_message("Updated the description successfully")

async def setup(bot: commands.Bot):
    bot.tree.add_command(MyGroup(name="events", description="Events"))