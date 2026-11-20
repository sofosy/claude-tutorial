"""Cabecera común de los guiones de la serie; cada gNN.py define el resto."""
import json, sys
RAIZ = "/home/user/claude-tutorial/guiones/"

def base(titulo, descripcion, comentario, navegar, esperar, setup, aprenderas, errores, empresa="contabilidad"):
    return {
        "titulo": titulo, "descripcion": descripcion, "_comentario": comentario,
        "base_url": "http://localhost:4200", "zona_horaria": "America/Santo_Domingo",
        "musica": {"archivo": "marca/musica/elevator-music-mcculloch.mp3", "volumen_db": -32, "ducking": True, "fade_s": 2},
        "loudnorm": {"lufs": -14, "tp": -1.5},
        "marca_video": {"entrada_s": 3, "cierre_s": 3},
        "rotulo_paso": {"segundos": 3.5},
        "css_global": ["app-chatbot-widget{display:none!important}", ".chatbot-fab{display:none!important}"],
        "voz": {"id": "es-DO-RamonaNeural", "velocidad": "+12%"},
        "pronunciacion": {"NIC": "nic", "CxC": "ce-por-ce", "CxP": "ce-por-pe", "ISR": "i-ese-erre", "BHD": "be-hache-de",
                          "USD": "dólares", "DOP": "pesos", "ITBIS": "itebis", "CPI": "ce-pe-i", "SPI": "ese-pe-i", "PDF": "pe-de-efe"},
        "privacidad": {"_perfil": "Datos ficticios sembrados por seeds/ (RNC 130555xxx, nombres con «Germiva»): la narración los nombra, no se sustituye nada.",
                       "perfil": "ninguno", "permitidos": ["germiva", "130555", "example.com"],
                       "mapa_fijo": {"localhost:3001": "api.germiva.com", "localhost:4200": "germiva.com"}},
        "sesion": {"tipo": "api", "url": "http://localhost:3001/api/auth/dev/login", "cuerpo": {"username": "admin", "password": "admin"},
                   "clave": "aut", "extra": {"__v": 2}, "navegar": navegar, "esperar": esperar},
        "setup": {"tipo": "shell", "cmd": setup},
        "portada_s": 8, "aprenderas": aprenderas, "errores_comunes": errores,
    }

def paso(id, capitulo, rotulo, ruta, texto, narracion, acciones, **extra):
    return {"id": id, "capitulo": capitulo, "rotulo": rotulo, "ruta": ruta, "texto_pantalla": texto, **extra,
            "narracion": " ".join(narracion.split()), "acciones": acciones}

def clic(sel, al): return {"click": sel, "al_decir": al}
def esc(sel, texto, al): return {"escribir": {"sel": sel, "texto": texto}, "al_decir": al}
def res(sel, al, ms=3000, cursor=False): return {"resaltar": sel, "durante_ms": ms, "cursor": cursor, "al_decir": al}

def guardar(nombre, g, pasos):
    g["pasos"] = pasos
    open(RAIZ + nombre + ".json", "w", encoding="utf-8").write(json.dumps(g, ensure_ascii=False, indent=2) + "\n")
    n = sum(len(p["narracion"]) for p in pasos)
    print(nombre, "pasos", len(pasos), "caracteres", n, "≈", round(n/15.5), "s")
