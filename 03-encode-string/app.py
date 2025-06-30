import base64, json
from src.encode import encode_message_to_matrix, plot_image


def respond_png(img_bytes: bytes):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "image/png"},
        "isBase64Encoded": True,
        "body": base64.b64encode(img_bytes).decode(),
    }


def lambda_handler(event, _):
    # Read text payload
    body = event.get("body", "")
    if event.get("isBase64Encoded"):
        body = base64.b64decode(body).decode()

    message = body if isinstance(body, str) else json.loads(body)["message"]

    # Get the matrix of the message
    matrix = encode_message_to_matrix(message)

    # Convert matrix to PNG bytes
    png_buffer = plot_image(matrix)
    img_bytes = png_buffer.getvalue()

    # Always return the image as base64 in the response
    return respond_png(img_bytes)
