import os
import uuid
from gtts import gTTS
from config import TEMP_DIR, logger

def generate_speech(text: str, lang: str = 'en') -> tuple[bool, str]:
    """
    Generate speech from text using gTTS.

    Args:
        text (str): Text to convert to speech
        lang (str): Language code (default: 'en')

    Returns:
        tuple[bool, str]: (success, file_path or error_message)
    """
    try:
        # Ensure temp directory exists with proper permissions
        os.makedirs(TEMP_DIR, mode=0o755, exist_ok=True)
        logger.debug(f"Temporary directory {TEMP_DIR} verified")

        # Generate unique filename
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join(TEMP_DIR, filename)
        logger.debug(f"Generated filepath: {filepath}")

        # Generate speech
        logger.info("Initializing gTTS with text length: %d", len(text))
        tts = gTTS(text=text, lang=lang)

        logger.info("Saving speech to file")
        tts.save(filepath)
        logger.info(f"Speech file saved successfully at: {filepath}")

        return True, filepath
    except Exception as e:
        logger.error(f"Error generating speech: {str(e)}")
        return False, str(e)

def cleanup_file(filepath: str) -> None:
    """
    Remove temporary audio or image file.

    Args:
        filepath (str): Path to file to remove
    """
    try:
        if os.path.exists(filepath):
            logger.debug(f"Cleaning up file: {filepath}")
            os.remove(filepath)
            logger.info(f"Successfully removed file: {filepath}")
        else:
            logger.warning(f"File not found for cleanup: {filepath}")
    except Exception as e:
        logger.error(f"Error cleaning up file {filepath}: {str(e)}")