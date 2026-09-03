import matplotlib.pyplot as plt
import numpy as np


# Données

mois = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin"]
ventes = [1200, 1500, 1350, 1800, 2100, 2300]
clients = [80, 95, 90, 110, 125, 140]

prix_moyens = [15, 16, 15, 17, 18, 19]

# Données pour l'histogramme
montants_commandes = [
    12, 15, 18, 20, 22, 25, 28, 30, 32, 35,
    15, 18, 21, 23, 26, 29, 31, 34, 36, 40,
    14, 17, 19, 22, 24, 27, 30, 33, 37, 42,
    16, 20, 23, 25, 28, 32, 35, 38, 41, 45
]


# Création de la figure

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

fig.suptitle(
    "Dashboard des ventes",
    fontsize=18,
    fontweight="bold"
)


# 1. Bar chart

ax1 = axes[0, 0]

ax1.bar(
    mois,
    ventes,
    color="steelblue",
    label="Ventes"
)

ax1.set_title("Ventes par mois")
ax1.set_xlabel("Mois")
ax1.set_ylabel("Montant des ventes (€)")
ax1.legend()

ax1.grid(
    axis="y",
    linestyle="--",
    alpha=0.3
)

# 2. Line chart

ax2 = axes[0, 1]

ax2.plot(
    mois,
    clients,
    marker="o",
    linewidth=2,
    color="darkorange",
    label="Nombre de clients"
)

ax2.set_title("Évolution du nombre de clients")
ax2.set_xlabel("Mois")
ax2.set_ylabel("Nombre de clients")
ax2.legend()

ax2.grid(
    linestyle="--",
    alpha=0.3
)


# 3. Scatter plot

ax3 = axes[1, 0]

ax3.scatter(
    clients,
    ventes,
    s=80,
    color="seagreen",
    alpha=0.8,
    label="Mois"
)

ax3.set_title("Relation entre clients et ventes")
ax3.set_xlabel("Nombre de clients")
ax3.set_ylabel("Ventes (€)")
ax3.legend()

ax3.grid(
    linestyle="--",
    alpha=0.3
)


# =========================
# 4. Histogramme
# =========================

ax4 = axes[1, 1]

ax4.hist(
    montants_commandes,
    bins=8,
    color="mediumpurple",
    edgecolor="black",
    alpha=0.8,
    label="Commandes"
)

ax4.set_title("Distribution des montants des commandes")
ax4.set_xlabel("Montant de la commande (€)")
ax4.set_ylabel("Nombre de commandes")
ax4.legend()

ax4.grid(
    axis="y",
    linestyle="--",
    alpha=0.3
)



# Mise en page

plt.tight_layout()

fig.subplots_adjust(top=0.90)


# Sauvegarde

plt.savefig(
    "dashboard_ventes.png",
    dpi=150,
    bbox_inches="tight"
)

plt.show()