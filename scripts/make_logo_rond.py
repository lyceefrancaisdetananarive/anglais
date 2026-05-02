"""Génère logo-lft-rond.png : version masquée en cercle du logo LFT.
Utilisée dans les PDF pour avoir un rendu identique à la page d'accueil
(cercle parfait sans bordure carrée bleue)."""

from PIL import Image, ImageDraw
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "assets", "img", "logo-lft.png")
DST  = os.path.join(ROOT, "assets", "img", "logo-lft-rond.png")

img = Image.open(SRC).convert("RGBA")
w, h = img.size

# Crée un masque circulaire centré qui couvre 100 % du cadre carré.
# Le carré bleu en dehors du cercle devient transparent.
mask = Image.new("L", (w, h), 0)
draw = ImageDraw.Draw(mask)
# Petite marge pour éviter l'aliasing du contour bleu
margin = 4
draw.ellipse((margin, margin, w - margin, h - margin), fill=255)

# Applique le masque alpha
img.putalpha(mask)

# Crop optionnel : coupe au bounding box du cercle pour éviter
# les marges inutiles dans le PDF.
bbox = mask.getbbox()
if bbox:
    img = img.crop(bbox)

img.save(DST, format="PNG")
print(f"✓ {os.path.relpath(DST, ROOT)}  ({img.size[0]}x{img.size[1]} px)")
