import timeit

import numpy as np

def distances_naive(points: np.ndarray) -> np.ndarray:
    """
    Calcule les distances entre toutes les paires de points
    avec deux boucles Python.
    """
    n = len(points)

    distances = np.zeros((n, n), dtype=np.float64)

    for i in range(n):
        for j in range(n):
            dx = points[i, 0] - points[j, 0]
            dy = points[i, 1] - points[j, 1]

            distances[i, j] = np.sqrt(dx**2 + dy**2)

    return distances


def distances_vectorisees(points: np.ndarray) -> np.ndarray:
    """
    Calcule les distances entre toutes les paires de points
    avec NumPy et le broadcasting.
    """
    differences = points[:, np.newaxis, :] - points[np.newaxis, :, :]

    distances = np.sqrt(np.sum(differences**2, axis=2))

    return distances


def main() -> None:
    
    rng = np.random.default_rng(42)

    points = rng.random((1000, 2))

    # Vérification des résultats
    distances_1 = distances_naive(points)
    distances_2 = distances_vectorisees(points)

    print("Shape des résultats :", distances_1.shape)

    print(
        "Les deux résultats sont identiques :",
        np.allclose(distances_1, distances_2),
    )

    # Mesure de la version naïve
    temps_naif = timeit.timeit(
        lambda: distances_naive(points),
        number=5,
    )

    # Mesure de la version vectorisée
    temps_vectorise = timeit.timeit(
        lambda: distances_vectorisees(points),
        number=5,
    )

    print("\n--- Mesure des performances ---")
    print(f"Version naïve      : {temps_naif:.4f} secondes")
    print(f"Version vectorisée : {temps_vectorise:.4f} secondes")

    if temps_vectorise > 0:
        acceleration = temps_naif / temps_vectorise
        print(f"Accélération        : x{acceleration:.2f}")


if __name__ == "__main__":
    main()