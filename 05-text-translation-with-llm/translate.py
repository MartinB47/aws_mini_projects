#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path


def translate(text: str, target_language: str) -> str:
    """
    Call Ollama CLI to translate `text` into `target_language`
    using the gemma3n:e4b model.
    """
    prompt = f"Translate the following text to {target_language}:\n\n" f"{text}"
    # Run the model; will pull if not present
    result = subprocess.run(
        ["ollama", "run", "gemma3n:e4b", prompt], capture_output=True, text=True
    )
    if result.returncode != 0:
        # If Ollama returns an error, print stderr and exit
        sys.stderr.write("Ollama error:\n" + result.stderr)
        sys.exit(result.returncode)
    return result.stdout.strip()


def main():
    parser = argparse.ArgumentParser(
        description="Translate text using Ollama gemma3n:e4b model"
    )
    parser.add_argument(
        "target_language", help="Language to translate into (e.g. 'Spanish', 'German')"
    )
    parser.add_argument(
        "input_file", type=Path, help="Path to the UTF-8 text file to translate"
    )
    parser.add_argument(
        "output_file", type=Path, nargs="?", default=None,
        help="Path where the translated text will be written (default: outputs/{basename of input file}.txt)"
    )
    args = parser.parse_args()

    # Only accept .txt files
    if args.input_file.suffix.lower() != ".txt":
        sys.exit(f"Input file must have a .txt extension: {args.input_file}")

    # Read input
    if not args.input_file.exists():
        sys.exit(f"Input file not found: {args.input_file}")
    text = args.input_file.read_text(encoding="utf-8")

    # Perform translation
    translation = translate(text, args.target_language)

    # Determine output path
    if args.output_file is None:
        output_dir = Path("outputs")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / (args.input_file.stem + ".txt")
    else:
        output_file = args.output_file
        output_dir = output_file.parent
        if output_dir and not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)

    # Write output
    output_file.write_text(translation, encoding="utf-8")
    print(f"✅ Translation complete. Output written to {output_file}")


if __name__ == "__main__":
    main()