zero_width_space = '\u200B'
field_char_limit = 1024
link_field = 'LINK 🌐'
comment_field = 'COMMENT 💬'
def add_fields_to_embed(embed, thread):
    for name, value in thread.items():
        if name == comment_field and len(value) > field_char_limit:
            split_pos = value.rfind('\n', 0, field_char_limit)
            if split_pos == -1:
                split_pos = field_char_limit
            embed.add_field(name=name, value=value[:split_pos], inline=False)
            embed.add_field(name=zero_width_space, value=value[split_pos:], inline=False)
        elif name == link_field:
            embed.set_image(url=value)
        else:
            embed.add_field(name=name, value=value, inline=False)

if __name__ == '__main__':
    print('it does not work here!')
