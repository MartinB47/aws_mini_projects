import base64, json, os, uuid
import boto3
from src.encode import encode_message_to_matrix, plot_image

S3_BUCKET = os.environ.get("BUCKET")
s3 = boto3.client("s3")
INLINE_MAX = 5_000_000


def respond_png(img_bytes: bytes):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "image/png"},
        "isBase64Encoded": True,
        "body": base64.b64encode(img_bytes).decode(),
    }


def respond_url(key):
    url = s3.generate_presigned_url(
        "get_object", Params={"Bucket": S3_BUCKET, "Key": key}, ExpiresIn=600
    )
    return {"statusCode": 200, "body": json.dumps({"url": url})}


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

    if len(img_bytes) <= INLINE_MAX or not S3_BUCKET:
        # Put image in payload as base64
        return respond_png(img_bytes)

    # Write to s3, presign, and return the link
    key = f"{uuid.uuid4()}.png"
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=img_bytes, ContentType="image/png")
    return respond_url(key)
