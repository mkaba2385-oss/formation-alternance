from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def load_image(path: str | Path) -> np.ndarray:
    """
    Charge une image RGB et la transforme en tableau NumPy.

    Retour :
        tableau de shape (H, W, 3)
    """
    image = Image.open(path).convert("RGB")

    return np.array(image)


def save_image(array: np.ndarray, path: str | Path) -> None:
    """
    Sauvegarde un tableau NumPy sous forme d'image.
    """
    array = np.clip(array, 0, 255).astype(np.uint8)

    image = Image.fromarray(array)

    image.save(path)


def rgb_to_grayscale(image: np.ndarray) -> np.ndarray:
    """
    Convertit une image RGB en niveaux de gris
    avec la formule ITU-R BT.601.
    """
    red = image[:, :, 0]
    green = image[:, :, 1]
    blue = image[:, :, 2]

    grayscale = (
        0.299 * red
        + 0.587 * green
        + 0.114 * blue
    )

    return np.clip(grayscale, 0, 255).astype(np.uint8)


def gaussian_kernel_5x5() -> np.ndarray:
    """
    Retourne un kernel gaussien 5x5.
    """
    kernel = np.array(
        [
            [1, 4, 6, 4, 1],
            [4, 16, 24, 16, 4],
            [6, 24, 36, 24, 6],
            [4, 16, 24, 16, 4],
            [1, 4, 6, 4, 1],
        ],
        dtype=np.float64,
    )

    return kernel / kernel.sum()


def gaussian_blur(image: np.ndarray) -> np.ndarray:
    """
    Applique un flou gaussien avec un kernel 5x5.

    Le calcul de convolution est réalisé manuellement
    avec NumPy, sans OpenCV ni scikit-image.
    """
    kernel = gaussian_kernel_5x5()

    padded = np.pad(
        image,
        pad_width=2,
        mode="edge",
    )

    height, width = image.shape

    result = np.zeros(
        (height, width),
        dtype=np.float64,
    )

    for i in range(height):
        for j in range(width):
            window = padded[i : i + 5, j : j + 5]

            result[i, j] = np.sum(window * kernel)

    return np.clip(result, 0, 255).astype(np.uint8)


def sobel_edges(image: np.ndarray) -> np.ndarray:
    """
    Détecte les contours avec les kernels de Sobel.
    """
    kernel_x = np.array(
        [
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1],
        ],
        dtype=np.float64,
    )

    kernel_y = np.array(
        [
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1],
        ],
        dtype=np.float64,
    )

    padded = np.pad(
        image,
        pad_width=1,
        mode="edge",
    )

    height, width = image.shape

    gradient_x = np.zeros(
        (height, width),
        dtype=np.float64,
    )

    gradient_y = np.zeros(
        (height, width),
        dtype=np.float64,
    )

    for i in range(height):
        for j in range(width):
            window = padded[i : i + 3, j : j + 3]

            gradient_x[i, j] = np.sum(window * kernel_x)
            gradient_y[i, j] = np.sum(window * kernel_y)

    magnitude = np.sqrt(
        gradient_x**2 + gradient_y**2
    )

    magnitude = np.clip(magnitude, 0, 255)

    return magnitude.astype(np.uint8)


def color_histogram(image: np.ndarray) -> dict[str, np.ndarray]:
    """
    Calcule l'histogramme des trois canaux RGB.

    Retourne 256 valeurs pour chaque canal.
    """
    histogram: dict[str, np.ndarray] = {}

    histogram["red"] = np.bincount(
        image[:, :, 0].ravel(),
        minlength=256,
    )

    histogram["green"] = np.bincount(
        image[:, :, 1].ravel(),
        minlength=256,
    )

    histogram["blue"] = np.bincount(
        image[:, :, 2].ravel(),
        minlength=256,
    )

    return histogram


def save_histogram(
    histogram: dict[str, np.ndarray],
    path: str | Path,
) -> None:
    """
    Crée une image représentant l'histogramme RGB.
    """
    width = 768
    height = 400

    canvas = Image.new(
        "RGB",
        (width, height),
        "white",
    )

    draw = ImageDraw.Draw(canvas)

    max_value = max(
        int(histogram["red"].max()),
        int(histogram["green"].max()),
        int(histogram["blue"].max()),
    )

    if max_value == 0:
        max_value = 1

    # Trois zones : rouge, vert, bleu
    channels = [
        ("red", 0),
        ("green", 256),
        ("blue", 512),
    ]

    for channel, offset in channels:
        values = histogram[channel]

        for x in range(256):
            value = values[x]

            bar_height = int(
                value / max_value * 300
            )

            x1 = offset + x
            y1 = height - bar_height
            x2 = x1
            y2 = height

            draw.line(
                (x1, y1, x2, y2),
                fill=channel,
                width=1,
            )

    canvas.save(path)


def main() -> None:
    input_path = Path("image_entree.png")
    output_dir = Path("output")

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------
    # 1. Chargement
    # --------------------------------------------------

    image = load_image(input_path)

    print("Image chargée")
    print(f"Shape : {image.shape}")
    print(f"Type : {image.dtype}")

    # --------------------------------------------------
    # 2. Niveaux de gris
    # --------------------------------------------------

    grayscale = rgb_to_grayscale(image)

    save_image(
        grayscale,
        output_dir / "grayscale.png",
    )

    print("Grayscale sauvegardé")

    # --------------------------------------------------
    # 3. Flou gaussien
    # --------------------------------------------------

    blur = gaussian_blur(grayscale)

    save_image(
        blur,
        output_dir / "blur.png",
    )

    print("Flou gaussien sauvegardé")

    # --------------------------------------------------
    # 4. Détection de contours
    # --------------------------------------------------

    edges = sobel_edges(grayscale)

    save_image(
        edges,
        output_dir / "edges.png",
    )

    print("Contours sauvegardés")

    # --------------------------------------------------
    # 5. Histogramme
    # --------------------------------------------------

    histogram = color_histogram(image)

    save_histogram(
        histogram,
        output_dir / "histogram.png",
    )

    print("Histogramme sauvegardé")

    print("\nTraitement terminé.")


if __name__ == "__main__":
    main()