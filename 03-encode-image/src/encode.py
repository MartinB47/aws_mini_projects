import numpy as np
import io
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def message_to_bits(message):
    if isinstance(message, str):
        bits = np.unpackbits(np.frombuffer(message, dtype=np.uint8))
    else:
        raise ValueError("Message must be a string")
    return bits


def bits_to_square_matrix(bits):
    length = len(bits)
    side = int(np.ceil(np.sqrt(length)))
    padded_bits = np.pad(bits, (0, side * side - length), "constant", constant_values=0)
    matrix = padded_bits.reshape((side, side))
    return matrix


def plot_image(matrix) -> io.BytesIO:
    side = matrix.shape[0]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(matrix, cmap="binary", interpolation="none")

    ax.set_xticks([])
    ax.set_yticks([])
    ax.gca().set_xticks(np.arange(-0.5, side, 1), minor=True)
    ax.gca().set_yticks(np.arange(-0.5, side, 1), minor=True)
    ax.grid(which="minor", color="lightgray", linestyle="-", linewidth=0.5)
    ax.set_title(f"Encoded message as {side}×{side} matrix")
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150)
    buf.seek(0)
    plt.close(fig)
    return buf


def encode_message_to_matrix(message):
    bits = message_to_bits(message)
    matrix = bits_to_square_matrix(bits)
    return matrix
