# Licencias — tipografía

## Inter (Bold, ExtraBold)

- **Autor:** The Inter Project Authors — https://github.com/rsms/inter
- **Licencia:** SIL Open Font License 1.1 (OFL) — ver `OFL.txt` en esta carpeta
- **Origen de los .ttf:** paquete `@fontsource/inter` vía CDN jsDelivr
  (build estático de la misma fuente que publica Google Fonts; el release
  oficial de rsms/inter solo trae variable font + `.ttc`, que este Pillow/
  freetype no pudo abrir — `cannot open resource` — así que se usó la
  variante estática de fontsource, que sí carga)
  - https://cdn.jsdelivr.net/fontsource/fonts/inter@latest/latin-700-normal.ttf
  - https://cdn.jsdelivr.net/fontsource/fonts/inter@latest/latin-800-normal.ttf
- **OFL.txt origen:** https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/inter/OFL.txt
- **Descargado:** 2026-09-23
- **Verificado:** `PIL.ImageFont.truetype()` la carga sin error en el venv del
  proyecto (`Inter Bold`, `Inter ExtraBold`).

Uso comercial libre, sin atribución obligatoria (aunque se agradece); no
puede venderse la fuente suelta, pero sí usarse embebida/rasterizada en
imágenes y video, que es como la usa `tarjeta.py`/`anotar.py`.

**No integrada todavía.** `tutorial/anotar.py::_FUENTES` sigue apuntando a
fuentes del sistema (Arial Bold / Segoe UI Bold en Windows). Para usar Inter
solo hay que anteponer una ruta a esa lista, p. ej.:

```python
_FUENTES = [
    str(Path(__file__).resolve().parent.parent / "marca/fuentes/Inter-ExtraBold.ttf"),
    # ...resto de la lista tal cual, como respaldo
]
```
