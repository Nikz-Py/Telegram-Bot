# Deploying the Telegram Text-to-Speech Bot on Render

This guide provides step-by-step instructions for deploying the Telegram Text-to-Speech Bot on Render.

## Prerequisites

1. A [Render](https://render.com/) account
2. A [Telegram](https://telegram.org/) bot token from [BotFather](https://t.me/botfather)
3. Your Telegram user ID (for admin access, optional)

## Deployment Steps

### Option 1: Deploy via Blueprint (Recommended)

Render Blueprints enable you to deploy multiple services with a single click.

1. Fork or clone this repository to your GitHub account.

2. Connect your GitHub account to Render.

3. Click the "New +" button in the Render dashboard and select "Blueprint".

4. Connect to your GitHub account and select the repository.

5. Render will automatically detect the `render.yaml` file and configure:
   - A web service for the Flask health check API
   - A worker service for the Telegram bot
   - A PostgreSQL database

6. Configure the environment variables:
   - `TELEGRAM_TOKEN`: Your Telegram bot token from BotFather
   - `ADMIN_IDS`: Comma-separated list of Telegram user IDs (optional)

7. Click "Apply" to deploy the services.

### Option 2: Manual Deployment

If you prefer to deploy services individually:

#### 1. Create a PostgreSQL Database

1. In the Render dashboard, go to "PostgreSQL" and click "New PostgreSQL".
2. Enter a name (e.g., "tts-bot-db") and leave other settings as default.
3. Click "Create Database".
4. Note the "External Database URL" for later use.

#### 2. Deploy the Web Service

1. In the Render dashboard, go to "Web Services" and click "New Web Service".
2. Connect your GitHub repository.
3. Configure the following settings:
   - Name: `tts-bot-web`
   - Environment: `Python`
   - Build Command: `pip install -e .`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT main:app`
   - Health Check Path: `/health`

4. Add the following environment variables:
   - `RENDER`: `true`
   - `TELEGRAM_TOKEN`: Your Telegram bot token
   - `ADMIN_IDS`: Comma-separated list of admin Telegram user IDs (optional)
   - `SESSION_SECRET`: A random string for Flask sessions
   - `DATABASE_URL`: The External Database URL from step 1

5. Click "Create Web Service".

#### 3. Deploy the Worker Service

1. In the Render dashboard, go to "Background Workers" and click "New Background Worker".
2. Connect your GitHub repository.
3. Configure the following settings:
   - Name: `tts-bot-worker`
   - Environment: `Python`
   - Build Command: `pip install -e .`
   - Start Command: `python main.py`

4. Add the same environment variables as the web service:
   - `RENDER`: `true`
   - `TELEGRAM_TOKEN`: Your Telegram bot token
   - `ADMIN_IDS`: Comma-separated list of admin Telegram user IDs (optional)
   - `SESSION_SECRET`: A random string for Flask sessions (same as web service)
   - `DATABASE_URL`: The External Database URL from step 1

5. Click "Create Background Worker".

## Verifying Deployment

1. Once deployed, access the web service URL to check the health endpoint:
   - Navigate to `https://tts-bot-web.onrender.com/health`
   - You should see a JSON response with the bot's status

2. Send a message to your Telegram bot to verify it's working.

## Monitoring and Logs

- Monitor your services in the Render dashboard
- Check logs by clicking on a service and navigating to the "Logs" tab
- Set up notifications in the "Alerts" section for downtime or errors

## Updating the Bot

To update the bot, simply push changes to your GitHub repository. Render will automatically rebuild and redeploy the services.

## Troubleshooting

1. **Bot not responding**: Check the worker logs for errors.
2. **Database connection issues**: Verify your DATABASE_URL is correctly set.
3. **Health check failing**: Ensure both services are running properly.