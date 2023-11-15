import discord

DEEP_PINK = 0xe6528b
def cmd_embed():
    embed = discord.Embed(title="Sample Embed", url="https://4chan.org/", description="This is an embed of 4chan", color=DEEP_PINK)
    embed.add_field(name='', value='test')
    return embed

if __name__ == '__main__':
   print("You can't use this here!")
