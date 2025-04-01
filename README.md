# Telegram Text-to-Speech Bot

A Telegram bot that converts user text messages to voice messages using Google Text-to-Speech (gTTS).

## Features

- Converts text messages to voice messages
- Supports multiple languages (English, Spanish, French, German, Italian, Portuguese, Russian, Hindi, Japanese, Korean, Malayalam)
- Admin broadcast feature
- Health check API endpoint

## Local Development

1. Set up environment variables:
   - `TELEGRAM_TOKEN`: Your Telegram bot token from BotFather
   - `ADMIN_IDS`: Comma-separated list of Telegram user IDs for admin access (optional)
   - `SESSION_SECRET`: Secret key for Flask session (optional)
   - `DATABASE_URL`: Database connection string (optional, defaults to SQLite)

2. Run the application:
   ```
   python main.py
   ```

## Deploying on Render

This project includes configuration files for deployment on Render.

### Deployment Steps

1. Fork or clone this repository to your GitHub account.

2. Sign up for a [Render](https://render.com/) account if you don't have one.

3. Click the "New +" button in the Render dashboard and select "Blueprint".

4. Connect your GitHub account and select the repository.

5. Render will automatically detect the `render.yaml` file and configure the services.

6. Add the following environment variables in the Render dashboard:
   - `TELEGRAM_TOKEN`: Your Telegram bot token from BotFather
   - `ADMIN_IDS`: Comma-separated list of Telegram user IDs for admin access (optional)

7. Click "Apply" to deploy the services.

### What Gets Deployed

1. A web service that serves the Flask health check API
2. A worker service that runs the Telegram bot
3. A PostgreSQL database

## Project Structure

- `main.py`: Main entry point for the application
- `bot.py`: Telegram bot implementation
- `handlers.py`: Message handlers for the bot
- `config.py`: Configuration settings
- `app.py`: Flask web application
- `models.py`: Database models
- `utils.py`: Utility functions
- `Procfile`: Process definition for deployment
- `render.yaml`: Render Blueprint configuration