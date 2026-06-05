"""Exercices Matplotlib pour s'entraîner."""

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(8, 5))
plt.plot(x, y, label="sin(x)", color="blue")
plt.scatter(x[::10], y[::10], color="red", label="points")
plt.title("Exemple de courbe sin(x)")
plt.xlabel("x")
plt.ylabel("sin(x)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Histogramme
valeurs = np.random.normal(loc=0, scale=1, size=1000)
plt.figure(figsize=(8, 5))
plt.hist(valeurs, bins=20, color="green", edgecolor="black")
plt.title("Histogramme de valeurs normales")
plt.xlabel("Valeur")
plt.ylabel("Nombre")
plt.tight_layout()
plt.show()

print("Exercices Matplotlib terminés.")
