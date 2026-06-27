#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Architecture du réseau de Flow Matching conditionnel.

Trois encodeurs de conditionnement (nuage de points DP3/PointNet, état robot,
temps de flux) forment un vecteur c qui module par FiLM chaque bloc résiduel
d'un U-Net temporel 1D (en forme de U) prédisant le champ de vitesse v_theta.
Style mémoire : Okabe-Ito, français, sans titre. Exporte un PDF vecteur.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OI = dict(orange="#E69F00", sky="#56B4E9", green="#009E73", yellow="#F0E442",
          blue="#0072B2", verm="#D55E00", purple="#CC79A7", grey="#BBBBBB")
plt.rcParams.update({"font.family": "serif", "svg.fonttype": "none", "font.size": 8})

fig, ax = plt.subplots(figsize=(7.6, 8.4))
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")


def box(x, y, w, h, t, fc, fs=7.0, ec="0.25", lw=1.0, film=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0.3,rounding_size=1.4",
                 fc=fc, ec=ec, lw=lw, zorder=3))
    ax.text(x + w/2, y + h/2, t, ha="center", va="center", fontsize=fs, zorder=5)
    if film:   # pastille orange = bloc conditionné par FiLM
        ax.plot(x + w - 1.6, y + h - 1.6, marker="o", ms=4.5,
                color=OI["orange"], mec="0.25", mew=0.5, zorder=6)
    return dict(cx=x+w/2, cy=y+h/2, x=x, y=y, w=w, h=h,
                t=(x+w/2, y+h), b=(x+w/2, y), l=(x, y+h/2), r=(x+w, y+h/2))


def ar(p0, p1, color="0.25", lw=1.1, ls="-", rad=0.0, style="-|>"):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=11,
                 color=color, lw=lw, linestyle=ls,
                 connectionstyle=f"arc3,rad={rad}", zorder=4, shrinkA=2, shrinkB=2))


# ======================================================================
# 1) ENCODEURS DE CONDITIONNEMENT  (haut)
# ======================================================================
ax.text(2, 99, "Encodeurs de conditionnement", fontsize=9, weight="bold")

pc_in  = box(1, 90, 16, 7.5, "Nuage de points\ncible + outil  ($N\\times3$)", OI["sky"], 6.6)
pc_enc = box(20, 88.5, 24, 10.5, "Encodeur DP3 (PointNet)\nMLP partagé $3{\\to}64{\\to}128{\\to}256$\nmax-pool sur les points $\\to$ 64", OI["green"], 6.2)
f_pc   = box(47, 90.5, 8, 7, "$f_{\\mathrm{pc}}$\n64", OI["green"], 7)

rb_in  = box(1, 79, 16, 7.5, "État robot\n($2\\times9$)", OI["sky"], 6.8)
rb_enc = box(20, 78, 24, 9, "MLP   $18{\\to}128{\\to}64$", OI["green"], 7)
f_rb   = box(47, 79, 8, 7, "$f_{\\mathrm{rob}}$\n64", OI["green"], 7)

t_in   = box(1, 68, 16, 7.5, "Temps de flux\n$t\\in[0,1]$", OI["sky"], 6.8)
t_enc  = box(20, 67, 24, 9, "Embedding sinusoïdal\n$+$ MLP $\\to 256$", OI["green"], 6.6)
f_t    = box(47, 68, 8, 7, "$f_{t}$\n256", OI["green"], 7)

for a, b in [(pc_in, pc_enc), (pc_enc, f_pc), (rb_in, rb_enc), (rb_enc, f_rb),
             (t_in, t_enc), (t_enc, f_t)]:
    ar(a["r"], b["l"])

gl = box(60, 84, 12, 8, "concat.\nglobal  128", OI["orange"], 6.6)
c  = box(36, 57, 22, 8.5, "$\\mathbf{c}$ : conditionnement\n(global $+$ temps)  384", OI["orange"], 7)
ar(f_pc["r"], gl["l"], rad=-0.12)
ar(f_rb["r"], gl["l"], rad=0.12)
ar(gl["b"], c["t"], rad=0.15)
ar(f_t["r"], c["t"], rad=-0.15)

# ======================================================================
# 2) U-NET TEMPOREL 1D  en forme de U
# ======================================================================
ax.text(0.8, 28, "U-Net temporel 1D — réseau de vitesse $v_\\theta$",
        fontsize=8.5, weight="bold", rotation=90, va="center", ha="center")

xt  = box(3, 56, 13, 7, "$\\mathbf{x}_t$\n$16\\times9$", OI["grey"], 7)
# bras gauche : encodeur (descend)
d1  = box(3, 42, 16, 10.5, "Down\n$9{\\to}256$\n$L=16$", OI["blue"], 6.8, film=True)
d2  = box(3, 28, 16, 10.5, "Down\n$256{\\to}512$\n$L=8$", OI["blue"], 6.8, film=True)
d3  = box(3, 14, 16, 10.5, "Down\n$512{\\to}1024$\n$L=4$", OI["blue"], 6.6, film=True)
# fond du U : goulot
mid = box(33, 2.5, 24, 9, "Bottleneck  $1024$\n$2\\times$ ResBlock  ($L=4$)", OI["purple"], 6.6, film=True)
# bras droit : décodeur (remonte)
u1  = box(71, 14, 16, 10.5, "Up\n$1024{\\to}512$\n$L=8$", OI["sky"], 6.8, film=True)
u2  = box(71, 28, 16, 10.5, "Up\n$512{\\to}256$\n$L=16$", OI["sky"], 6.8, film=True)
fin = box(71, 42, 16, 10.5, "Conv finale\n$256{\\to}9$", OI["blue"], 6.8, film=True)
vout = box(71, 56, 16, 7, "$v_\\theta$\n$16\\times9$", OI["verm"], 7)

# flux principal en U
ar(xt["b"], d1["t"])
ar(d1["b"], d2["t"]); ar(d2["b"], d3["t"])
ar(d3["b"], mid["l"], rad=-0.25)
ar(mid["r"], u1["b"], rad=-0.25)
ar(u1["t"], u2["b"]); ar(u2["t"], fin["t"] if False else fin["b"])
ar(fin["t"], vout["b"])

# connexions de saut (concaténation) à travers l'ouverture du U
ar(d3["r"], u1["l"], color=OI["blue"], ls="--", lw=1.0)
ar(d2["r"], u2["l"], color=OI["blue"], ls="--", lw=1.0)
ax.text(45, 31.5, "connexions de saut\n(concaténation)", fontsize=6.4,
        color="0.45", ha="center", va="center")

# ======================================================================
# 3) CONDITIONNEMENT FiLM : c -> tous les blocs (pastilles oranges)
# ======================================================================
ar(c["b"], (45, 48), color=OI["orange"], lw=1.3)
ax.text(45, 45, "FiLM $(\\gamma,\\beta)$ :\nmodule chaque bloc\n(●)", fontsize=6.6,
        color=OI["orange"], ha="center", va="center")

# ======================================================================
# 4) SORTIE -> INTÉGRATION ODE
# ======================================================================
ode = box(71, 67, 28, 12,
          "Intégration ODE\n(Euler, 10 pas)\n"
          "$\\mathbf{x}_{k+1}=\\mathbf{x}_k+v_\\theta\\,\\Delta t$\n"
          "$\\Rightarrow$ trajectoire nominale", OI["yellow"], 6.6)
ar(vout["t"], ode["b"], rad=0.12)
ax.text(11, 53.2, "inférence : $\\mathbf{x}_0\\sim\\mathcal{N}(0,\\mathbf{I})$",
        fontsize=6.2, color="0.45", ha="center")

fig.savefig("architecture_fm.pdf", bbox_inches="tight", pad_inches=0.05)
fig.savefig("architecture_fm.png", dpi=170, bbox_inches="tight")
print("écrit : architecture_fm.pdf / .png")
