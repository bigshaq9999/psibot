import discord
from discord import app_commands

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from commands.catalog import generate_catalog
from commands.replies import get_thread_replies

import configparser

def get_token():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['DEFAULT']['DISCORD_BOT_TOKEN']

def get_guild_id():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['DEFAULT']['GUILD_ID']

MY_GUILD = discord.Object(get_guild_id)

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


client = MyClient()

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

@client.tree.command()
@app_commands.describe(num1="first number", num2="second number")
async def four_arithmetic(interaction: discord.Interaction, num1: float, num2: float):
    await interaction.response.send_message(f"{num1} + {num2} = {num1 + num2}")
    await interaction.followup.send(f"{num1} - {num2} = {num1 - num2}")
    await interaction.followup.send(f"{num1} * {num2} = {num1 * num2}")
    try:
        await interaction.followup.send(f"{num1} / {num2} = {num1 / num2}")
    except ZeroDivisionError:
        await interaction.followup.send("Cannot divide by zero.")



@client.tree.command()
@app_commands.describe(board="the catalog of this board")
async def catalog_search(interaction: discord.Interaction, board: str, keyword: str):
    await interaction.response.send_message(f"Catalog of {board} was requested.", ephemeral=True)
    catalog_data = generate_catalog(board, keyword)
    for page in catalog_data:
        # page_str = f"PAGE {page['page']}\n\n"
        for thread in page['threads']:
            print(len(thread))
            await interaction.followup.send(thread) 

@client.tree.command()
@app_commands.describe(board="the board on which the thread exists", thread_id='the id of the thread')
async def replies(interaction: discord.Interaction, board: str, thread_id: int):
    await interaction.response.send_message(f"replies of {thread_id} on /{board}/ requested.", ephemeral=True)
    all_replies = get_thread_replies(board, thread_id)
    for reply in all_replies:
        await interaction.followup.send(reply)


def get_token():
    with open('token.txt', 'r') as file:
        return file.read().strip()

client.run(get_token())