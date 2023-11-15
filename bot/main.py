import discord
from discord import app_commands

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from commands.catalog import generate_catalog
from commands.replies import get_thread_replies
from commands.test_embed import cmd_embed 
from paginator import Paginator
from add_fields_to_embed import add_fields_to_embed

import configparser

DEEP_PINK = 0xe6528b

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

id_field = 'ID 🔑'
time_field = 'TIME 🕖'

@client.tree.command()
@app_commands.describe(board="the catalog of this board")
async def catalog_search(interaction: discord.Interaction, board: str, keyword: str):
    embeds = []
    catalog_data = generate_catalog(board, keyword)

    for page in catalog_data:
        for thread in page['threads']:
            embed = discord.Embed(title=thread['SUB'], url=f'https://boards.4channel.org/{board}/thread/{thread[id_field]}', color=DEEP_PINK)
            add_fields_to_embed(embed, thread)
            embeds.append(embed)
    paginator = Paginator(interaction, embeds)
    await interaction.response.send_message(embed=embeds[0], view=paginator) 

@client.tree.command()
@app_commands.describe(board="the board on which the thread exists", thread_id='the id of the thread')
async def replies(interaction: discord.Interaction, board: str, thread_id: int):
    replies = get_thread_replies(board, thread_id)
    
    url = f'https://boards.4channel.org/{board}/thread/{thread_id}'
    embed_op = discord.Embed(title="OP's post", url=url, color=DEEP_PINK)

    add_fields_to_embed(embed_op, replies[0])
    await interaction.response.send_message(embed=embed_op, ephemeral=True)

    reply_count = 0
    embed = None
    for reply in replies[1:]:
        if reply_count % 5 == 0:
            if embed is not None:
                await interaction.followup.send(embed=embed, ephemeral=True)
            embed = discord.Embed(title=f"<t:{reply[time_field]}>", url=f'https://boards.4channel.org/{board}/thread/{reply[id_field]}', color=DEEP_PINK)
        add_fields_to_embed(embed, reply)
        reply_count += 1
        if reply_count % 5 != 0:
            embed.add_field(name=zero_width_space, value=zero_width_space, inline=False)
    if embed is not None:
        await interaction.followup.send(embed=embed, ephemeral=True)

@client.tree.command()
@app_commands.describe()
async def test_embed(interaction: discord.Interaction):
    embed=cmd_embed()
    await interaction.response.send_message(embed=embed)

@client.tree.command() # replace with your guild id
async def paginate(interaction: discord.Interaction):
    embeds = [
        discord.Embed(title="Page 1", description="This is the first page", color=discord.Color.red()),
        discord.Embed(title="Page 2", description="This is the second page", color=discord.Color.green()),
        discord.Embed(title="Page 3", description="This is the third page", color=discord.Color.blue())
    ]
    paginator = Paginator(interaction, embeds)
    await interaction.response.send_message(embed=embeds[0], view=paginator)



client.run(get_token())
