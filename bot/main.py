import discord
from discord import app_commands

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from commands.catalog import generate_catalog
from commands.replies import get_thread_replies

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

@client.tree.command()
@app_commands.describe(num1="first number", num2="second number")
async def four_arithmetic(interaction: discord.Interaction, num1: float, num2: float):
    embed = discord.Embed(title="Four Arithmetic Operations", color=DEEP_PINK)
    embed.add_field(name="Addition", value=f"{num1} + {num2} = {num1 + num2}", inline=False)
    embed.add_field(name="Subtraction", value=f"{num1} - {num2} = {num1 - num2}", inline=False)
    embed.add_field(name="Multiplication", value=f"{num1} * {num2} = {num1 * num2}", inline=False)
    try:
        embed.add_field(name="Division", value=f"{num1} / {num2} = {num1 / num2}", inline=False)
    except ZeroDivisionError:
        embed.add_field(name="Division", value="Cannot divide by zero.", inline=False)
    await interaction.response.send_message(embed=embed)

id_field = 'ID 🔑'
comment_field = 'COMMENT 💬'
time_field = 'TIME 🕖'
link_field = 'LINK 🌐'

@client.tree.command()
@app_commands.describe(board="the catalog of this board")
async def catalog_search(interaction: discord.Interaction, board: str, keyword: str):
    catalog_data = generate_catalog(board, keyword)
    await interaction.response.send_message(f"Catalog of /{board}/ was requested.", ephemeral=True)
    for page in catalog_data:
        for thread in page['threads']:
            embed = discord.Embed(title=thread['SUB'], url=f'https://boards.4channel.org/{board}/thread/{thread[id_field]}', color=DEEP_PINK)
            for name, value in thread.items():
                field_char_limit = 1024
                if name == comment_field and len(value) > field_char_limit:
                    split_pos = value.rfind('\n', 0, field_char_limit)
                    if split_pos == -1:
                        split_pos = field_char_limit
                    embed.add_field(name=name, value=value[:split_pos], inline=False)
                    zero_width_space = '\u200B'
                    embed.add_field(name=zero_width_space, value=value[split_pos:], inline=False)
                else:
                    embed.add_field(name=name, value=value, inline=False)
            await interaction.followup.send(embed=embed) 



@client.tree.command()
@app_commands.describe(board="the board on which the thread exists", thread_id='the id of the thread')
async def replies(interaction: discord.Interaction, board: str, thread_id: int):
    replies = get_thread_replies(board, thread_id)
    
    url = f'https://boards.4channel.org/{board}/thread/{thread_id}'
    embed_op = discord.Embed(title="OP's post", url=url, color=DEEP_PINK)
    for name, value in replies[0].items():
        field_char_limit = 1024
        if name == time_field:
            embed_op.add_field(name=name, value=f"<t:{value}>", inline=False)
        elif name == comment_field and len(value) > field_char_limit:
            split_pos = value.rfind('\n', 0, field_char_limit)
            if split_pos == -1:
                split_pos = field_char_limit
            embed_op.add_field(name=name, value=value[:split_pos], inline=False)
            zero_width_space = '\u200B'
            embed_op.add_field(name=zero_width_space, value=value[split_pos:], inline=False)
        elif name == link_field:
            embed_op.set_image(url=value)
        else:
            embed_op.add_field(name=name, value=value, inline=False)
    await interaction.response.send_message(embed=embed_op, ephemeral=True)

    reply_count = 0
    embed = None
    for reply in replies[1:]:
        if reply_count % 5 == 0:
            if embed is not None:
                await interaction.followup.send(embed=embed, ephemeral=True)
            embed = discord.Embed(title=f"<t:{reply[time_field]}>", url=f'https://boards.4channel.org/{board}/thread/{reply[id_field]}', color=DEEP_PINK)
        for name, value in reply.items():
            field_char_limit = 1024
            if name == comment_field and len(value) > field_char_limit:
                split_pos = value.rfind('\n', 0, field_char_limit)
                if split_pos == -1:
                    split_pos = field_char_limit
                embed.add_field(name=name, value=value[:split_pos], inline=False)
                zero_width_space = '\u200B'
                embed.add_field(name=zero_width_space, value=value[split_pos:], inline=False)
            elif name == link_field:
                embed.set_image(url=value)
            else:
                embed.add_field(name=name, value=value, inline=False)
        reply_count += 1
    if embed is not None:
        await interaction.followup.send(embed=embed, ephemeral=True)



@client.tree.command()
@app_commands.describe()
async def test_embed(interaction: discord.Interaction):
    embed = discord.Embed(title="Sample Embed", url="https://4chan.org/", description="This is an embed of 4chan", color=DEEP_PINK)
    embed.add_field(name='', value='test')
    await interaction.response.send_message(embed=embed)


client.run(get_token())