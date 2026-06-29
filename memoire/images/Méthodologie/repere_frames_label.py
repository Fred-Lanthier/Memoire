#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Étape 2 : étiquetage de l'image rendue par repere_frames.py.
Pur matplotlib (sans Open3D / X) : charge l'image brute + les données de repères,
projette chaque origine en pixels et superpose les étiquettes {b}{e}{c}{f} + légende.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

plt.rcParams.update({"font.family": "serif", "svg.fonttype": "none"})

arr = mpimg.imread("repere_frames_raw.png")
d = np.load("repere_frames_data.npz", allow_pickle=True)
names = list(d["names"]); origins = d["origins"]
ex, ey, ez, cx, cy, cz, ux, uy, uz, VFOV, W, H = d["cam"]
EYE, CENTER, UP = [ex, ey, ez], [cx, cy, cz], [ux, uy, uz]


def project(P, eye, center, up, vfov_deg, W, H):
    eye, center, up = map(lambda v: np.array(v, float), (eye, center, up))
    z = eye - center; z /= np.linalg.norm(z)
    x = np.cross(up, z); x /= np.linalg.norm(x)
    y = np.cross(z, x)
    pc = np.stack([x, y, z], 1).T @ (np.array(P, float) - eye)
    f = 1.0 / np.tan(np.radians(vfov_deg) / 2)
    return ((pc[0] / (-pc[2])) * (f / (W / H)) * .5 + .5) * W, \
           (1 - ((pc[1] / (-pc[2])) * f * .5 + .5)) * H


labels = {"b": r"$\{b\}$ base", "e": r"$\{e\}$ TCP",
          "c": r"$\{c\}$ caméra", "o": r"$\{o\}$ outil"}
off = {"b": (-140, 30), "e": (200, -50), "c": (-170, -90), "o": (120, 120)}

for name, P in zip(names, origins):
    px, py = project(P, EYE, CENTER, UP, VFOV, W, H)
    print(f"  {name}: px={px:.0f} py={py:.0f}")

fig, ax = plt.subplots(figsize=(6.3, 5.0))
ax.imshow(arr)
ax.set_axis_off()
for name, P in zip(names, origins):
    px, py = project(P, EYE, CENTER, UP, VFOV, W, H)
    dx, dy = off[name]
    ax.annotate(labels[name], xy=(px, py), xytext=(px + dx, py + dy),
                fontsize=11, ha="center", va="center",
                arrowprops=dict(arrowstyle="-", lw=0.7, color="black"),
                bbox=dict(fc="white", ec="0.6", boxstyle="round,pad=0.25"))

ax.text(0.015, 0.02, r"$x$ : rouge\quad $y$ : vert\quad $z$ : bleu".replace("\\quad", "   "),
        transform=ax.transAxes, fontsize=9, va="bottom",
        bbox=dict(fc="white", ec="0.6", boxstyle="round,pad=0.3"))

fig.savefig("repere_frames.pdf", bbox_inches="tight", pad_inches=0.02)
fig.savefig("repere_frames_preview.png", dpi=160, bbox_inches="tight")
print("écrit : repere_frames.pdf / repere_frames_preview.png")
