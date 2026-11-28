"""Cabecera común de los guiones de la clínica (Citas, Pacientes, Consentimiento, ARS).

Misma identidad que la serie de Citas de 2026-10: voz es-DO-RamonaNeural +12 %, música
«elevator-music-mcculloch» a -32 dB con ducking, entrada/cierre de RegiSalud y sonoridad -14 LUFS.
Sin subtítulos quemados: el motor nunca los pinta en el video (el .srt es un archivo aparte).
"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

PERMITIDOS = [
    "regisalud", "RegiSalud", "Los Prados", "40205550", "00105551", "8095550", "8295550", "8495550", "losprados", "los-prados", "402-0555", "001-0555", "correo.test",
    "131456789", "EXQ-", "Carmen Peña", "Ana Pérez", "Jorge Medina", "Marta Reyes", "Pablo Santos", "Elías Tavárez",
    "Luis Gómez", "Ramírez", "Castro", "Herrera", "Almonte", "Lora", "Mejía", "Rosa Elena", "Martínez",
    "Juan Carlos", "Batista", "Carolina", "Méndez", "Miguel Ángel", "Rosario", "Paola", "Jiménez",
    "Rafael Antonio", "Núñez", "Yesenia", "Castillo", "Héctor Manuel", "Vargas", "Laura Patricia", "Santana",
    "Daniel Alberto", "Polanco", "Mariela", "Guzmán", "Francisco Javier", "Cabrera", "Altagracia", "Peralta",
    "Mateo", "Valeria", "Natalia", "Gabriela", "Fernández", "Sofía", "Andrés", "Lucía", "Tomás",
    "Rosa", "Elena", "Juan", "Carlos", "Miguel", "Ángel", "Rafael", "Antonio", "Héctor", "Manuel", "Laura", "Patricia", "Daniel", "Alberto", "Francisco", "Javier", "Ana", "Jorge", "Marta", "Pablo", "Elías", "Luis", "Pérez", "Medina", "Reyes", "Santos", "Tavárez", "Gómez",
    "809-555", "829-555", "849-555", "102017174", "401516454", "809-476-3535", "humano.com.do", "PSS-", "Consultorio", "Humano", "Senasa", "Mapfre", "Universal", "Primera",
]

BASE = {
    "base_url": "http://127.0.0.1:4200",
    "zona_horaria": "America/Santo_Domingo",
    "sesion": {
        "tipo": "api", "url": "http://localhost:3001/api/auth/dev/login",
        "cuerpo": {"username": "admin.losprados@regisalud.test", "password": "LosPrados2026!"},
        "clave": "aut", "extra": {"__v": 2}, "navegar": "/home",
    },
    "marca": {"nombre": "RegiSalud", "logo": "marca/regisalud.png", "simbolo": "marca/regisalud-simbolo.png",
              "linea": "RegiSalud · Tutorial"},
    "url_publica": "https://regisalud.com",
    "voz": {"id": "es-DO-RamonaNeural", "velocidad": "+12%"},
    "musica": {"archivo": "marca/musica/elevator-music-mcculloch.mp3", "volumen_db": -32, "ducking": True, "fade_s": 2},
    "loudnorm": {"lufs": -14, "tp": -1.5},
    "marca_video": {"entrada_s": 3, "cierre_s": 3},
    "rotulo_paso": {"segundos": 3.5},
    "rutas_locales": [
        {"url": "https://fonts.googleapis.com/css?family=Material*", "archivo": "fuentes/material-icons.css"},
        {"url": "https://fonts.googleapis.com/css2?family=Roboto*", "archivo": "fuentes/roboto.css"},
        {"url": "https://fonts.gstatic.com/local/*", "carpeta": "fuentes"},
    ],
    "css_global": [
        "app-chatbot-widget{display:none!important}",
        ".chatbot-fab{display:none!important}",
        ".nav-notification-icons .notification-badge{display:none!important}",
    ],
    "pronunciacion": {"RegiSalud": "Regisalud", "ARS": "a-erre-ese", "PDF": "pe-de-efe"},
    "privacidad": {
        "permitidos": PERMITIDOS,
        "mapa_fijo": {"localhost:3001": "api.regisalud.com", "127.0.0.1:4200": "regisalud.com",
                      "localhost:4200": "regisalud.com"},
    },
    "tags": ["RegiSalud", "clínica", "consultorio", "citas médicas", "República Dominicana", "tutorial"],
}


def guion(nombre: str, titulo: str, descripcion: str, pasos: list, comentario: str = "", **extra) -> Path:
    g = {"titulo": titulo, "descripcion": descripcion, "_comentario": comentario, **BASE, **extra, "pasos": pasos}
    ruta = RAIZ / "guiones" / f"{nombre}.json"
    ruta.write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return ruta
