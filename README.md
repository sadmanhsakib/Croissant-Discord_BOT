# Croissant Discord Bot

A feature-rich Discord bot written in Python that helps moderate channels, automate routine tasks, provide utility commands, and fetch media content from Reddit. Croissant is designed to be **server-aware** (per-guild configuration), with settings persisted in a PostgreSQL database.

---
If you want to add **Croissant** in your Discord server, feel free to add this bot to your server click [here](https://discord.com/oauth2/authorize?client_id=1175661660656652096&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize&response_type=code&scope=bot).

---
## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Commands](#commands)
- [How It Works (Architecture)](#how-it-works-architecture)
- [Requirements](#requirements)
- [Configuration](#configuration)
- [Installation & Local Development](#installation--local-development)
- [Running the Bot](#running-the-bot)
- [Discord Permissions & Intents](#discord-permissions--intents)
- [Database Schema](#database-schema)
- [Deployment Notes](#deployment-notes)
- [Troubleshooting](#troubleshooting)
- [Security & Privacy](#security--privacy)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Croissant is an “everyday” Discord bot that provides:

- Utility commands (ping, status, echo, hello)
- Moderation helpers (bulk message deletion)
- Media storage and quick posting via `;ITEM_NAME`
- Reddit image/GIF fetching (with NSFW gating)
- Presence-based greetings (welcome back / bye)
- Scheduled channel cleanup (“AutoDelete”) at a configured daily time
- Per-server configuration stored in PostgreSQL

Default command prefix is `-` (per-server customizable).

---

## Key Features

- **Per-server configuration**
  - Prefix, Reddit search limits, NSFW policy, delete timers, and more are stored per guild.
- **Media storage**
  - Save image/GIF/video links under a short name and recall them instantly.
- **Reddit integration**
  - Fetch a random image/GIF from a subreddit with controls for NSFW content.
- **Scheduled channel purging**
  - Daily automated cleanup for configured channels.
- **Presence notifications**
  - Optional “welcome back / bye” messages when members go online/offline.

---

## Commands

Croissant uses a **prefix command system** (default: `-`). Commands below assume the prefix is `-`.

### General

- `-help`
  - Shows an embedded help menu.
- `-echo MESSAGE`
  - Repeats the message back to the channel.
- `-hello`
  - Greets the user.
- `-ping`
  - Displays bot latency.
- `-status`
  - Shows bot status.
- `-list`
  - Lists saved item names in normal storage.
- `-list nsfw`
  - Lists saved item names in NSFW storage.
- `-list autodelete`
  - Lists channels scheduled for daily auto-deletion.

### Moderation

- `-del NUMBER`
  - Deletes `NUMBER` messages in the current channel (also removes the command message).
- `-del all`
  - Deletes all messages in the current channel (bulk purge).

### Media / Storage

- `;ITEM_NAME`
  - Posts the saved link for `ITEM_NAME` (triggered by typing `;name` in any message).
- `-add NAME LINK`
  - Adds an item to normal storage.
- `-add nsfw NAME LINK`
  - Adds an item to NSFW storage (only sends in NSFW channels).
- `-rmv NAME`
  - Removes an item from storage (normal or NSFW).

### Greetings

- `-greet USERNAME ITEM1 ITEM2 ...`
  - Sends a text greeting, then posts the requested stored items.

### Reddit

- `-reddit SUBREDDIT_NAME`
  - Fetches a random **image/GIF** post from the given subreddit.
  - NSFW subreddits are blocked unless `NSFW_ALLOWED=true` for that server.

### Scheduled AutoDelete

- `-add autodelete CHANNEL_ID TIME(HOUR:MINUTE:SECOND)`
  - Schedules a channel to be purged daily at the specified time (Asia/Dhaka timezone).
- `-rmv autodelete CHANNEL_ID`
  - Removes the channel from the schedule.

### Configuration (Per Server)

- `-set VARIABLE VALUE`
  - Supported variables:
    - `PREFIX`
    - `DELETE_AFTER`
    - `SEARCH_LIMIT`
    - `NSFW_ALLOWED`
    - `ACTIVITY_CHANNEL_ID`

### Utilities

- `-random-line quran|sunnah|quote`
  - Sends a random line from `assets/quran.txt`, `assets/sunnah.txt`, or `assets/quote.txt`.

### Admin / Maintenance

- `-reload_var`
  - Reloads all server configuration values from the database.

---

## How It Works (Architecture)

- **[main.py](main.py)**
  - Creates the Discord bot, loads configuration from the database, authenticates Reddit, and loads the command cog.
  - Handles:
    - Guild join/leave events
    - Message events (`;ITEM_NAME` parsing)
    - Presence updates (welcome back / bye)
- **[bot_commands.py](bot_commands.py)**
  - The main command cog (commands listed above).
  - Runs a background scheduler loop (every 60s) for daily channel purging.
- **[config.py](config.py)**
  - Loads [.env](.env) variables and maintains per-guild caches loaded from PostgreSQL.
- **[database.py](database.py)**
  - Async PostgreSQL layer using `asyncpg`, storing per-server variables in a single table.
- **[reddit.py](reddit.py)**
  - Reddit authentication + image/GIF fetching via `asyncpraw`.
- **[keep_alive.py](keep_alive.py)**
  - A minimal Flask server to keep the process alive on certain hosting platforms.

---

## Requirements

- Python 3.10+ recommended
- A Discord application + bot token
- PostgreSQL database (connection URL required)
- Reddit API credentials (optional but required for `-reddit`)

> Note: [requirements.txt](requirements.txt) appears to contain non-text/NULL bytes in this repo snapshot, so you may need to regenerate it. The code imports indicate you’ll need at least:
> - `discord.py`
> - `python-dotenv`
> - `asyncpg`
> - `asyncpraw`
> - `asyncprawcore`
> - `Flask`

---

## Configuration

Create a [.env](.env) file in the project root with:

```env
BOT_TOKEN=your_discord_bot_token
REPO_URL=https://github.com/sadmanhsakib/Croissant-Discord_BOT
DATABASE_URL=postgresql://user:password@host:port/dbname

# Reddit (required only for -reddit)
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
CLIENT_ID=your_reddit_client_id
SECRET=your_reddit_client_secret