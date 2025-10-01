"""
Bedrock client and inference functions for text translation.
"""

import json
import boto3
import logging
import os
from typing import Dict, Any, Optional, Tuple
from botocore.exceptions import ClientError, BotoCoreError
from constants import BEDROCK_MODEL_ID, SUPPORTED_LANGUAGES

# Configure logging
logger = logging.getLogger()

# Initialize Bedrock client with error handling
try:
    bedrock_runtime = boto3.client(
        "bedrock-runtime", region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    logger.info("Bedrock client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Bedrock client: {str(e)}")
    bedrock_runtime = None


def create_bedrock_payload(text: str, target_language: str) -> Dict[str, Any]:
    """
    Create properly formatted payload for Bedrock Claude model

    Args:
        text: Text to translate
        target_language: Target language for translation

    Returns:
        dict: Formatted payload for Bedrock API
    """
    # Construct a clear, specific prompt for translation
    prompt = f"""Please translate the following text to {SUPPORTED_LANGUAGES[target_language.lower()]}. 
Only return the translated text, no explanations or additional commentary.

Text to translate: {text}

Translation:"""

    # Claude 3 model payload format
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4000,  # Generous limit for translations
        "temperature": 0.1,  # Low temperature for consistent translations
        "messages": [{"role": "user", "content": prompt}],
    }

    return payload


def call_bedrock_model(payload: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    """
    Make API call to Bedrock model with comprehensive error handling

    Args:
        payload: Formatted payload for Bedrock

    Returns:
        tuple: (translated_text, error_message)
    """
    if bedrock_runtime is None:
        return None, "Bedrock client not initialized"

    try:
        logger.info(f"Calling Bedrock model: {BEDROCK_MODEL_ID}")

        # Make the API call to Bedrock
        response = bedrock_runtime.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            body=json.dumps(payload),
            contentType="application/json",
            accept="application/json",
        )

        # Parse the response
        response_body = json.loads(response["body"].read())
        logger.debug(f"Bedrock response: {response_body}")

        # Extract translated text from Claude response format
        if "content" in response_body and len(response_body["content"]) > 0:
            translated_text = response_body["content"][0]["text"].strip()

            if translated_text:
                logger.info("Translation completed successfully")
                return translated_text, None
            else:
                return None, "Empty translation received from Bedrock"
        else:
            logger.error(f"Unexpected response format: {response_body}")
            return None, "Invalid response format from Bedrock"

    except ClientError as e:
        # AWS service-specific errors
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]

        if error_code == "AccessDeniedException":
            logger.error("Access denied to Bedrock model - check IAM permissions")
            return None, "Access denied to translation service"
        elif error_code == "ThrottlingException":
            logger.error("Bedrock API throttling - too many requests")
            return (
                None,
                "Translation service temporarily unavailable - please try again",
            )
        elif error_code == "ValidationException":
            logger.error(f"Bedrock validation error: {error_message}")
            return None, "Invalid request format"
        else:
            logger.error(f"Bedrock ClientError: {error_code} - {error_message}")
            return None, "Translation service error"

    except BotoCoreError as e:
        # Network, credentials, or configuration errors
        logger.error(f"Bedrock BotoCoreError: {str(e)}")
        return None, "Translation service connection error"

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Bedrock response: {str(e)}")
        return None, "Invalid response from translation service"

    except Exception as e:
        # Catch-all for unexpected errors
        logger.error(f"Unexpected error calling Bedrock: {str(e)}")
        return None, "Unexpected translation service error"
