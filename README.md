# 4chan Discord Bot 🤖

This is a Discord bot that allows users to search the catalog and view replies of threads on 4chan.

## Features 🔍

- Search the catalog of a specified board on 4chan for threads containing a specified keyword
- View the replies of a specified thread on a specified board on 4chan

## Setup ⚙️

1. Clone this repository to your local machine.
2. Create a `config.ini` file in the root directory of the project with the following contents:

```
[DEFAULT]
DISCORD_BOT_TOKEN = your_bot_token_here
GUILD_ID = your_guild_id_here
```

Make sure to replace `your_bot_token_here` and `your_guild_id_here` with your bot token and guild ID, respectively.
3. Run the bot by running `python main.py`.

## Usage 🎮

Once the bot is running, you can use the following commands in Discord:

- `/four_arithmetic num1:num1 num2:num2`: Perform basic arithmetic operations on two numbers.
- `/catalog_search board:board keyword:keyword`: Search the catalog of the specified board on 4chan for threads containing the specified keyword.
- `/replies board:board thread_id:thread_id`: View the replies of the specified thread on the specified board on 4chan.
