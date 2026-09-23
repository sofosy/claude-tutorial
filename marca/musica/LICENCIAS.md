# Licencias — música de fondo

Todas las pistas son **CC0 1.0 Universal (dominio público)**: uso comercial
permitido, sin atribución obligatoria y sin regalías. Se descargaron el
**2026-09-23** desde OpenGameArt.org (registro con licencia CC0 verificada en
la página de cada obra individual, no en una colección genérica).

Se descartó freepd.com (el sitio original cerró operaciones en 2025; el
dominio espejo `en.freepd.cn` no pudo verificarse como legítimo) y
AShamaluevMusic/archive.org (la licencia exige comprar un permiso para
monetizar, no es CC0).

---

## elevator-music-mcculloch.mp3

- **Título original:** Elevator Music
- **Autor:** Alex McCulloch (Pro Sensory)
- **URL de origen:** https://opengameart.org/content/elevator-music
- **Archivo origen:** https://opengameart.org/sites/default/files/ElevatorMusic.wav
- **Licencia:** CC0 1.0 Universal — https://creativecommons.org/publicdomain/zero/1.0/
- **Duración:** 1:36 (96 s) — el motor la repite en bucle (`-stream_loop -1`) para cubrir la duración del video
- **Nota del autor:** "Attribution appreciated but not required."
- **Descargado:** 2026-09-23
- Instrumental, sin voz, pads suaves — sonido literal de música de ambiente corporativo.

## elevator-music-2-mcculloch.mp3

- **Título original:** Elevator Music 2
- **Autor:** Alex McCulloch (Pro Sensory)
- **URL de origen:** https://opengameart.org/content/elevator-music-2
- **Archivo origen:** https://opengameart.org/sites/default/files/ElevatorMusic2.wav
- **Licencia:** CC0 1.0 Universal — https://creativecommons.org/publicdomain/zero/1.0/
- **Duración:** 1:52 (112 s) — bucle igual que la anterior
- **Nota del autor:** "state my name Alex McCulloch in your game. Attribution appreciated but not required."
- **Descargado:** 2026-09-23
- Instrumental, sin voz; variante de la anterior, algo más viva.

## first-light-particles-yoiyami.mp3

- **Título original:** First Light Particles
- **Autor:** Yoiyami
- **URL de origen:** https://opengameart.org/content/first-light-particles-%E2%80%93-cc0-atmospheric-pianoambient-track
- **Archivo origen:** https://opengameart.org/sites/default/files/first_light_particles_0.wav
- **Licencia:** CC0 1.0 Universal — https://creativecommons.org/publicdomain/zero/1.0/
- **Duración:** 2:12 (131.7 s)
- **Descargado:** 2026-09-23
- Piano suave + pads ambientales, instrumental, sin voz. Más introspectiva
  que las dos anteriores; buena opción para tutoriales de módulos más
  "delicados" (nómina, historial clínico).

---

Los `.wav` originales se transcodificaron a MP3 192 kbps/44.1 kHz/estéreo con
ffmpeg (mismo códec de audio que usa el motor) para reducir peso; no cambia la
licencia, que es del contenido, no del contenedor. `.mp3` está en
`.gitignore` del proyecto (ver "Material pesado"), así que estas pistas nunca
se versionan — quedan solo en disco local.

**Recomendada por defecto:** `elevator-music-mcculloch.mp3` (la más neutra y
menos protagonista bajo la voz).
