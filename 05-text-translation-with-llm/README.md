# Text Translation with LLM

This project provides a simple command-line tool to translate text files using the Ollama LLM (Large Language Model) with the `gemma3n:e4b` model.

## Description

The script translates the contents of a `.txt` file into a specified target language by invoking the Ollama CLI. The translation is performed locally using the specified model.

## How it Works

- The script reads a UTF-8 encoded `.txt` file.
- It sends the text to the Ollama model for translation into the target language.
- The translated text is written to an output file. By default, the output is saved in the `outputs/` directory with the same base name as the input file.
- Only `.txt` files are accepted as input.

## Usage

1. Ensure you have [Ollama](https://ollama.com/) installed and running.
2. Place your input `.txt` file in the desired location.
3. Run the script using Python 3:

### Basic usage (default output path)

```
python translate.py <target_language> <input_file.txt>
```

Example:
```
python translate.py Spanish texts/example.txt
```
This will write the translation to `outputs/example.txt`.

### Custom output path

```
python translate.py <target_language> <input_file.txt> <output_file.txt>
```

Example:
```
python translate.py German texts/example.txt my_german_translation.txt
```

## Requirements
- Python 3.7+
- Ollama CLI installed and accessible in your PATH 