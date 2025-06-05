# Bookwyrm


Bookwyrm is a companion tool for Dungeons & Dragons fifth edition that provides quick access to spell information without requiring tedious book dives or scouring the web. It features a robust search function that helps users efficiently find spells based on a wide range of criteria.

Bookwyrm scrapes spell data from the web and stores it locally for fast and reliable lookups. It can be used through your CLI or as a Discord App/Bot.

![gif](https://i.imgur.com/hIK6Arf.gif)
## Features
- Quickly pull up a spell's details
- Comprehensive search function that lets users filter spells with a wide range of criteria
  - Combine as many filters as you want *ex) search for all ritual spells on the Druid spell list*
  - Great for planning out your character's known spells
- Creates a local spell library
  - Saved in a JSON file - super easy to modify values or add your own homebrew
  - No more reliance on websites, your library is *yours forever*
- Easily check for + download spell updates

## Setting up Bookwyrm

### Prerequisites

Bookwyrm requires Python 3.10 or higher.

### Installation
- Extract the contents of `bookwyrm.zip`
- Install required dependencies by running the following command in Bookwyrm's root directory:
```
pip install -r requirements.txt
```
*NOTE: The `discord.py` dependency is only required if you intend on running your own Discord bot.*

## Running the program

### CLI application

After following the above instructions, enter the following from within Bookwyrm's folder:
```
python bookwyrm.py
```

### Discord App/Bot
- Create a Discord Application at the [Discord Developer Portal](https://discord.com/developers/applications)
- Find your bot token, then paste it between the empty quotation marks on the last line of `bot.py`
#### Make sure the bot has the following permissions:
- Send Messages, Send Messages in Threads
- View Channels
- Add Reactions
- Manage Messages (not strictly required, recommended for smoother page navigation of search results)

#### Running the bot
Run the following from within Bookwyrm's folder:
```
python bot.py
```

