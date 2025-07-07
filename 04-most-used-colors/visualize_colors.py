#!/usr/bin/env python3
"""
Script to visualize color analysis results from JSON file.
Displays the top 5 dominant colors as rectangles.
"""

import json
import sys
import argparse
from PIL import Image, ImageDraw


def visualize_colors(colors, output_path=None, width=800, height=200):
    """
    Create a visualization of the dominant colors.

    Args:
        colors: List of RGB color tuples
        output_path: Path to save the image (optional)
        width: Width of the output image
        height: Height of the output image
    """
    # Create a new image with white background
    img = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(img)

    # Calculate rectangle dimensions
    rect_width = width // len(colors)
    rect_height = height

    print(f"Visualizing {len(colors)} colors:")

    # Draw rectangles for each color
    for i, color in enumerate(colors):
        x1 = i * rect_width
        x2 = (i + 1) * rect_width
        # Ensure color is a tuple of ints
        color_tuple = tuple(int(c) for c in color)
        # Draw the color rectangle
        draw.rectangle([x1, 0, x2, rect_height], fill=color_tuple)
        # Print color info
        hex_color = "#{:02x}{:02x}{:02x}".format(*color_tuple)
        print(f"  {i+1}. RGB: {color_tuple} | Hex: {hex_color}")

    # Save or show the image
    if output_path:
        img.save(output_path)
        print(f"\nColor visualization saved to: {output_path}")
    else:
        img.show()
        print("\nColor visualization displayed.")


def main():
    parser = argparse.ArgumentParser(description="Visualize color analysis results")
    parser.add_argument("input_file", help="Path to JSON file with color data")
    parser.add_argument("-o", "--output", help="Output image path (optional)")
    parser.add_argument(
        "-w", "--width", type=int, default=800, help="Image width (default: 800)"
    )
    parser.add_argument(
        "--height", type=int, default=200, help="Image height (default: 200)"
    )

    args = parser.parse_args()

    try:
        # Read JSON file
        with open(args.input_file, "r") as f:
            data = json.load(f)

        # Extract colors
        if "colors" in data:
            colors = data["colors"]
        else:
            print("Error: JSON file must contain a 'colors' field")
            sys.exit(1)

        # Validate colors
        if not colors or len(colors) == 0:
            print("Error: No colors found in JSON file")
            sys.exit(1)

        # Visualize colors
        visualize_colors(colors, args.output, args.width, args.height)

    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file '{args.input_file}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
