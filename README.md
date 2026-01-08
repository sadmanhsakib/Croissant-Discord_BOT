# Croissant Discord Bot

A feature-rich Discord bot written in Python that helps moderate channels, automate routine tasks, provide utility commands, and fetch media content from Reddit. Croissant is designed to be **server-aware** (per-guild configuration), with settings persisted in a PostgreSQL database.

## 📑 Table of Contents

- [Overview](#overview)
- [Invite Croissant](#invite-croissant)
- [Key Features](#key-features)
- [Commands](#commands)
- [How It Works (Architecture)](#how-it-works-architecture)
- [Requirements](#requirements)
- [Configuration](#configuration)
- [Security & Privacy](#security--privacy)
- [Contributing](#contributing)
- [License](#license)

## 📖 Overview

Croissant is an “everyday” Discord bot that provides:

- AI-powered responses 
- Utility commands (ping, status, echo, hello)
- Moderation helpers (bulk message deletion)
- Media storage and quick posting via `;ITEM_NAME`
- Reddit image/GIF fetching (with NSFW gating)
- Presence-based greetings (welcome back / bye)
- Scheduled channel cleanup (“AutoDelete”) at a configured daily time
- Per-server configuration stored in PostgreSQL

Default command prefix is `-` (per-server customizable).

## 🥐 Invite Croissant
If you want to add **Croissant** in your Discord server, feel free to add this bot to your server by clicking [here](https://discord.com/oauth2/authorize?client_id=1419550251739516959&permissions=1374389746800&integration_type=0&scope=bot).

## ✨ Key Features

- **AI-Powered Responses**
  - Mention the bot to ask questions and receive intelligent AI-generated responses powered by [Groq](https://groq.com/).
- **Docker Support**
  - Easily deploy and host the bot using Docker for streamlined configuration and portability.
- **Per-server configuration**
  - Prefix, Reddit search limits, NSFW policy, delete timers, and more are stored per guild.
- **Media storage**
  - Save image/GIF/video links under a short name and recall them instantly.
- **Reddit integration**
  - Fetch a random image/GIF from a subreddit with controls for NSFW content.
- **Scheduled channel purging**
  - Optional daily automated cleanup for configured channels.
- **Presence notifications**
  - Optional “welcome back / bye” messages when members go online/offline.

## 💬 Commands

Croissant uses a **prefix command system** (default: `-`). Commands below assume the prefix is `-`. Additionally, the bot responds to **@mentions** for AI-powered conversations.

### AI Conversation

- `@Croissant YOUR_QUESTION`
  - Mention the bot followed by your question to receive an AI-generated response.
  - **How it works**: The bot uses [Groq](https://groq.com/)'s API to process your message and generate intelligent responses. The AI model, token limits, system prompt, and temperature are configured centrally in the database, allowing fine-tuned control over response behavior.
  - **Example**: `@Croissant What is the capital of France?`

### General

- `-help`
  - Shows an embedded help menu.
- `-echo MESSAGE --number(OPTIONAL)`
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

## 🏗️ How It Works (Architecture)

- **[main.py](main.py)**
  - Creates the Discord bot, loads configuration from the database, authenticates Reddit, and loads the command cog.
  - Handles:
    - Guild join/leave events
    - Message events (`;ITEM_NAME` parsing, AI mentions via Groq)
    - Presence updates (welcome back / bye)
- **[bot_commands.py](bot_commands.py)**
  - The main command cog (commands listed above).
  - Runs a background scheduler loop (every 60s) for daily channel purging.
- **[config.py](config.py)**
  - Loads [.env](example.env) variables and maintains per-guild caches loaded from PostgreSQL.
- **[database.py](database.py)**
  - Async PostgreSQL layer using `asyncpg`, storing per-server variables in a single table.
- **[reddit.py](reddit.py)**
  - Reddit authentication + image/GIF fetching via `asyncpraw`.

## 📋 Requirements

- Python 3.10+ recommended (Python 3.12 for Docker)
- A Discord application + bot token
- PostgreSQL database (connection URL required)
- Groq API key (required for AI-powered responses)
- Reddit API credentials (optional but required for `-reddit`)
- Check [requirements](requirements.txt) for additional libraries that are required for local hosting


## ⚙️ Configuration

Create a [.env](example.env) file in the project root with:

```env
BOT_TOKEN=your_discord_bot_token
README_URL=https://github.com/sadmanhsakib/Croissant-Discord_BOT/blob/main/README.md
DATABASE_URL=postgresql://user:password@host:port/dbname

# Groq API (required for AI responses)
GROQ_API=your_groq_api_key

# Reddit (required only for -reddit)
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
CLIENT_ID=your_reddit_client_id
SECRET=your_reddit_client_secret
```

## 🐳 Docker Deployment

Croissant includes a [Dockerfile](Dockerfile) for easy containerized deployment.

### Quick Start

1. **Build the Docker image**:
   ```bash
   docker build -t croissant-bot .
   ```

2. **Run the container**:
   ```bash
   docker run -d --env-file .env --name croissant croissant-bot
   ```

### Docker Compose (Optional)

For more complex setups, you can use Docker Compose to manage the bot alongside a PostgreSQL database.

### Benefits

- **Portability**: Run the bot on any system with Docker installed.
- **Isolation**: Dependencies are containerized, avoiding conflicts with the host system.
- **Easy Updates**: Rebuild the image to apply updates seamlessly.

## 🔒 Security & Privacy

Croissant is built with security and privacy in mind, ensuring that server data and user interactions are handled responsibly.

### Core Security Features
- **Environment Variables**: Sensitive credentials such as the Discord Bot Token, Database URL, and Reddit API keys are stored securely in a `.env` file and are never hardcoded into the source code. This prevents accidental exposure in version control.
- **Database Isolation**: All configuration data is stored in a secure PostgreSQL database (`asyncpg`). The bot uses parameterized queries to prevent SQL injection attacks.
- **Permission Management**:
  - The bot uses Discord's **Intents** system to request only necessary data (Message Content, Presences, Members).
  - Moderation commands (like `-del`) and configuration commands (like `-set`) are restricted to users with appropriate permissions or are designed to be used by server administrators.
- **Data Minimization**:
  - The bot **does not** permanently store user messages. It only processes messages in real-time for commands and specific triggers (like `;item`).
  - Stored data is strictly limited to server configuration (prefixes, limits) and user-defined shortcuts (media links).
  - AI responses are only stored in the local cache and are not stored in the database.
  - Upon server leave, the bot removes all server-specific data from the local cache and the database.
- **NSFW Protection**:
  - NSFW content from Reddit or stored items is strictly gated. It requires the server to explicitly enable `NSFW_ALLOWED` and can only be accessed in channels marked as NSFW within Discord.

## 🤝 Contributing

This project is the work of a sole contributor.

- **Lead Developer & Maintainer**: [Sadman Sakib](https://github.com/sadmanhsakib)

If you have suggestions, bug reports, or feature requests, please open an issue on the GitHub repository. While external contributions are welcome via Pull Requests, please note that the core vision and maintenance are handled by the author.

## 📄 License

This project is licensed under the PolyForm Noncommercial License 1.0.0 - see the [LICENSE](LICENSE) file for details.