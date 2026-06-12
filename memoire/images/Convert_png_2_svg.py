import argparse
import os
import sys
from collections import defaultdict
from PIL import Image


def convert_png_to_svg_optimized(input_path):
    if not os.path.exists(input_path):
        print(f"Erreur : '{input_path}' n'existe pas.")
        sys.exit(1)

    output_path = os.path.splitext(input_path)[0] + ".svg"
    print(f"Vectorisation optimisée : {input_path} -> {output_path}...")

    try:
        img = Image.open(input_path).convert("RGBA")
        width, height = img.size

        # Étape 1 : Balayage horizontal pour combiner les pixels consécutifs de même couleur
        # Dictionnaire : couleur -> liste de (y, x_debut, x_fin)
        shapes_by_color = defaultdict(list)

        for y in range(height):
            current_color = None
            start_x = None

            for x in range(width):
                r, g, b, a = img.getpixel((x, y))

                # Ignorer les pixels transparents ou le fond blanc pur (si tu veux l'exclure)
                # Optionnel : si tu veux ignorer le fond blanc pour gagner de la place, active la ligne suivante :
                # if r == 255 and g == 255 and b == 255: a = 0

                color_key = (r, g, b, a) if a > 0 else None

                if color_key != current_color:
                    if current_color is not None:
                        shapes_by_color[current_color].append(
                            (y, start_x, x - 1)
                        )
                    current_color = color_key
                    start_x = x

            # Fin de ligne
            if current_color is not None:
                shapes_by_color[current_color].append(
                    (y, start_x, width - 1)
                )

        # Étape 2 : Écriture du SVG
        with open(output_path, "w") as f:
            f.write(
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" shape-rendering="crispEdges">\n'
            )

            for color, segments in shapes_by_color.items():
                r, g, b, a = color
                fill_color = f"rgb({r},{g},{b})"
                fill_opacity = f' fill-opacity="{a/255}"' if a < 255 else ""

                path_data = []
                for y, x_start, x_end in segments:
                    w = x_end - x_start + 1
                    # Utilisation de rectangles optimisés dans le tracé (M=Move, h=horizontal, v=vertical)
                    path_data.append(f"M{x_start},{y}h{w}v1h-{w}z")

                f.write(
                    f'  <path d="{" ".join(path_data)}" fill="{fill_color}"{fill_opacity} stroke="none" />\n'
                )

            f.write("</svg>\n")

        # Étape 3 : Afficher le gain de poids
        original_size = os.path.getsize(input_path) / 1024
        new_size = os.path.getsize(output_path) / 1024
        print(f"Fait ! 🎉")
        print(f"Poids PNG d'origine : {original_size:.1f} Kb")
        print(f"Poids SVG optimisé   : {new_size:.1f} Kb")

    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Vectorise un PNG en SVG avec optimisation des segments de pixels."
    )
    parser.add_argument("image_path", type=str, help="Chemin de l'image PNG")
    args = parser.parse_args()
    convert_png_to_svg_optimized(args.image_path)


if __name__ == "__main__":
    main()
