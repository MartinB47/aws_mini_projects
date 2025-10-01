"""
Configuration constants and supported languages for the translation service.
"""

import os

BEDROCK_MODEL_ID = os.getenv(
    "BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"
)
MAX_TEXT_LENGTH = 10000
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB max file size
ALLOWED_FILE_EXTENSIONS = [".txt"]

# Supported languages mapping (lowercase key -> display name)
SUPPORTED_LANGUAGES = {
    "english": "English",
    "spanish": "Spanish",
    "french": "French",
    "german": "German",
    "italian": "Italian",
    "portuguese": "Portuguese",
    "chinese": "Chinese",
    "japanese": "Japanese",
    "korean": "Korean",
    "russian": "Russian",
    "arabic": "Arabic",
}
