from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
from telegram.ext import CallbackContext, CallbackQueryHandler
from config import (
    WELCOME_MESSAGE,
    HELP_MESSAGE,
    ERROR_MESSAGE,
    TEXT_TOO_LONG,
    INVALID_LANGUAGE,
    LANGUAGE_CHANGED,
    SUPPORTED_LANGUAGES,
    DEFAULT_LANG,
    ADMIN_IDS,
    BROADCAST_HELP,
    BROADCAST_UNAUTHORIZED,
    BROADCAST_USAGE,
    BROADCAST_SUCCESS,
    BROADCAST_NO_USERS,
    logger
)
from utils import generate_speech, cleanup_file

# Store user language preferences (in memory)
user_languages = {}
# Store active user IDs (in memory)
active_users = set()

def create_language_keyboard():
    """Create an inline keyboard for language selection."""
    keyboard = []
    row = []
    for code, name in SUPPORTED_LANGUAGES.items():
        # Add flag emoji based on language code
        flag = "🌐"  # Default flag
        if code == 'en': flag = "🇬🇧"
        elif code == 'es': flag = "🇪🇸"
        elif code == 'fr': flag = "🇫🇷"
        elif code == 'de': flag = "🇩🇪"
        elif code == 'it': flag = "🇮🇹"
        elif code == 'pt': flag = "🇵🇹"
        elif code == 'ru': flag = "🇷🇺"
        elif code == 'hi': flag = "🇮🇳"
        elif code == 'ja': flag = "🇯🇵"
        elif code == 'ko': flag = "🇰🇷"
        elif code == 'ml': flag = "🇮🇳"

        button = InlineKeyboardButton(f"{flag} {name}", callback_data=f"lang_{code}")
        row.append(button)

        # Create new row after every 2 buttons
        if len(row) == 2:
            keyboard.append(row)
            row = []

    # Add any remaining buttons
    if row:
        keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)

def create_main_menu_keyboard():
    """Create main menu keyboard."""
    keyboard = [
        [InlineKeyboardButton("🔄 Change Language", callback_data="change_lang")],
        [InlineKeyboardButton("❓ Help", callback_data="help"), 
         InlineKeyboardButton("ℹ️ About", callback_data="about")]
    ]
    return InlineKeyboardMarkup(keyboard)

def start_command(update: Update, context: CallbackContext) -> None:
    """Handle the /start command."""
    user_id = update.effective_user.id
    logger.info(f"Start command received from user {user_id}")
    # Add user to active users
    active_users.add(user_id)
    keyboard = create_main_menu_keyboard()
    update.message.reply_text(WELCOME_MESSAGE, reply_markup=keyboard)

def help_command(update: Update, context: CallbackContext) -> None:
    """Handle the /help command."""
    user_id = update.effective_user.id
    logger.info(f"Help command received from user {user_id}")
    # Add help message for admin users
    if user_id in ADMIN_IDS:
        help_text = HELP_MESSAGE + "\n\n" + BROADCAST_HELP
    else:
        help_text = HELP_MESSAGE
    keyboard = create_main_menu_keyboard()
    update.message.reply_text(help_text, reply_markup=keyboard)

def broadcast_command(update: Update, context: CallbackContext) -> None:
    """Handle the /broadcast command (admin only)."""
    user_id = update.effective_user.id
    logger.info(f"Broadcast command received from user {user_id}")

    # Check if user is admin
    if user_id not in ADMIN_IDS:
        logger.warning(f"Unauthorized broadcast attempt from user {user_id}")
        update.message.reply_text(BROADCAST_UNAUTHORIZED)
        return

    # Check if message is provided
    if not context.args:
        update.message.reply_text(BROADCAST_USAGE)
        return

    # Get broadcast message
    message = ' '.join(context.args)
    success_count = 0
    failed_users = []

    # Broadcast message to all active users
    for target_id in active_users:
        try:
            context.bot.send_message(chat_id=target_id, text=message)
            success_count += 1
            logger.debug(f"Broadcast message sent to user {target_id}")
        except Exception as e:
            logger.error(f"Failed to send broadcast to user {target_id}: {str(e)}")
            failed_users.append(target_id)

    # Log broadcast results
    logger.info(f"Broadcast completed: {success_count} successful, {len(failed_users)} failed")

    # Remove failed users from active users set
    for failed_id in failed_users:
        active_users.discard(failed_id)

    # Send result to admin
    if success_count > 0:
        update.message.reply_text(BROADCAST_SUCCESS.format(success_count))
    else:
        update.message.reply_text(BROADCAST_NO_USERS)

def lang_command(update: Update, context: CallbackContext) -> None:
    """Handle the /lang command to change language."""
    logger.info(f"Language command received from user {update.effective_user.id}")
    keyboard = create_language_keyboard()
    message = (
        "Please select your preferred language:\n\n"
        "Current language: " + SUPPORTED_LANGUAGES.get(
            user_languages.get(update.effective_user.id, DEFAULT_LANG),
            "English (default)"
        )
    )
    update.message.reply_text(message, reply_markup=keyboard)

def button_callback(update: Update, context: CallbackContext) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    user_id = query.from_user.id
    logger.debug(f"Received callback query from user {user_id}: {query.data}")

    # Answer callback query to remove loading state
    query.answer()

    if query.data == "change_lang":
        keyboard = create_language_keyboard()
        query.edit_message_text("Please select your preferred language:", reply_markup=keyboard)
        logger.debug(f"Showing language selection menu to user {user_id}")

    elif query.data == "help":
        keyboard = create_main_menu_keyboard()
        query.edit_message_text(HELP_MESSAGE, reply_markup=keyboard)
        logger.debug(f"Showing help message to user {user_id}")

    elif query.data == "about":
        keyboard = create_main_menu_keyboard()
        about_text = "I'm a Text-to-Speech bot that can convert your messages into voice in multiple languages! 🎤"
        query.edit_message_text(about_text, reply_markup=keyboard)
        logger.debug(f"Showing about message to user {user_id}")

    elif query.data.startswith("lang_"):
        lang_code = query.data.split("_")[1]
        if lang_code in SUPPORTED_LANGUAGES:
            user_languages[user_id] = lang_code
            keyboard = create_main_menu_keyboard()
            message = LANGUAGE_CHANGED.format(SUPPORTED_LANGUAGES[lang_code])
            query.edit_message_text(message, reply_markup=keyboard)
            logger.info(f"Language changed to {SUPPORTED_LANGUAGES[lang_code]} for user {user_id}")
        else:
            logger.warning(f"Invalid language code received from user {user_id}: {lang_code}")
            query.edit_message_text(INVALID_LANGUAGE)

def handle_text(update: Update, context: CallbackContext) -> None:
    """Handle text messages and convert them to speech."""
    if not update.message or not update.message.text:
        return

    text = update.message.text
    user_id = update.effective_user.id
    logger.info(f"Processing text message from user {user_id}: {text[:50]}...")

    # Check message length
    if len(text) > 100000:
        logger.warning(f"Text too long from user {user_id}: {len(text)} characters")
        update.message.reply_text(TEXT_TOO_LONG)
        return

    try:
        # Show typing action while processing
        context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action=ChatAction.RECORD_VOICE
        )

        # Get user's language preference or use default
        lang = user_languages.get(user_id, DEFAULT_LANG)
        logger.info(f"Generating speech for user {user_id} in {SUPPORTED_LANGUAGES[lang]}")

        # Generate speech
        success, result = generate_speech(text, lang)

        if success:
            logger.info(f"Speech generated successfully for user {user_id}, sending voice message")
            # Send voice message
            with open(result, 'rb') as audio:
                update.message.reply_voice(voice=audio)
            # Cleanup
            cleanup_file(result)
            logger.info(f"Voice message sent and cleanup completed for user {user_id}")
        else:
            logger.error(f"Speech generation failed for user {user_id}: {result}")
            update.message.reply_text(ERROR_MESSAGE)

    except Exception as e:
        logger.error(f"Error processing message for user {user_id}: {str(e)}")
        update.message.reply_text(ERROR_MESSAGE)

def error_handler(update: Update, context: CallbackContext) -> None:
    """Handle errors."""
    error = context.error
    logger.error(f"Update {update} caused error {error}")

    try:
        if "Conflict" in str(error):
            logger.warning("Detected conflict with another bot instance. This instance will attempt to continue.")
            return

        if update and update.effective_message:
            update.effective_message.reply_text(ERROR_MESSAGE)
    except Exception as e:
        logger.error(f"Error in error handler: {str(e)}")