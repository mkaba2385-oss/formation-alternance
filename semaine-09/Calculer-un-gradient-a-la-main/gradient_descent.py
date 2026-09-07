import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


def f(x: float, y: float) -> float:
    """Fonction à minimiser."""
    return (x - 3) ** 2 + 2 * y ** 2


def gradient(x: float, y: float) -> tuple[float, float]:
    """Calcule le gradient de f."""
    dx = 2 * (x - 3)
    dy = 4 * y

    return dx, dy


# 1. Vérification avec SymPy

x_symbol, y_symbol = sp.symbols("x y")

f_symbol = (x_symbol - 3) ** 2 + 2 * y_symbol ** 2

df_dx = sp.diff(f_symbol, x_symbol)
df_dy = sp.diff(f_symbol, y_symbol)

print("=== Vérification SymPy ===")
print("f(x, y) =", f_symbol)
print("∂f/∂x =", df_dx)
print("∂f/∂y =", df_dy)


# 2. Gradient descent

lr = 0.1
n_iterations = 5

x = 0.0
y = 0.0

trajectory = [(x, y)]

print("\n=== Gradient descent ===")
print(f"Point initial : ({x}, {y})")
print(f"f = {f(x, y)}")

for iteration in range(1, n_iterations + 1):
    dx, dy = gradient(x, y)

    print(
        f"\nItération {iteration}"
    )
    print(f"Gradient = ({dx}, {dy})")

    x = x - lr * dx
    y = y - lr * dy

    trajectory.append((x, y))

    print(f"Point = ({x}, {y})")
    print(f"f = {f(x, y)}")

# 3. Contour plot

x_values = np.linspace(-1, 4.5, 300)
y_values = np.linspace(-2.5, 2.5, 300)

X, Y = np.meshgrid(x_values, y_values)

Z = f(X, Y)

plt.figure(figsize=(8, 6))

contours = plt.contour(X, Y, Z, levels=20)
plt.clabel(contours, inline=True, fontsize=8)

trajectory_x = [point[0] for point in trajectory]
trajectory_y = [point[1] for point in trajectory]

plt.plot(
    trajectory_x,
    trajectory_y,
    marker="o",
    label="Gradient descent",
)

plt.scatter(
    trajectory_x[0],
    trajectory_y[0],
    marker="s",
    s=80,
    label="Départ",
)

plt.scatter(
    3,
    0,
    marker="*",
    s=150,
    label="Minimum",
)

plt.xlabel("x")
plt.ylabel("y")
plt.title("Gradient Descent sur f(x,y) = (x-3)² + 2y²")
plt.legend()
plt.grid(True)

plt.show()