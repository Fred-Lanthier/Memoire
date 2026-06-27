#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figure des repères du système (style Fig. 4.5 d'Auger), pour notre robot :
  {b} base du robot, {e} TCP/effecteur, {c} caméra poignet, {f} pointe de fourchette.

Méthode :
  - cinématique directe à partir du URDF (panda_fork.urdf) à une pose fixe ;
  - chaque maillon est rendu à partir de son STL de collision ;
  - un trièdre RGB (x=rouge, y=vert, z=bleu) est superposé à chaque repère ;
  - rendu hors-écran Open3D, exporté en PNG (composé/étiqueté ensuite).
"""
import os
import numpy as np
import open3d as o3d

MESH = ("/home/flanthier/Github/src/robot-assisted-feeding/src/franka_ros/"
        "src/franka_ros/franka_description/meshes/collision/")
FORK_STL = ("/home/flanthier/Github/src/vision_processing/src/vision_processing/"
            "diffusion_model_train/fork_tip.stl")

# ----------------------------------------------------------------------
def rpy_xyz(rpy=(0, 0, 0), xyz=(0, 0, 0)):
    r, p, y = rpy
    cr, sr, cp, sp, cy, sy = (np.cos(r), np.sin(r), np.cos(p),
                              np.sin(p), np.cos(y), np.sin(y))
    R = np.array([[cy*cp, cy*sp*sr - sy*cr, cy*sp*cr + sy*sr],
                  [sy*cp, sy*sp*sr + cy*cr, sy*sp*cr - cy*sr],
                  [-sp,   cp*sr,            cp*cr]])
    T = np.eye(4); T[:3, :3] = R; T[:3, 3] = xyz
    return T

def Rz(t):
    T = np.eye(4)
    T[:3, :3] = [[np.cos(t), -np.sin(t), 0],
                 [np.sin(t),  np.cos(t), 0], [0, 0, 1]]
    return T

# --- cinématique directe (origines tirées du URDF) ---
q = np.array([0, -0.785, 0, -2.356, 0, 1.571, 0.785])   # pose "ready" Franka

J = [(( 0, 0, 0),          (0, 0, 0.333)),   # joint1
     ((-np.pi/2, 0, 0),    (0, 0, 0)),       # joint2
     (( np.pi/2, 0, 0),    (0, -0.316, 0)),  # joint3
     (( np.pi/2, 0, 0),    (0.0825, 0, 0)),  # joint4
     ((-np.pi/2, 0, 0),    (-0.0825, 0.384, 0)),  # joint5
     (( np.pi/2, 0, 0),    (0, 0, 0)),       # joint6
     (( np.pi/2, 0, 0),    (0.088, 0, 0))]   # joint7

T = np.eye(4)
link_T = {0: T.copy()}
for i, (rpy, xyz) in enumerate(J, start=1):
    T = T @ rpy_xyz(rpy, xyz) @ Rz(q[i-1])
    link_T[i] = T.copy()

T8   = link_T[7] @ rpy_xyz((0, 0, 0), (0, 0, 0.107))
Thand = T8 @ rpy_xyz((0, 0, -np.pi/4))
T_TCP = Thand @ rpy_xyz((0, 0, 0), (0, 0, 0.1034))                      # {e}
T_cam = (T_TCP @ rpy_xyz((0, -np.pi/2, 0), (-0.052, 0.035, -0.045))
                @ rpy_xyz((-np.pi/2, 0, -np.pi/2)))                     # {c}
T_fork = T_TCP @ rpy_xyz((0, -3.6215581978882336, 0), (-0.0055, 0, 0.1296))  # {f}

frames = {"b": np.eye(4), "e": T_TCP, "c": T_cam, "f": T_fork}
print("TCP position:", np.round(T_TCP[:3, 3], 3),
      "| fork tip:", np.round(T_fork[:3, 3], 3),
      "| cam:", np.round(T_cam[:3, 3], 3))

# --- maillons + leur transformation ---
links = [(f"link{i}.stl", link_T[i]) for i in range(8)]
links.append(("hand.stl", Thand))

def load(path, Tworld, scale=1.0, local=np.eye(4)):
    m = o3d.io.read_triangle_mesh(path)
    if scale != 1.0:
        m.scale(scale, center=(0, 0, 0))
    m.transform(Tworld @ local)
    m.compute_vertex_normals()
    return m

meshes = [load(MESH + f, Tw) for f, Tw in links]
# fourchette (visuel) : origine locale + échelle mm->m
fork_local = rpy_xyz((0, 0.4799655442984406, 0), (-0.033, -0.02, 0.0171378))
meshes.append(load(FORK_STL, T_fork, scale=0.001, local=fork_local))

# ----------------------------------------------------------------------
# rendu hors-écran
W, H = 1400, 1100
ren = o3d.visualization.rendering.OffscreenRenderer(W, H)
ren.scene.set_background([1, 1, 1, 1])

mat = o3d.visualization.rendering.Material()
mat.shader = "defaultLitTransparency"
mat.base_color = [0.78, 0.80, 0.85, 0.35]   # robot translucide
for i, m in enumerate(meshes):
    ren.scene.add_geometry(f"link{i}", m, mat)

# trièdres RGB à chaque repère
axmat = o3d.visualization.rendering.Material()
axmat.shader = "defaultUnlit"
for name, Tf in frames.items():
    tri = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.12)
    tri.transform(Tf)
    ren.scene.add_geometry(f"frame_{name}", tri, axmat)

# éclairage : profil doux + soleil frontal (rendu plus clair)
try:
    ren.scene.set_lighting(ren.scene.LightingProfile.SOFT_SHADOWS,
                           np.array([-0.3, -0.5, -0.8]))
except Exception:
    pass
ren.scene.scene.set_sun_light([-0.3, -0.5, -0.8], [1, 1, 1], 400000)
ren.scene.scene.enable_sun_light(True)
ren.scene.scene.set_indirect_light_intensity(60000)

# caméra : orbite azimut/élévation autour de CENTER (faciles à ajuster)
CENTER, UP, VFOV = [0.12, 0.0, 0.38], [0, 0, 1], 41.0
DIST, AZ, EL = 1.19, -56.5, 18.2          # deg : +EL = plus haut, -AZ = plus à gauche
_az, _el = np.radians(AZ), np.radians(EL)
EYE = [CENTER[0] + DIST*np.cos(_el)*np.cos(_az),
       CENTER[1] + DIST*np.cos(_el)*np.sin(_az),
       CENTER[2] + DIST*np.sin(_el)]
ren.setup_camera(VFOV, CENTER, EYE, UP)

# sauvegarde des données pour l'étape d'étiquetage (avant le rendu fragile)
np.savez("repere_frames_data.npz",
         names=np.array(list(frames)),
         origins=np.array([frames[k][:3, 3] for k in frames]),
         cam=np.array(EYE + CENTER + UP + [VFOV, W, H], float))

# rendu + écriture immédiate (l'erreur X asynchrone d'Open3D survient ensuite)
o3d.io.write_image("repere_frames_raw.png", ren.render_to_image())
os._exit(0)
