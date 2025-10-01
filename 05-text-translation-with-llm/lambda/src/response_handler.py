"""
Response creation functions for API Gateway.
"""

from typing import Dict, Any, Optional


def create_success_response(
    original_text: str, translated_text: str, target_language: str
) -> Dict[str, Any]:
    """
    Create standardized success response (always returns text/plain)

    Args:
        original_text: Original input text
        translated_text: Translated text from Bedrock
        target_language: Target language

    Returns:
        dict: Formatted API Gateway response
    """
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/plain; charset=utf-8",
            "Content-Disposition": f"attachment; filename=translated_{target_language}.txt",
        },
        "body": translated_text,
    }


def create_error_response(
    status_code: int, error_message: str, details: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create standardized error response (always returns text/plain)

    Args:
        status_code: HTTP status code
        error_message: Human-readable error message
        details: Optional additional details

    Returns:
        dict: Formatted API Gateway error response
    """
    error_text = f"Error: {error_message}"
    if details:
        error_text += f"\nDetails: {details}"

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "text/plain; charset=utf-8",
        },
        "body": error_text,
    }
