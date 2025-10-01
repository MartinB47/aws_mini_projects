import logging
import os
from typing import Dict, Any

# Import our modular components
from validation import validate_multipart_input
from bedrock_client import create_bedrock_payload, call_bedrock_model
from response_handler import create_success_response, create_error_response

# Configure logging with structured format for better CloudWatch analysis
logger = logging.getLogger()
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))


def parse_multipart_form_data(
    body: str, content_type: str
) -> tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Parse multipart form data from request body

    Args:
        body: Raw request body
        content_type: Content-Type header value

    Returns:
        tuple: (files_dict, form_data_dict)
    """
    files = {}
    form_data = {}

    # Extract boundary from content-type
    boundary = None
    for part in content_type.split(";"):
        part = part.strip()
        if part.startswith("boundary="):
            boundary = part.split("=", 1)[1]
            break

    if not boundary:
        raise ValueError("No boundary found in multipart data")

    # Split by boundary
    parts = body.split(f"--{boundary}")

    for part in parts:
        if not part.strip() or part.strip() == "--":
            continue

        # Split headers and content
        if "\r\n\r\n" in part:
            headers_part, content = part.split("\r\n\r\n", 1)
        else:
            continue

        # Parse headers
        headers = {}
        for line in headers_part.split("\r\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.strip().lower()] = value.strip()

        # Extract field name and filename
        content_disposition = headers.get("content-disposition", "")
        field_name = None
        filename = None

        for item in content_disposition.split(";"):
            item = item.strip()
            if item.startswith("name="):
                field_name = item.split("=", 1)[1].strip('"')
            elif item.startswith("filename="):
                filename = item.split("=", 1)[1].strip('"')

        if field_name:
            if filename:
                # It's a file
                files[field_name] = {
                    "filename": filename,
                    "content": content.rstrip("\r\n"),
                    "content_type": headers.get("content-type", "text/plain"),
                }
            else:
                # It's form data
                form_data[field_name] = content.rstrip("\r\n")

    return files, form_data


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda function handler for text translation using AWS Bedrock

    Only supports multipart form data with file uploads:
    - Multipart: file upload with target_language field

    Args:
        event: API Gateway event object
        context: Lambda context object

    Returns:
        dict: API Gateway response object (always text/plain)
    """
    # Log the incoming request (excluding sensitive data)
    logger.info(
        f"Processing translation request from {event.get('requestContext', {}).get('identity', {}).get('sourceIp', 'unknown')}"
    )

    try:
        # Check content type
        content_type = event.get("headers", {}).get("content-type", "") or event.get(
            "headers", {}
        ).get("Content-Type", "")

        if "multipart/form-data" not in content_type.lower():
            return create_error_response(
                400,
                "Only multipart/form-data is supported. Please upload a .txt file with target_language field.",
            )

        # Handle multipart form data (file upload)
        body = event.get("body", "")
        if event.get("isBase64Encoded", False):
            import base64

            body = base64.b64decode(body).decode("utf-8")

        files, form_data = parse_multipart_form_data(body, content_type)

        logger.info(
            f"Multipart request: files={list(files.keys())}, form_data={list(form_data.keys())}"
        )

        # Validate multipart input
        validation_error, text_content, target_language = validate_multipart_input(
            files, form_data
        )
        if validation_error:
            logger.warning(f"Input validation failed: {validation_error}")
            return create_error_response(400, validation_error)

        text = text_content

        # Create Bedrock payload
        bedrock_payload = create_bedrock_payload(text, target_language)

        # Call Bedrock model for translation
        translated_text, error_message = call_bedrock_model(bedrock_payload)

        if error_message:
            logger.error(f"Bedrock translation failed: {error_message}")
            return create_error_response(500, error_message)

        # Log successful translation (without content for privacy)
        logger.info(
            f"Translation successful: {len(text)} chars -> {len(translated_text)} chars"
        )

        # Return successful response (always text/plain)
        return create_success_response(text, translated_text, target_language)

    except ValueError as e:
        logger.error(f"Invalid multipart data: {str(e)}")
        return create_error_response(400, f"Invalid multipart data: {str(e)}")

    except KeyError as e:
        logger.error(f"Missing required field: {str(e)}")
        return create_error_response(400, f"Missing required field: {str(e)}")

    except Exception as e:
        # Log the full error for debugging but return generic message to user
        logger.error(f"Unexpected error in lambda_handler: {str(e)}", exc_info=True)
        return create_error_response(500, "Internal server error")
