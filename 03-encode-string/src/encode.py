import numpy as np
import io
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def message_to_bits(message: str) -> np.ndarray:
    """Convert a message to a binary bit array.

    Args:
        message: A string or bytes-like object to convert to bits

    Returns:
        numpy.ndarray: A 1D array of binary bits (0s and 1s)

    Raises:
        ValueError: If message is not a string or bytes-like object
    """
    if isinstance(message, str):
        message = message.encode("utf-8")
    # Convert bytes to binary bit array
    bits = np.unpackbits(np.frombuffer(message, dtype=np.uint8))
    return bits


def bits_to_square_matrix(bits: np.ndarray) -> np.ndarray:
    """Convert a bit array to a square matrix.

    Args:
        bits: A 1D array of binary bits (0s and 1s)

    Returns:
        numpy.ndarray: A 2D square matrix of bits

    Raises:
        ValueError: If bits is not a 1D array of binary bits
    """
    length = len(bits)
    side = int(np.ceil(np.sqrt(length)))
    padded_bits = np.pad(bits, (0, side * side - length), "constant", constant_values=0)
    matrix = padded_bits.reshape((side, side))
    return matrix


def plot_image(matrix: np.ndarray) -> io.BytesIO:
    side = matrix.shape[0]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(matrix, cmap="binary", interpolation="none")

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticks(np.arange(-0.5, side, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, side, 1), minor=True)
    ax.grid(which="minor", color="lightgray", linestyle="-", linewidth=0.5)
    ax.set_title(f"Encoded message as {side}×{side} matrix")
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150)
    buf.seek(0)
    plt.close(fig)
    return buf


def encode_message_to_matrix(message: str) -> np.ndarray:
    """Encode a message to a square matrix representation.

    This function converts a message to binary bits and then arranges them
    in a square matrix format, padding with zeros if necessary.

    Args:
        message: The message to encode as a string

    Returns:
        numpy.ndarray: A 2D square matrix containing the encoded message bits
    """
    bits = message_to_bits(message)
    matrix = bits_to_square_matrix(bits)
    return matrix
