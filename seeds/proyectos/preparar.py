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


def proyecto(b, nombre="Nave industrial Haina", descripcion="Nave de 1,000 m² para almacén y despacho, en Haina.",
             **extra):
    return llamar("POST", "/v1/projects", {
        "name": nombre, "description": descripcion,
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
    detalle = llamar("GET", ruta)
    por_nodo = {l["wbsNodeId"]: l for l in detalle.get("lines", [])}
    lineas = {}
    for clave, _fase, nombre, *_ in partidas:
        nodo = next(n for n in detalle["nodes"] if n["name"] == nombre)
        lineas[clave] = {"id": por_nodo[nodo["id"]]["id"], "lineKey": por_nodo[nodo["id"]]["lineKey"],
                         "codigo": nodo["code"]}
    return {"id": p["id"], "version": version, "ruta": ruta, "lineas": lineas}


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


def proveedor(nombre, rnc):
    return c.proveedor({"name": nombre, "tin": rnc}, False)


def compra_de_obra(b, proveedor_id, ncf, concepto, monto, clave, fecha="2026-11-10", emitir=True):
    """Factura de compra B01 de un servicio para una partida del proyecto."""
    f = llamar("POST", "/v1/invoices/inline", {
        "issuedDate": fecha, "ncfType": c.ncf_tipo("B01"), "partner": proveedor_id, "paymentType": 2,
        "paymentDueDate": "2026-12-10", "currency": c.DOP, "goods606Category": "02", "ncf": ncf,
        "recordAsPurchase": True, "project": b["proyecto"]["id"], "notes": concepto,
        "details": [{"productName": concepto, "goodOrServiceIndicator": 2, "quantity": 1, "unitPrice": monto,
                     "tax": c.ITBIS_18, "projectBudgetLine": b["presupuesto"]["lineas"][clave]["id"]}]})
    if emitir:
        llamar("PATCH", f"/v1/invoices/change-status/{f['invoiceNumber']}", {"invoiceStatusCode": "EMITTED"})
    return f["invoiceNumber"]


def orden_de_obra(b, proveedor_id, producto, cantidad, precio, clave):
    """Orden de compra del proyecto, aprobada por Laura: queda como compromiso."""
    o = llamar("POST", "/v1/orders", {
        "orderType": "PURCHASE", "partnerId": proveedor_id, "requestedDeliveryDate": "2026-12-01",
        "warehouseId": b["almacen"], "project": b["proyecto"]["id"],
        "orderLines": [{"productId": producto, "quantity": cantidad, "unitPrice": precio,
                        "projectBudgetLine": b["presupuesto"]["lineas"][clave]["id"]}]})
    llamar("POST", f"/v1/orders/{o['id']}/submit-approval", {})
    como("laura.mendez", "POST", f"/v1/orders/{o['id']}/approve", {})
    return o


def control():
    # P05: presupuesto aprobado, una compra ya contabilizada en Excavación
    # (250,000 de real) y una orden aprobada de acero (450,000 comprometidos).
    b = aprobado()
    b["movitierra"] = proveedor("Movimientos de Tierra Germiva S.R.L.", "130555041")
    b["aceros"] = proveedor("Aceros Germiva del Caribe S.R.L.", "130555051")
    compra_de_obra(b, b["movitierra"], "B0100000321", "Excavación de zapatas, primera etapa", 250000, "exc")
    acero = llamar("POST", "/v1/product", {
        "category": "PRODUCT", "name": "Acero estructural A36", "code": "MAT-ACERO", "tax": c.ITBIS_18,
        "unitMeasure": TON, "unitMeasureValue": "1", "managesInventory": True, "active": True})["id"]
    orden_de_obra(b, b["aceros"], acero, 10, 45000, "est")
    # En borrador: la segunda etapa excede lo disponible de la partida (190,000).
    compra_de_obra(b, b["movitierra"], "B0100000322", "Excavación de zapatas, segunda etapa", 200000, "exc",
                   fecha="2026-11-18", emitir=False)
    return b


def cambios():
    # P06: presupuesto aprobado y una orden de cambio deductiva que Laura
    # preparó y envió: el video la aprueba con el administrador.
    b = aprobado()
    ruta = f"/v1/project-budgets/{b['presupuesto']['id']}/change-orders"
    orden = como("laura.mendez", "POST", ruta, {
        "changeType": "DEDUCTIVE", "origin": "CLIENT", "title": "Luminarias que suple el cliente",
        "requestDate": "2026-11-16", "scheduleDays": 0, "clientReference": "Correo del 16 de noviembre",
        "description": "El cliente comprará las luminarias por su cuenta.",
        "lines": [{"kind": "EXISTING_LINE", "budgetLine": b["presupuesto"]["lineas"]["ele"]["id"],
                   "quantity": "0", "costAmount": "-30000.00", "priceAmount": "-39600.00"}]})
    como("laura.mendez", "POST", f"{ruta}/{orden['id']}/submit", {})
    return b


def servicio_de_obra():
    """Servicio con que se arma la línea de las facturas del contrato: obra con
    materiales (base presunta del 10 %, Norma 07-2007)."""
    regimen = int(sql("SELECT id FROM presumptive_tax_regimes WHERE code='NORMA-07-2007-CONSTRUCCION' "
                      "AND deleted_at IS NULL LIMIT 1"))
    return llamar("POST", "/v1/product", {
        "name": "Construcción de nave industrial", "code": "SRV-OBRA", "category": "SERVICE",
        "description": "Construcción de nave industrial con materiales", "tax": c.ITBIS_18, "unitMeasure": UND,
        "unitMeasureValue": "1", "managesInventory": False, "presumptiveTaxRegime": regimen})["id"]


def facturacion():
    # P07: presupuesto aprobado y el servicio de la factura; el video registra
    # el contrato y factura el anticipo.
    b = aprobado()
    b["servicio"] = servicio_de_obra()
    return b


def contrato(b, **extra):
    ruta = f"/v1/project-billing/projects/{b['proyecto']['id']}"
    llamar("PUT", f"{ruta}/contract", {
        "budget": b["presupuesto"]["id"], "currency": c.DOP, "originalAmount": "6600000.00",
        "advancePercentage": "20", "amortizationPercentage": "20", "retentionPercentage": "5",
        "retentionBase": "GROSS", "retentionReleaseTerms": "Recepción definitiva de la obra sin defectos",
        "retentionReleaseDate": "2027-10-30", "taxRegime": "CONSTRUCTION_WITH_MATERIALS",
        "billingMode": "PROGRESS", "product": b["servicio"], "ncfType": c.ncf_tipo("B01"),
        "paymentTermDays": 30, **extra})
    return ruta


def emitir(numero):
    llamar("PATCH", f"/v1/invoices/change-status/{numero}", {"invoiceStatusCode": "EMITTED"})


def cubicacion():
    # P08: contrato registrado y anticipo facturado y emitido; el video mide,
    # aprueba y factura la primera cubicación.
    b = facturacion()
    ruta = contrato(b)
    doc = llamar("POST", f"{ruta}/advance/invoice", {"issuedDate": "2026-11-05"})
    b["anticipo"] = doc.get("invoiceNumber") or (doc.get("invoice") or {}).get("invoiceNumber")
    if b["anticipo"]:
        emitir(b["anticipo"])
    return b


def subcontrato():
    # P09: presupuesto aprobado, el subcontratista de la excavación y su primera
    # factura en borrador (200,000), todavía sin subcontrato.
    b = aprobado()
    b["movitierra"] = proveedor("Movimientos de Tierra Germiva S.R.L.", "130555041")
    compra_de_obra(b, b["movitierra"], "B0100000321", "Excavación de zapatas, primera etapa", 200000, "exc",
                   emitir=False)
    return b


def empleado(nombre, numero, usuario_, puesto):
    """Empleado con su usuario (rol sin administración) para registrar sus horas."""
    rol = int(sql("SELECT id FROM roles WHERE is_admin_role=1 AND deleted_at IS NULL ORDER BY id LIMIT 1"))
    e = llamar("POST", "/v1/employees", {
        "name": nombre, "documentType": "DOCUMENTO_EXTRANJERO", "foreignDocumentNumber": f"GER-{numero}",
        "employeeNumber": numero, "position": puesto, "hireDate": "2026-01-05",
        "user": {"username": usuario_, "email": f"{usuario_}@constructora.germiva.com", "password": CLAVE,
                 "roleIds": [rol]}})
    sql(f"UPDATE users SET emailVerified=1 WHERE username='{usuario_}'")
    return e["id"]


def dias(lunes, horas):
    import datetime
    base = datetime.date.fromisoformat(lunes)
    return [{"date": str(base + datetime.timedelta(days=i)), "hours": str(h)} for i, h in enumerate(horas) if h]


def horas():
    # P10: presupuesto aprobado; dos albañiles con tarifa por puesto; la hoja de
    # Juan de la semana del 9 de noviembre enviada a aprobación (40 h en Zapatas).
    b = aprobado()
    llamar("PUT", "/v1/project-timesheets/settings", {"maxHoursPerDay": "12.00", "overtimeFactor": "1.3500",
                                                      "allowFutureDays": True, "trueUpWithPayroll": True})
    b["albanil"] = llamar("POST", "/v1/positions", {"code": "OBR-ALB", "name": "Albañil"})["id"]
    b["ayudante"] = llamar("POST", "/v1/positions", {"code": "OBR-AYU", "name": "Ayudante de obra"})["id"]
    b["juan"] = empleado("Juan Pérez Germiva", "OBR-001", "juan.perez", b["albanil"])
    b["ramon"] = empleado("Ramón Díaz Germiva", "OBR-002", "ramon.diaz", b["ayudante"])
    llamar("POST", "/v1/project-labor-rates", {"position": b["albanil"], "validFrom": "2026-01-01",
                                                "baseHourlyCost": "250.0000", "burdenPercentage": "30",
                                                "notes": "Tarifa de obra 2026"})
    hoja = como("juan.perez", "POST", "/v1/project-timesheets", {
        "weekStart": "2026-11-09",
        "lines": [{"project": b["proyecto"]["id"], "budgetLine": b["presupuesto"]["lineas"]["zap"]["id"],
                   "days": dias("2026-11-09", [8, 8, 8, 8, 8])}]})
    como("juan.perez", "POST", f"/v1/project-timesheets/{hoja['id']}/submit", {})
    return b


def hitos():
    # P12: un proyecto de servicios que se cobra por hitos: contrato de 600,000
    # con dos hitos (30 % y 40 %); el video agrega el tercero y factura el primero.
    b = base()
    b["proyecto"] = proyecto(b, "Supervisión de la nave Haina",
                             "Supervisión técnica de la construcción de la nave.", costCenter=None, warehouse=None)
    servicio = llamar("POST", "/v1/product", {
        "name": "Supervisión de obra", "code": "SRV-SUPERV", "category": "SERVICE",
        "description": "Supervisión técnica de obra", "tax": c.ITBIS_18, "unitMeasure": UND,
        "unitMeasureValue": "1", "managesInventory": False})["id"]
    ruta = f"/v1/project-billing/projects/{b['proyecto']['id']}"
    llamar("PUT", f"{ruta}/contract", {"currency": c.DOP, "originalAmount": "600000.00", "advancePercentage": "0",
                                       "retentionPercentage": "0", "taxRegime": "STANDARD",
                                       "billingMode": "MILESTONES", "product": servicio,
                                       "ncfType": c.ncf_tipo("B01"), "paymentTermDays": 30})
    llamar("POST", f"{ruta}/milestones", {"name": "Planos revisados y aprobados", "percentage": "30",
                                          "plannedDate": "2026-11-20",
                                          "condition": "Planos firmados por el cliente"})
    llamar("POST", f"{ruta}/milestones", {"name": "Estructura terminada", "percentage": "40",
                                          "plannedDate": "2027-02-15"})
    return b


def cierre():
    # P13: la obra con una orden de acero sin facturar (compromiso abierto) y
    # el contrato de venta registrado: el video intenta completar el proyecto.
    b = control()
    b["servicio"] = servicio_de_obra()
    contrato(b)
    llamar("PATCH", f"/v1/projects/{b['proyecto']['id']}", {"status": "IN_PROGRESS"})
    return b


def consolidar():
    # C46: la obra con su presupuesto aprobado y el presupuesto contable anual
    # de la empresa en borrador, con los gastos fijos: el video le incorpora la obra.
    b = aprobado()
    c.quitar_presupuestos_de_la_instantanea()
    def renglon(codigo, mes, monto):
        return {"accountChart": c.cuenta(codigo), "period": mes, "fiscalYear": 2026, "budgetAmount": monto}
    llamar("POST", "/v1/budgets", {
        "code": "PRES-2026", "name": "Presupuesto anual 2026", "type": "annual",
        "startDate": "2026-01-01", "endDate": "2026-12-31",
        "budgetDetails": [renglon("6.03.02", "november", 60000), renglon("6.03.02", "december", 60000),
                          renglon("6.03.03", "november", 20000), renglon("6.03.03", "december", 20000)]})
    return b


def resolver_compromiso():
    """Entre dos pasos del video de cierre: la orden de acero ya no va y se anula.
    Entra como Laura: un inicio de sesión del administrador cerraría la del navegador."""
    orden = sql("SELECT o.id FROM orders o JOIN projects p ON p.id=o.project_id "
                "WHERE p.deleted_at IS NULL AND o.deleted_at IS NULL ORDER BY o.id DESC LIMIT 1")
    c.TOKEN = token_de("laura.mendez")
    llamar("PATCH", f"/v1/orders/{int(orden)}/status/CANCELED", {"reason": "El acero restante lo suple el cliente"})


ESTADOS = {"inicio": inicio, "con-proyecto": con_proyecto, "borrador": borrador,
           "por-aprobar": por_aprobar, "aprobado": aprobado, "control": control, "cambios": cambios, "facturacion": facturacion,
           "cubicacion": cubicacion, "subcontrato": subcontrato, "horas": horas, "avance": control, "hitos": hitos, "cierre": cierre, "consolidar": consolidar}

if __name__ == "__main__":
    if sys.argv[1] == "resolver-compromiso":
        resolver_compromiso()
        sys.exit(0)
    c.TOKEN = c.token()
    ESTADOS[sys.argv[1]]()
