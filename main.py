from bot import run_bot
from config import logger, TELEGRAM_TOKEN
import time
from threading import Thread
from app import app  # Import the Flask app

def run_flask():
    """Run the Flask application."""
    app.run(host='0.0.0.0', port=5000)

def main():
    """Main entry point for the application."""
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN not set. Please set it in environment variables.")
        return

    # In deployment, the web service will handle the Flask app separately
    # Only start the Flask server in a thread when running in standalone mode
    import os
    if os.environ.get('RENDER') != 'true':
        # Start Flask server in a separate thread for local development
        flask_thread = Thread(target=run_flask, daemon=True)
        flask_thread.start()
        logger.info("Flask server started")

    logger.info("Starting Text-to-Speech Bot...")
    while True:  # Continuous operation loop
        try:
            run_bot()
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {str(e)}")
            logger.info("Restarting bot in 10 seconds...")
            time.sleep(10)

if __name__ == "__main__":
    main()