import json, boto3, os
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, _):
    # Extract HTTP path and method from API Gateway event structure
    path = event.get("rawPath", "") or event.get("requestContext", {}).get(
        "http", {}
    ).get("path", "")
    method = event.get("requestContext", {}).get("http", {}).get("method", "")

    # Increment counter
    if path == "/counter/increment" and method == "POST":
        resp = table.update_item(
            Key={"id": "counter"},
            UpdateExpression="ADD #v :inc",
            ExpressionAttributeNames={"#v": "value"},
            ExpressionAttributeValues={":inc": Decimal(1)},
            ReturnValues="UPDATED_NEW",
        )
        count = int(resp["Attributes"]["value"])

    # Get count
    elif path == "/counter" and method == "GET":
        item = table.get_item(Key={"id": "counter"}).get("Item", {})
        count = int(item.get("value", 0))

    # Reset count
    elif path == "/counter/reset" and method == "POST":
        table.put_item(Item={"id": "counter", "value": 0})
        count = 0
    else:
        return {"statusCode": 400, "body": "Bad route or method"}
    return {"statusCode": 200, "body": json.dumps({"count": count})}
