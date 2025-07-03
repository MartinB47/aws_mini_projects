def lambda_handler(event, context):
    """
    AWS Lambda handler function for the Hello World API endpoint.

    Args:
        event (dict): The event dict containing request data.
        context (LambdaContext): The runtime information of the Lambda function.

    Returns:
        dict: The HTTP response with status code, headers, and body.
    """
    # Return a simple HTTP 200 response with a plain text body
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/plain"},
        "body": "Hello World!",
    }
