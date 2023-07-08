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
    return config['DEFAULT']['DISCORD_GUILD_ID']

MY_GUILD = discord.Object(id=int(get_guild_id()))

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
    embed = discord.Embed(title="Four Arithmetic Operations", color=0xFF5733)
    embed.add_field(name="Addition", value=f"{num1} + {num2} = {num1 + num2}", inline=False)
    embed.add_field(name="Subtraction", value=f"{num1} - {num2} = {num1 - num2}", inline=False)
    embed.add_field(name="Multiplication", value=f"{num1} * {num2} = {num1 * num2}", inline=False)
    try:
        embed.add_field(name="Division", value=f"{num1} / {num2} = {num1 / num2}", inline=False)
    except ZeroDivisionError:
        embed.add_field(name="Division", value="Cannot divide by zero.", inline=False)
    await interaction.response.send_message(embed=embed)



@client.tree.command()
@app_commands.describe(board="the catalog of this board")
# async def catalog_search(interaction: discord.Interaction, board: str, keyword: str):
#     await interaction.response.send_message(f"Catalog of /{board}/ was requested.", ephemeral=True)
#     catalog_data = generate_catalog(board, keyword)
#     for page in catalog_data:
#         for thread in page['threads']:
#             embed = discord.Embed(title=thread['SUB'], url=f'https://boards.4channel.org/{board}/thread/{thread["ID"]}', color=0xFF5733)
#             for name, value in thread.items():
#                 if name == 'COMMENT' and len(value) > 1024:
#                     # Split the COMMENT field into two fields
#                     embed.add_field(name=name, value=value[:1024], inline=False)
#                     embed.add_field(name='\u200B', value=value[1024:], inline=False)
#                 else:
#                     embed.add_field(name=name, value=value, inline=False)
#             await interaction.followup.send(embed=embed) 

async def catalog_search(interaction: discord.Interaction, board: str, keyword: str):
    await interaction.response.send_message(f"Catalog of /{board}/ was requested.", ephemeral=True)
    catalog_data = generate_catalog(board, keyword)
    for page in catalog_data:
        for thread in page['threads']:
            embed = discord.Embed(title=thread['SUB'], url=f'https://boards.4channel.org/{board}/thread/{thread["ID"]}', color=0xFF5733)
            for name, value in thread.items():
                if name == 'COMMENT' and len(value) > 1024:
                    # Find the last space character before the 1024th character
                    split_pos = value.rfind('\n', 0, 1024)
                    if split_pos == -1:
                        split_pos = 1024
                    # Split the COMMENT field at the split position
                    embed.add_field(name=name, value=value[:split_pos], inline=False)
                    embed.add_field(name='\u200B', value=value[split_pos:], inline=False)
                else:
                    embed.add_field(name=name, value=value, inline=False)
            await interaction.followup.send(embed=embed) 



@client.tree.command()
@app_commands.describe(board="the board on which the thread exists", thread_id='the id of the thread')
async def replies(interaction: discord.Interaction, board: str, thread_id: int):
    await interaction.response.send_message(f"replies of {thread_id} on /{board}/ requested.", ephemeral=True)
    all_replies = get_thread_replies(board, thread_id)
    for reply in all_replies:
        await interaction.followup.send(reply)


@client.tree.command()
@app_commands.describe()
async def test_embed(interaction: discord.Interaction):
    embed = discord.Embed(title="Sample Embed", url="https://4chan.org/", description="This is an embed of 4chan", color=0xFF5733)
    embed.add_field(name='', value='test')
    await interaction.response.send_message(embed=embed)


client.run(get_token())