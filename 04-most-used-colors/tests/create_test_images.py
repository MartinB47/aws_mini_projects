#!/usr/bin/env python3
"""
Script to create test images for color analysis testing.
"""

from PIL import Image, ImageDraw
import base64
import json
import io


def create_rgb_stripes():
    """Create an image with red, green, blue stripes."""
    img = Image.new("RGB", (300, 100), color="white")
    draw = ImageDraw.Draw(img)

    # Draw red stripe
    draw.rectangle([0, 0, 100, 100], fill="red")
    # Draw green stripe
    draw.rectangle([100, 0, 200, 100], fill="green")
    # Draw blue stripe
    draw.rectangle([200, 0, 300, 100], fill="blue")

    return img


def create_gradient():
    """Create a gradient image."""
    img = Image.new("RGB", (200, 200), color="white")
    draw = ImageDraw.Draw(img)

    # Create a gradient from red to blue
    for x in range(200):
        r = int(255 * (1 - x / 200))
        b = int(255 * (x / 200))
        draw.line([(x, 0), (x, 200)], fill=(r, 0, b))

    return img


def create_solid_colors():
    """Create an image with solid color blocks."""
    img = Image.new("RGB", (400, 100), color="white")
    draw = ImageDraw.Draw(img)

    colors = ["red", "green", "blue", "yellow", "purple"]
    for i, color in enumerate(colors):
        x1 = i * 80
        x2 = (i + 1) * 80
        draw.rectangle([x1, 0, x2, 100], fill=color)

    return img


def save_image_and_create_event(img, filename, description):
    """Save image and create corresponding event file."""
    # Save image
    img_path = f"tests/events/{filename}.png"
    img.save(img_path)

    # Convert to base64
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

    # Create event
    event = {"body": img_base64}

    # Save event
    event_path = f"tests/events/{filename}_event.json"
    with open(event_path, "w") as f:
        json.dump(event, f, indent=2)

    print(f"Created {img_path} and {event_path}")
    print(f"Description: {description}")
    print(f"Image size: {img.size}")
    print("-" * 50)


def main():
    """Create all test images and events."""
    print("Creating test images and events...")
    print("=" * 50)

    # Create RGB stripes
    rgb_img = create_rgb_stripes()
    save_image_and_create_event(rgb_img, "rgb_stripes", "Red, green, blue stripes")

    # Create gradient
    gradient_img = create_gradient()
    save_image_and_create_event(gradient_img, "gradient", "Red to blue gradient")

    # Create solid colors
    solid_img = create_solid_colors()
    save_image_and_create_event(
        solid_img,
        "solid_colors",
        "Solid color blocks: red, green, blue, yellow, purple",
    )

    print("\nTest files created successfully!")
    print("\nTo test with SAM local invoke:")
    print("sam local invoke ColorAnalysisFunction -e tests/events/rgb_stripes_event.json")
    print("sam local invoke ColorAnalysisFunction -e tests/events/gradient_event.json")
    print("sam local invoke ColorAnalysisFunction -e tests/events/solid_colors_event.json")


if __name__ == "__main__":
    main()
