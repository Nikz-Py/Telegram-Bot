from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from config import TELEGRAM_TOKEN, logger
from handlers import (
    start_command,
    help_command,
    handle_text,
    error_handler,
    lang_command,
    button_callback,
    broadcast_command
)
import signal
import sys
import os
import atexit
import time
import threading

# Global updater instance for cleanup
_updater = None
_last_health_check = time.time()
_health_check_interval = 300  # 5 minutes

def health_check():
    """Periodic health check function."""
    global _last_health_check
    while True:
        try:
            current_time = time.time()
            if current_time - _last_health_check > _health_check_interval:
                logger.info("Health check: Bot is running normally")
                _last_health_check = current_time
            time.sleep(60)  # Check every minute
        except Exception as e:
            logger.error(f"Health check error: {str(e)}")

def cleanup():
    """Cleanup function to be called on exit."""
    global _updater
    if _updater:
        logger.info("Cleaning up bot resources...")
        try:
            _updater.stop()
            logger.info("Bot resources cleaned up successfully")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info(f"Received shutdown signal {signum}. Stopping bot...")
    cleanup()
    sys.exit(0)

def run_bot() -> None:
    """Run the bot."""
    global _updater

    while True:  # Main restart loop
        try:
            # Set up signal handlers for graceful shutdown
            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
            atexit.register(cleanup)

            logger.info("Initializing bot...")
            # Create the Updater with a higher read timeout to handle conflicts better
            _updater = Updater(TELEGRAM_TOKEN, use_context=True, request_kwargs={'read_timeout': 30})
            dispatcher = _updater.dispatcher

            # Add handlers
            dispatcher.add_handler(CommandHandler("start", start_command))
            dispatcher.add_handler(CommandHandler("help", help_command))
            dispatcher.add_handler(CommandHandler("lang", lang_command))
            dispatcher.add_handler(CommandHandler("broadcast", broadcast_command))
            dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

            # Add callback query handler for inline keyboard buttons
            dispatcher.add_handler(CallbackQueryHandler(button_callback))

            # Add error handler
            dispatcher.add_error_handler(error_handler)

            logger.info("Starting bot...")

            # Start health check thread
            health_thread = threading.Thread(target=health_check, daemon=True)
            health_thread.start()

            # Ensure clean start by removing webhook and dropping pending updates
            _updater.bot.delete_webhook()
            logger.info("Webhook deleted")

            # Small delay to ensure webhook deletion is processed
            time.sleep(1)

            logger.info("Starting polling...")
            # Use only drop_pending_updates to avoid conflict with clean parameter
            _updater.start_polling(drop_pending_updates=True)
            logger.info("Bot is running...")

            # Run the bot until a stop signal is received
            _updater.idle()

        except Exception as e:
            logger.error(f"Error running bot: {str(e)}")
            cleanup()
            logger.info("Waiting 10 seconds before restart attempt...")
            time.sleep(10)  # Wait before attempting restart