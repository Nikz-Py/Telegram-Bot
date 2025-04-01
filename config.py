import os
import logging
import sys

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
    stream=sys.stdout  # Ensure logs go to stdout for better visibility
)
logger = logging.getLogger(__name__)

# Bot Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')
if not TELEGRAM_TOKEN:
    logger.error("No TELEGRAM_TOKEN provided in environment variables!")
    sys.exit(1)  # Exit if no token is provided

# Admin Configuration
ADMIN_IDS = [int(id.strip()) for id in os.getenv('ADMIN_IDS', '').split(',') if id.strip()]
if not ADMIN_IDS:
    logger.warning("No admin IDs configured. Broadcast feature will be disabled.")

# Temporary file storage
# Use /tmp for Render deployment or local temp_audio directory
TEMP_DIR = "/tmp/temp_audio" if os.environ.get('RENDER') == 'true' else "temp_audio"
try:
    # Ensure directory exists with correct permissions
    os.makedirs(TEMP_DIR, mode=0o755, exist_ok=True)
    logger.info(f"Successfully created/verified temp directory at {TEMP_DIR}")
except Exception as e:
    logger.error(f"Failed to create temp directory: {str(e)}")
    sys.exit(1)  # Exit if we can't create the temp directory

# Language settings
DEFAULT_LANG = 'en'
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'hi': 'Hindi',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ml': 'Malayalam'
}

# Bot messages
WELCOME_MESSAGE = """
Welcome to Text-to-Speech Bot! 🎤

I can convert your text messages into voice messages.
Just send me any text and I'll reply with an audio message.

Supported languages:
🇬🇧 English (default)
🇪🇸 Spanish (/lang es)
🇫🇷 French (/lang fr)
🇩🇪 German (/lang de)
🇮🇹 Italian (/lang it)
🇵🇹 Portuguese (/lang pt)
🇷🇺 Russian (/lang ru)
🇮🇳 Hindi (/lang hi)
🇯🇵 Japanese (/lang ja)
🇰🇷 Korean (/lang ko)
🇮🇳 Malayalam (/lang ml)

Commands:
/start - Show this welcome message
/help - Show help information
/lang - Change language (e.g., /lang fr for French)
"""

HELP_MESSAGE = """
How to use this bot:

1. Simply send any text message
2. I'll convert it to speech and send it back as a voice message

Supported languages:
   - English (default, /lang en)
   - Spanish (/lang es)
   - French (/lang fr)
   - German (/lang de)
   - Italian (/lang it)
   - Portuguese (/lang pt)
   - Russian (/lang ru)
   - Hindi (/lang hi)
   - Japanese (/lang ja)
   - Korean (/lang ko)
   - Malayalam (/lang ml)

To change language:
Use /lang followed by the language code
Example: /lang fr (for French)

Note: Messages should not be too long (max 100,000 characters)
"""

ERROR_MESSAGE = "Sorry, an error occurred while processing your request. Please try again."
TEXT_TOO_LONG = "Text is too long! Please send a message with less than 100,000 characters."
INVALID_LANGUAGE = "Invalid language code. Use /help to see all available languages and their codes."
LANGUAGE_CHANGED = "Language changed to {}"

# Admin Messages
BROADCAST_HELP = """
Admin Only Command:
/broadcast [message] - Send a message to all users
Example: /broadcast Hello everyone!

Note: This command is only available to admin users.
"""

BROADCAST_UNAUTHORIZED = "Sorry, you are not authorized to use this command."
BROADCAST_USAGE = "Please provide a message to broadcast.\nExample: /broadcast Hello everyone!"
BROADCAST_SUCCESS = "Message broadcast to {} users successfully!"
BROADCAST_NO_USERS = "No users to broadcast to."