# Genera la foto de demo del «Chocolate tradicional Cacao Real» (empaque ficticio) para el video 1.
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

AQUI = Path(__file__).parent
F = Path(__file__).resolve().parents[2] / "marca" / "fuentes"
W, H = 1200, 1200
img = Image.new("RGB", (W, H), (246, 241, 234))
d = ImageDraw.Draw(img)
# sombra
sombra = Image.new("L", (W, H), 0)
ImageDraw.Draw(sombra).rounded_rectangle((250, 330, 990, 960), 40, fill=120)
img.paste((205, 195, 182), (0, 0), sombra.filter(ImageFilter.GaussianBlur(28)))
# empaque
d.rounded_rectangle((230, 300, 970, 930), 36, fill=(92, 52, 30))
d.rounded_rectangle((230, 300, 970, 400), 36, fill=(70, 38, 22))
d.rectangle((230, 370, 970, 400), fill=(70, 38, 22))
d.rounded_rectangle((300, 470, 900, 820), 28, fill=(214, 168, 76))
d.rounded_rectangle((316, 486, 884, 804), 22, outline=(120, 74, 30), width=4)

def fuente(nombre, tam):
    for n in (nombre, "Inter-Bold.ttf", "Inter-Regular.ttf"):
        p = F / n
        if p.exists():
            return ImageFont.truetype(str(p), tam)
    return ImageFont.load_default()

t1, t2, t3 = fuente("Inter-ExtraBold.ttf", 74), fuente("Inter-Bold.ttf", 44), fuente("Inter-Bold.ttf", 28)
def centro(txt, y, f, color):
    w = d.textlength(txt, font=f)
    d.text(((W - w) / 2, y), txt, font=f, fill=color)
centro("CACAO REAL", 535, t1, (74, 40, 20))
centro("Chocolate tradicional", 655, t2, (74, 40, 20))
centro("de mesa · 100 % cacao dominicano", 725, t3, (98, 60, 30))
centro("8 tabletas", 330, t3, (232, 210, 170))
img.save(AQUI / "chocolate-cacao-real.jpg", quality=92)
print("ok", AQUI / "chocolate-cacao-real.jpg")
