"""
Input validation functions for the translation service.
"""

from typing import Dict, Any, Optional, Tuple
from constants import (
    MAX_TEXT_LENGTH,
    MAX_FILE_SIZE,
    ALLOWED_FILE_EXTENSIONS,
    SUPPORTED_LANGUAGES,
)


def validate_multipart_input(
    files: Dict[str, Any], form_data: Dict[str, Any]
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Validate multipart form data input

    Args:
        files: Dictionary containing uploaded files
        form_data: Dictionary containing form fields

    Returns:
        tuple: (error_message, text_content, target_language)
    """
    # Check required fields
    if "file" not in files:
        return "Missing required field: 'file'", None, None

    if "target_language" not in form_data:
        return "Missing required field: 'target_language'", None, None

    file_data = files["file"]
    target_language = form_data["target_language"]

    # Validate target language
    if not isinstance(target_language, str):
        return "Target language must be a string", None, None

    # Normalize language input (case-insensitive)
    normalized_language = target_language.lower().strip()
    if normalized_language not in SUPPORTED_LANGUAGES:
        supported_list = ", ".join(SUPPORTED_LANGUAGES.keys())
        return (
            f"Unsupported target language. Supported languages: {supported_list}",
            None,
            None,
        )

    # Validate file
    if not isinstance(file_data, dict) or "content" not in file_data:
        return "Invalid file data", None, None

    file_content = file_data["content"]
    filename = file_data.get("filename", "")

    # Check file extension
    if not any(filename.lower().endswith(ext) for ext in ALLOWED_FILE_EXTENSIONS):
        return (
            f"Only {', '.join(ALLOWED_FILE_EXTENSIONS)} files are allowed",
            None,
            None,
        )

    # Check file size
    if len(file_content) > MAX_FILE_SIZE:
        return (
            f"File size exceeds maximum of {MAX_FILE_SIZE // (1024*1024)}MB",
            None,
            None,
        )

    # Validate text content
    if not isinstance(file_content, str) or not file_content.strip():
        return "File must contain non-empty text", None, None

    # Check text length to prevent API limits
    if len(file_content) > MAX_TEXT_LENGTH:
        return (
            f"Text exceeds maximum length of {MAX_TEXT_LENGTH} characters",
            None,
            None,
        )

    return None, file_content.strip(), normalized_language
