#!/usr/bin/env python3
"""
Direct test of the Lambda handler function to debug image validation issues.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import json
from app import lambda_handler


def test_with_rgb_stripes():
    """Test with the RGB stripes image."""
    # Read the existing event file
    with open("events/rgb_stripes_event.json", "r") as f:
        event = json.load(f)

    print("\nTesting with RGB stripes image...")
    print(f"Base64 length: {len(event['body'])}")
    print(f"Base64 starts with: {event['body'][:20]}...")

    result = lambda_handler(event, None)
    print(f"Status Code: {result['statusCode']}")
    print(f"Response: {result['body']}")

    if result["statusCode"] == 200:
        response_body = json.loads(result["body"])
        print("\nTop 5 dominant colors:")
        for i, color in enumerate(response_body["colors"], 1):
            print(f"{i}. RGB: {color}")
    else:
        print(f"Error: {result['body']}")


if __name__ == "__main__":
    print("=== Direct Lambda Handler Tests ===\n")
    test_with_rgb_stripes()
