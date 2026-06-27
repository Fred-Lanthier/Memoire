#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figure du protocole d'échantillonnage des cibles (chapitre Design du système).

Schéma vue de dessus, exprimé dans le repère robot F_r :
  - grille 3x3 des 9 positions de l'assiette ;
  - dans chaque assiette, les 5 positions de cible en quinconce ;
  - repère robot F_r à l'origine (axes seulement) ;
  - flèche : champ de vision de la caméra à l'effecteur.

Tout est paramétrique : ajuster les valeurs ci-dessous reflète le protocole réel.
Exporte un PDF vecteur (style mémoire : Okabe-Ito, français, sans titre).
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# ----------------------------------------------------------------------
# Palette Okabe-Ito (cohérente avec le style du mémoire)
# ----------------------------------------------------------------------
OI = dict(orange="#E69F00", skyblue="#56B4E9", green="#009E73",
          yellow="#F0E442", blue="#0072B2", vermillion="#D55E00",
          purple="#CC79A7", black="#000000", grey="#999999")

plt.rcParams.update({
    "font.size": 9, "font.family": "serif",
    "svg.fonttype": "none",          # texte fidèle aux polices LaTeX
    "axes.linewidth": 0.8,
})

# ----------------------------------------------------------------------
# PARAMÈTRES DU PROTOCOLE  (← à confirmer avec les valeurs réelles)
# ----------------------------------------------------------------------
COLS_X        = [0.32, 0.40, 0.48]   # m, colonnes gauche / centre / droite (axe x_b)
ROWS_Y        = [0.20, 0.00, -0.20]  # m, rangées haut / centre / bas (axe y_b)
PLATE_RADIUS  = 0.130     # m, rayon de l'assiette (diamètre 26 cm)
TARGET_OFFSET = 0.060     # m, demi-écart du quinconce (points périphériques proches du bord)

# Quinconce : 4 points + centre (repère assiette)
quinc = np.array([[0, 0],
                  [ TARGET_OFFSET,  TARGET_OFFSET],
                  [-TARGET_OFFSET,  TARGET_OFFSET],
                  [-TARGET_OFFSET, -TARGET_OFFSET],
                  [ TARGET_OFFSET, -TARGET_OFFSET]])

# Les 9 positions se chevauchent (assiettes de 26 cm) : on n'illustre que la
# diagonale représentative — supérieur droit, centre, inférieur gauche.
plates = [(COLS_X[2], ROWS_Y[0]),   # supérieur droit
          (COLS_X[1], ROWS_Y[1]),   # centre
          (COLS_X[0], ROWS_Y[2])]   # inférieur gauche

# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(5.4, 4.3))

# lignes tiretées noires traversant tout le graphique : TOUTES les positions
# possibles du centre de l'assiette (les 9 intersections de la grille 3x3)
for xc in COLS_X:
    ax.axvline(xc, color=OI["black"], lw=0.7, ls=(0, (5, 4)), zorder=1)
for yc in ROWS_Y:
    ax.axhline(yc, color=OI["black"], lw=0.7, ls=(0, (5, 4)), zorder=1)

# assiettes représentatives : cercles bleus pleins + quinconce des cibles
for x, y in plates:
    ax.add_patch(Circle((x, y), PLATE_RADIUS, fill=False,
                        ec=OI["blue"], lw=1.2, zorder=3))
    ax.scatter(x + quinc[:, 0], y + quinc[:, 1], s=5,
               color=OI["vermillion"], zorder=4)

# --- repère base du robot à l'origine (axes seulement) ---
L = 0.075
ax.annotate("", xy=(L, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color=OI["black"], lw=1.3))
ax.annotate("", xy=(0, L), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color=OI["black"], lw=1.3))
_bb = dict(fc="white", ec="none", pad=0.5)
ax.text(L + 0.006, 0, "$x_b$", va="center", fontsize=9, bbox=_bb, zorder=5)
ax.text(0, L + 0.008, "$y_b$", ha="center", fontsize=9, bbox=_bb, zorder=5)

# --- limites : assiettes entièrement visibles ---
ax.set_xlim(-0.07, max(COLS_X) + PLATE_RADIUS + 0.04)
ax.set_ylim(min(ROWS_Y) - PLATE_RADIUS - 0.05,
            max(ROWS_Y) + PLATE_RADIUS + 0.06)
ax.set_aspect("equal")
ax.set_xlabel("Positions d'assiette dans le repère robot\n"
              "(3 des 9 positions de la grille $3\\times3$ illustrées)",
              fontsize=8)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)

fig.tight_layout()
out = "protocole_echantillonnage"
fig.savefig(out + ".pdf", bbox_inches="tight")   # vecteur, inclus dans le mémoire
fig.savefig(out + ".svg", bbox_inches="tight")
fig.savefig(out + ".png", dpi=200, bbox_inches="tight")
print("écrit :", out + ".pdf / .svg / .png")
