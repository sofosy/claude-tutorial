# python seeds/certificacion/comprobante.py <salida.png> <monto> <referencia> <ordenante> <cuenta> [concepto]
# Captura ficticia de una transferencia de banca en línea (banco inventado «Banco Ámbar»), para las demos.
import sys
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

out, monto, ref, ordenante, cuenta = sys.argv[1:6]
concepto = sys.argv[6] if len(sys.argv) > 6 else "Pago certificación e-CF"
F = "C:/Windows/Fonts/"
def f(n, s): return ImageFont.truetype(F + n, s)
W, H = 750, 1334
im = Image.new("RGB", (W, H), "#F4F6F8")
d = ImageDraw.Draw(im)
# barra de estado
d.text((40, 22), "9:41", font=f("seguisb.ttf", 28), fill="#111")
d.text((W - 150, 22), "LTE  87%", font=f("segoeui.ttf", 26), fill="#111")
# cabecera del banco
d.rectangle([0, 70, W, 200], fill="#B4530F")
d.ellipse([40, 100, 110, 170], fill="#F6C453")
d.text((58, 108), "A", font=f("segoeuib.ttf", 44), fill="#B4530F")
d.text((130, 100), "Banco Ámbar", font=f("segoeuib.ttf", 40), fill="white")
d.text((130, 150), "Banca en línea", font=f("segoeui.ttf", 26), fill="#FDE7C8")
# tarjeta principal
d.rounded_rectangle([30, 230, W - 30, 1250], radius=28, fill="white", outline="#E3E7EC", width=2)
d.ellipse([W // 2 - 55, 270, W // 2 + 55, 380], fill="#16A34A")
d.line([(W // 2 - 25, 325), (W // 2 - 5, 348), (W // 2 + 30, 300)], fill="white", width=10)
def center(y, text, font, fill):
    w = d.textlength(text, font=font); d.text(((W - w) / 2, y), text, font=font, fill=fill)
center(400, "Transferencia exitosa", f("segoeuib.ttf", 40), "#111827")
center(460, "Monto transferido", f("segoeui.ttf", 26), "#6B7280")
center(495, f"RD$ {float(monto):,.2f}", f("segoeuib.ttf", 58), "#111827")
fecha = datetime.now().strftime("%d/%m/%Y %I:%M %p").lower().replace("am", "a. m.").replace("pm", "p. m.")
filas = [
    ("Fecha y hora", fecha),
    ("Número de referencia", ref),
    ("Desde", ordenante),
    ("Cuenta de origen", cuenta),
    ("Para", "SOFOSY S.R.L."),
    ("Cuenta destino", "Corriente ****7730"),
    ("Banco destino", "Banco Ámbar"),
    ("Concepto", concepto),
    ("Estado", "Completada"),
]
y = 610
for k, v in filas:
    d.line([(60, y - 14), (W - 60, y - 14)], fill="#EEF0F3", width=2)
    d.text((60, y), k, font=f("segoeui.ttf", 25), fill="#6B7280")
    fv = f("seguisb.ttf", 26)
    w = d.textlength(v, font=fv)
    if w > 380:
        fv = f("seguisb.ttf", 22); w = d.textlength(v, font=fv)
    d.text((W - 60 - w, y), v, font=fv, fill="#16A34A" if k == "Estado" else "#111827")
    y += 66
center(1200, "Conserve este comprobante para sus registros.", f("segoeui.ttf", 22), "#9CA3AF")
im.save(out)
print("comprobante", out)
