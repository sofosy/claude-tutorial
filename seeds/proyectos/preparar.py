"""Arma por el API el estado que cada video de la serie Proyectos encuentra hecho.

Empresa «Constructora Germiva Demo S.R.L.»; obra «Nave industrial Haina» para
«Industrias Germiva del Caribe S.R.L.». Todo ficticio (RNC 130555xxx). Reutiliza
las utilidades de seeds/contabilidad/preparar.py (misma API, misma base).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "contabilidad"))
import preparar as c  # noqa: E402

llamar, sql = c.llamar, c.sql
M3, M2, TON, UND = 28, 27, 39, 43
INICIO, FIN = "2026-11-02", "2027-04-30"
CLAVE = "Demo2026!"

# Partidas de la obra: (clave, fase, nombre, categoría, unidad, cantidad, costo unitario)
PARTIDAS = [
    ("exc", "Cimentación", "Excavación y relleno", "SUB", M3, 500, 800),
    ("zap", "Cimentación", "Zapatas y pedestales", "MAT", M3, 80, 9000),
    ("est", "Estructura", "Estructura metálica", "MAT", TON, 40, 45000),
    ("cub", "Estructura", "Cubierta y cerramiento", "MAT", M2, 1200, 900),
    ("pis", "Terminaciones", "Piso industrial", "MAT", M2, 1000, 700),
    ("ele", "Terminaciones", "Instalación eléctrica", "SUB", UND, 1, 300000),
]


def usuario(usuario_, nombre, apellido, rol_admin=True):
    """Segunda persona de la empresa (aprobadora): la aprobación es de cuatro ojos."""
    rol = int(sql("SELECT id FROM roles WHERE is_admin_role=1 AND deleted_at IS NULL ORDER BY id LIMIT 1"))
    llamar("POST", "/user", {"username": usuario_, "email": f"{usuario_}@constructora.germiva.com",
                              "password": CLAVE, "name": nombre, "lastName": apellido, "roles": [rol],
                              "mustChangePassword": False})
    uid = int(sql(f"SELECT id FROM users WHERE username='{usuario_}'"))
    sql(f"UPDATE users SET emailVerified=1 WHERE id={uid}")
    return uid


def token_de(usuario_):
    return llamar("POST", "/auth/dev/login", {"username": usuario_, "password": CLAVE}, sin_token=True)["accessToken"]


def como(usuario_, metodo, ruta, cuerpo=None):
    """Una llamada con la sesión de otra persona, sin perder la del admin."""
    admin, c.TOKEN = c.TOKEN, token_de(usuario_)
    try:
        return llamar(metodo, ruta, cuerpo)
    finally:
        c.TOKEN = admin


def quitar_demo_de_la_instantanea():
    """El proyecto de demostración de la semilla (cifras sintéticas) no sale en los videos."""
    sql("UPDATE project_budgets SET deleted_at=NOW() WHERE deleted_at IS NULL; "
        "UPDATE projects SET deleted_at=NOW() WHERE company_id=1 AND deleted_at IS NULL")


def cuenta_de_obra():
    padre = int(sql("SELECT id FROM accounting_chart WHERE code='5.01.01' AND company_id IS NULL AND deleted_at IS NULL LIMIT 1"))
    nivel = int(sql(f"SELECT level FROM accounting_chart WHERE id={padre}"))
    return llamar("POST", "/v1/accounting-chart", {
        "type": "expense", "nature": "debit", "active": True, "code": "5.01.01.03", "name": "Costos de obra",
        "level": nivel + 1, "parent": padre, "allowsMovement": True})["id"]


def base():
    """Lo que toda la serie da por hecho: cliente, centro de costo de la obra,
    cuenta de costos de obra, la aprobadora y un solo nivel de aprobación."""
    quitar_demo_de_la_instantanea()
    b = {"cliente": llamar("POST", "/v1/partner", {
            "name": "Industrias Germiva del Caribe S.R.L.", "legalName": "Industrias Germiva del Caribe S.R.L.",
            "tin": "130555101", "documentType": "RNC", "partnerType": ["CUSTOMER"],
            "partnerCategory": "BUSINESS", "customerType": "REGULAR"})["id"],
         "centro": c.centro("CC-NAVE", "Obra Nave Haina", "cost"),
         "cuenta": cuenta_de_obra(),
         "laura": usuario("laura.mendez", "Laura", "Méndez"),
         "almacen": int(sql("SELECT id FROM warehouse WHERE company_id=1 ORDER BY id LIMIT 1"))}
    llamar("PUT", "/v1/project-budgets/settings", {"approvalLevels": [{"level": 1, "upTo": None}],
                                                     "controlPolicy": "WARN"})
    b["categorias"] = {k["code"]: k["id"] for k in llamar("GET", "/v1/project-budgets/categories")}
    return b


def proyecto(b, **extra):
    return llamar("POST", "/v1/projects", {
        "name": "Nave industrial Haina", "description": "Nave de 1,000 m² para almacén y despacho, en Haina.",
        "startDate": INICIO, "endDate": FIN, "partner": b["cliente"], "projectManager": 1,
        "teamMembers": [b["laura"]], "budget": 0, "costCenter": b["centro"], "warehouse": b["almacen"], **extra})


def nodos(b, partidas=PARTIDAS, sin_costo=()):
    fases, salida = [], []
    for clave, fase, nombre, cat, unidad, cantidad, costo in partidas:
        if fase not in fases:
            fases.append(fase)
            salida.append({"key": f"f{len(fases)}", "name": fase, "nodeType": "PHASE", "sortOrder": len(fases) - 1})
        salida.append({"key": clave, "parentKey": f"f{fases.index(fase) + 1}", "name": nombre, "nodeType": "LINE",
                       "sortOrder": len(salida),
                       "line": {"costCategory": b["categorias"][cat], "account": b["cuenta"], "unitMeasure": unidad,
                                "quantity": str(cantidad), "unitCost": "0" if clave in sin_costo else str(costo)}})
    return salida


def presupuesto(b, proyecto_id, partidas=PARTIDAS, sin_costo=(), indirectos="10", utilidad="20", aprobar=True):
    p = llamar("POST", "/v1/project-budgets", {"project": proyecto_id, "name": "Presupuesto de obra",
                                                "currency": c.DOP, "budgetType": "COST_AND_REVENUE",
                                                "exchangeRate": "1"})
    version = p["versions"][0]["id"]
    ruta = f"/v1/project-budgets/{p['id']}/versions/{version}"
    llamar("PUT", f"{ruta}/structure", {"editRevision": 0, "indirectPercentage": indirectos,
                                         "contingencyPercentage": "0", "profitPercentage": utilidad,
                                         "nodes": nodos(b, partidas, sin_costo)})
    if aprobar:
        envio = llamar("POST", f"{ruta}/submit", {})
        como("laura.mendez", "POST", f"{ruta}/approve", {"level": 1, "submissionNumber": envio["submissionNumber"],
                                                         "notes": "Revisado contra la cotización"})
    return {"id": p["id"], "version": version, "ruta": ruta}


# ── estados ──────────────────────────────────────────────────────────────────

def inicio():
    # P01: la empresa lista para crear su primer proyecto.
    base()


def con_proyecto():
    # P02: el proyecto creado, sin presupuesto.
    b = base()
    b["proyecto"] = proyecto(b)
    return b


def borrador():
    # P03: el presupuesto en borrador con sus seis partidas; a «Zapatas» le
    # falta el costo (el video lo arma con el análisis de precio unitario).
    b = con_proyecto()
    b["presupuesto"] = presupuesto(b, b["proyecto"]["id"], sin_costo=("zap",), indirectos="0", utilidad="0",
                                   aprobar=False)
    return b


def por_aprobar():
    # P04: el presupuesto completo en borrador, listo para enviar a aprobación.
    b = con_proyecto()
    b["presupuesto"] = presupuesto(b, b["proyecto"]["id"], aprobar=False)
    return b


def aprobado():
    b = con_proyecto()
    b["presupuesto"] = presupuesto(b, b["proyecto"]["id"])
    return b


ESTADOS = {"inicio": inicio, "con-proyecto": con_proyecto, "borrador": borrador,
           "por-aprobar": por_aprobar, "aprobado": aprobado}

if __name__ == "__main__":
    c.TOKEN = c.token()
    ESTADOS[sys.argv[1]]()
