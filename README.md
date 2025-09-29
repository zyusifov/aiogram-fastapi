# Aiogram FastAPI Template

A modern template for building Telegram bots using [Aiogram 3.x](https://docs.aiogram.dev/) and [FastAPI](https://fastapi.tiangolo.com/) with PostgreSQL database integration.

## Project Structure

```
aiogram-fastapi/
├── app/
│   ├── admin.py              # SQLAdmin configuration
│   ├── config.py             # Environment configuration
│   ├── db.py                 # Database setup
│   ├── main.py               # FastAPI application entry point
│   ├── bot/
│   │   ├── dispatcher.py     # Bot dispatcher configuration
│   │   └── handlers/         # Bot command handlers
│   │       ├── help.py       # Help command
│   │       ├── location.py   # Location sharing functionality
│   │       └── start.py      # User registration
│   └── models/               # SQLAlchemy models
│       ├── users.py          # User model
│       └── locations.py      # Location model
├── docker-compose.yml        # PostgreSQL container setup
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Installation

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (optional, for PostgreSQL)
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))

### Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd aiogram-fastapi
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**

   Create a `.env` file in the project root:

   ```env
   BOT_TOKEN=your_telegram_bot_token_here
   WEBHOOK_URL=https://your-domain.com/webhook

   # Database configuration (optional - defaults provided)
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=bot_db
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   ```

5. **Start PostgreSQL Database**

   Using Docker Compose (recommended):

   ```bash
   docker-compose up -d
   ```

   Or use your own PostgreSQL instance and update the connection settings in `.env`.

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Bot Commands

The bot supports the following commands:

- `/start [referral_code]` - Register a new user or welcome back existing users
- `/help` - Display available commands
- `/location` - Request user's location and save it to the database

## API Endpoints

- `POST /webhook` - Telegram webhook endpoint for receiving updates
- `GET /admin` - SQLAdmin panel for database management
- `GET /map` - HTML page for visualize all users locations on map
