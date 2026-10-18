"""Arma por el API el estado que cada video de Contabilidad encuentra hecho.

Los estados se apoyan unos en otros en el orden en que se ven los videos:
el balance inicial usa la cuenta bancaria creada en el del catálogo, y el de
bancos parte del balance inicial ya contabilizado.
"""
import json
import subprocess
import sys
import urllib.error
import urllib.request

API = "http://localhost:3001/api"
USD, DOP = 1, 32
CUENTA_BANCOS = 6          # 1.01.01.02 Bancos (agrupadora)
CAPITAL = 99               # 3.01.01.01.01 Capital social autorizado
CXC = 10                   # 1.01.02.01.01 Cuentas por cobrar clientes
CAJA = 5                   # 1.01.01.01.02 Caja general
VENTAS = 114               # 4.01.01 Ventas
SUELDOS = 143              # 6.02.01.01 Sueldos y salarios
MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
         "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]


def token():
    r = llamar("POST", "/auth/dev/login", {"username": "admin", "password": "admin"}, sin_token=True)
    return r["accessToken"]


TOKEN = None


def llamar(metodo, ruta, cuerpo=None, sin_token=False):
    cab = {"Content-Type": "application/json"}
    if not sin_token:
        cab["Authorization"] = f"Bearer {TOKEN}"
    datos = json.dumps(cuerpo).encode() if cuerpo is not None else None
    req = urllib.request.Request(API + ruta, data=datos, headers=cab, method=metodo)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            txt = r.read().decode()
            return json.loads(txt) if txt else {}
    except urllib.error.HTTPError as e:
        raise SystemExit(f"{metodo} {ruta} → {e.code}: {e.read().decode()[:400]}")


def sql(consulta):
    r = subprocess.run(["docker", "exec", "-i", "germiva-dev-mysql", "mysql", "-uroot", "germiva",
                        "-N", "-e", consulta], capture_output=True, text=True, check=True)
    return r.stdout.strip()


def periodo(nombre):
    return int(sql(f"SELECT id FROM accounting_periods WHERE company_id=1 AND name='{nombre}' "
                   "AND deleted_at IS NULL LIMIT 1"))


def cuenta(codigo):
    """Id de una cuenta del catálogo base por su código."""
    return int(sql(f"SELECT id FROM accounting_chart WHERE code='{codigo}' AND deleted_at IS NULL "
                   "ORDER BY company_id IS NULL, id LIMIT 1"))


def socio(nombre, rnc, tipo):
    cuerpo = {"name": nombre, "tin": rnc, "partnerType": [tipo], "partnerCategory": "BUSINESS"}
    if tipo == "CUSTOMER":
        cuerpo["customerType"] = "REGULAR"
    return llamar("POST", "/v1/partner", cuerpo)["id"]


# ── estados ──────────────────────────────────────────────────────────────────

def catalogo():
    socio("Ferretería Germiva del Este", "130555011", "CUSTOMER")


def balance_inicial():
    catalogo()
    llamar("POST", "/v1/accounting-chart", {
        "name": "Banco BHD - Cuenta corriente", "code": "1.01.01.02.02", "type": "asset",
        "nature": "debit", "level": 5, "parent": CUENTA_BANCOS, "allowsMovement": True})


def bancos():
    balance_inicial()
    cliente = int(sql("SELECT id FROM partners WHERE company_id=1 AND tin='130555011'"))
    llamar("POST", "/v1/accounts-receivable/opening-balance", {
        "partner": cliente, "amount": 45000, "issueDate": "2026-10-01",
        "documentNumber": "FAC-2026-0187", "description": "Saldo pendiente al inicio"})
    banco = int(sql("SELECT id FROM accounting_chart WHERE code='1.01.01.02.02'"))
    llamar("POST", "/v1/journal-entry/opening-balance", {
        "date": "2026-10-01", "description": "Balance inicial",
        "details": [
            {"accountId": banco, "description": "Saldo en Banco BHD", "debitAmount": 250000},
            {"accountId": CXC, "description": "Clientes", "debitAmount": 45000},
            {"accountId": CAPITAL, "description": "Capital aportado", "creditAmount": 295000},
        ]})


def cierre_mensual():
    # Abril a agosto ya cerrados: el video cierra septiembre. Un asiento en
    # borrador de septiembre muestra el bloqueo que el sistema aplica.
    for mes in MESES[3:8]:
        llamar("PUT", f"/v1/accounting-periods/{periodo(f'{mes} 2026')}/close", {})
    llamar("POST", "/v1/journal-entry", {
        "date": "2026-09-28", "accountingPeriodId": periodo("Septiembre 2026"),
        "description": "Pago de nómina de septiembre", "type": "manual",
        "details": [
            {"accountId": SUELDOS, "description": "Sueldos de septiembre", "debitAmount": 85000},
            {"accountId": CAJA, "description": "Pago de nómina", "creditAmount": 85000},
        ]})


def asiento_contabilizado(fecha, periodo_id, descripcion, lineas):
    je = llamar("POST", "/v1/journal-entry", {
        "date": fecha, "accountingPeriodId": periodo_id, "description": descripcion,
        "type": "manual", "details": lineas})
    llamar("POST", f"/v1/journal-entry/{je['id']}/post", {})
    return je


def cierre_anual():
    # 2025 solo tenía de enero a abril: se completa el calendario, se registra
    # la operación del año y quedan cerrados todos los meses menos diciembre.
    for n in range(5, 13):
        fin = sql(f"SELECT LAST_DAY('2025-{n:02d}-01')")
        llamar("POST", "/v1/accounting-periods", {
            "name": f"{MESES[n - 1]} 2025", "type": "monthly", "startDate": f"2025-{n:02d}-01",
            "endDate": fin, "fiscalYear": 2025, "periodNumber": n})
    nov = periodo("Noviembre 2025")
    asiento_contabilizado("2025-11-20", nov, "Ventas de contado del año", [
        {"accountId": CAJA, "description": "Cobros del año", "debitAmount": 1500000},
        {"accountId": VENTAS, "description": "Ventas del año", "creditAmount": 1500000}])
    asiento_contabilizado("2025-11-28", nov, "Sueldos pagados en el año", [
        {"accountId": SUELDOS, "description": "Sueldos del año", "debitAmount": 900000},
        {"accountId": CAJA, "description": "Pagos del año", "creditAmount": 900000}])
    for n in range(5, 12):
        llamar("PUT", f"/v1/accounting-periods/{periodo(f'{MESES[n - 1]} 2025')}/close", {})


def revaluacion():
    cliente = socio("Importadora Germiva Caribe", "130555021", "CUSTOMER")
    proveedor = socio("Germiva Supplies Miami", "130555022", "SUPPLIER")
    for fecha, tasa in (("2026-09-10", 58.50), ("2026-09-30", 60.25)):
        llamar("POST", "/v1/exchange-rates", {"fromCurrencyId": USD, "toCurrencyId": DOP,
                                              "rate": tasa, "effectiveDate": fecha})
    llamar("POST", "/v1/accounts-receivable/opening-balance", {
        "partner": cliente, "amount": 2000, "currency": USD, "exchangeRate": 58.50,
        "issueDate": "2026-09-10", "documentNumber": "FAC-USD-0042",
        "description": "Venta en dólares pendiente de cobro"})
    llamar("POST", "/v1/accounts-payable/opening-balance", {
        "partner": proveedor, "amount": 1000, "currency": USD, "exchangeRate": 58.50,
        "issueDate": "2026-09-10", "documentNumber": "INV-7781",
        "description": "Compra en dólares pendiente de pago"})


def panel():
    # Un mes con movimiento: ventas y sueldos contabilizados, un alquiler en
    # borrador y un cliente con su factura vencida, para que el panel y la
    # Vista 360 tengan qué mostrar.
    catalogo()
    oct_ = periodo("Octubre 2026")
    asiento_contabilizado("2026-10-05", oct_, "Ventas de contado de la primera quincena", [
        {"accountId": CAJA, "description": "Cobros en efectivo", "debitAmount": 320000},
        {"accountId": VENTAS, "description": "Ventas", "creditAmount": 320000}])
    asiento_contabilizado("2026-10-10", oct_, "Sueldos de la primera quincena", [
        {"accountId": SUELDOS, "description": "Sueldos", "debitAmount": 145000},
        {"accountId": CAJA, "description": "Pago de nómina", "creditAmount": 145000}])
    llamar("POST", "/v1/journal-entry", {
        "date": "2026-10-15", "accountingPeriodId": oct_, "description": "Pago de alquiler de octubre",
        "type": "manual", "details": [
            {"accountId": cuenta("6.03.02"), "description": "Alquiler del local", "debitAmount": 25000},
            {"accountId": CAJA, "description": "Pago en efectivo", "creditAmount": 25000}]})
    cliente = int(sql("SELECT id FROM partners WHERE company_id=1 AND tin='130555011'"))
    llamar("POST", "/v1/accounts-receivable/opening-balance", {
        "partner": cliente, "amount": 38500, "issueDate": "2026-09-01", "dueDate": "2026-09-30",
        "documentNumber": "FAC-2026-0142", "description": "Factura de agosto pendiente"})


def cuentas():
    # Dos cuentas propias de la empresa (una para desactivar, otra para
    # eliminar) y una creada sin padre, que por eso queda sin clasificar.
    balance_inicial()
    llamar("POST", "/v1/accounting-chart", {
        "name": "Caja chica sucursal Santiago", "code": "1.01.01.01.03", "type": "asset",
        "nature": "debit", "level": 5, "parent": cuenta("1.01.01.01"), "allowsMovement": True})
    llamar("POST", "/v1/accounting-chart", {
        "name": "Gastos de representación", "code": "9", "type": "expense",
        "nature": "debit", "level": 1, "allowsMovement": True})


def mapeo():
    # Un rol pendiente: el mapeo de «Gasto por comisiones bancarias» quedó
    # inactivo (alguien lo apagó), así que los cargos del banco no se pueden
    # contabilizar hasta que se le asigne cuenta desde su propia fila.
    balance_inicial()
    sql("UPDATE account_mappings SET active=0 WHERE company_id=1 "
        "AND required_mapping_type='bank_charge_expense' AND deleted_at IS NULL")


def autoposteo():
    # Dos centros de costo para asignar (por tipo de operación y general), la
    # cuenta «9» sin clasificar y el Libro Mayor apagado: lo que el Estado de
    # la Configuración tiene que señalar.
    cuentas()
    for codigo, nombre in (("ADM", "Administración"), ("VEN", "Ventas")):
        llamar("POST", "/v1/cost-centers", {
            "code": codigo, "name": nombre, "type": "cost", "allowsDirectPosting": True})
    sql("UPDATE company_configs SET auto_generate_general_ledger=0 WHERE company_id=1")


ARRENDAMIENTOS, SERVICIOS_PUBLICOS, OFICINA, HONORARIOS, ONLINE, SEGUROS = 158, 159, 164, 157, 167, 166


def linea(cuenta_id, descripcion, debito=0, credito=0):
    return {"accountId": cuenta_id, "description": descripcion, "debitAmount": debito, "creditAmount": credito}


def asientos():
    # V12: un borrador, un contabilizado y uno aprobado en octubre, para que la
    # lista muestre las acciones de cada estado.
    balance_inicial()
    oct_ = periodo("Octubre 2026")
    llamar("POST", "/v1/journal-entry", {
        "date": "2026-10-12", "accountingPeriodId": oct_, "type": "manual",
        "description": "Factura de luz de octubre",
        "details": [linea(SERVICIOS_PUBLICOS, "Energía eléctrica", 8750),
                    linea(CAJA, "Pago en efectivo", credito=8750)]})
    asiento_contabilizado("2026-10-05", oct_, "Compra de artículos de oficina", [
        linea(OFICINA, "Papelería y tóner", 4200), linea(CAJA, "Pago en efectivo", credito=4200)])
    je = asiento_contabilizado("2026-10-03", oct_, "Honorarios del contador de septiembre", [
        linea(HONORARIOS, "Honorarios profesionales", 15000), linea(CAJA, "Pago en efectivo", credito=15000)])
    llamar("POST", f"/v1/journal-entry/{je['id']}/approve", {})


def plantilla_recurrente(nombre, descripcion, inicio, dia, cuenta_id, monto, frecuencia="monthly"):
    return llamar("POST", "/v1/journal-entry/recurring", {
        "name": nombre, "description": descripcion, "frequency": frecuencia,
        "dayOfMonth": dia, "startDate": inicio,
        "templateDetails": [linea(cuenta_id, descripcion, monto), linea(CAJA, "Pago en efectivo", credito=monto)]})


def reversar():
    # V13: el alquiler se registró por 52,000 en vez de 25,000 (hay que
    # reversarlo) y un asiento automático, generado por una recurrente, para
    # ver el aviso de reversar algo que salió de un documento.
    balance_inicial()
    oct_ = periodo("Octubre 2026")
    asiento_contabilizado("2026-10-15", oct_, "Pago de alquiler de octubre", [
        linea(ARRENDAMIENTOS, "Alquiler del local", 52000), linea(CAJA, "Pago en efectivo", credito=52000)])
    rec = plantilla_recurrente("Servicio de internet", "Internet de la oficina", "2026-10-01", 1, ONLINE, 3500)
    llamar("POST", f"/v1/journal-entry/recurring/{rec['id']}/generate", {})


def recurrentes():
    # V14: una plantilla vencida (Generar Ahora funciona) y una que empieza en
    # noviembre (todavía no corresponde).
    balance_inicial()
    plantilla_recurrente("Servicio de internet", "Internet de la oficina", "2026-10-01", 1, ONLINE, 3500)
    plantilla_recurrente("Seguro del local", "Póliza del local comercial", "2026-11-01", 5, SEGUROS, 12000,
                         frecuencia="quarterly")


def mayor():
    # V16: un mes con movimiento en caja, banco, ventas y gastos.
    bancos()
    oct_ = periodo("Octubre 2026")
    asiento_contabilizado("2026-10-05", oct_, "Ventas de contado de la primera quincena", [
        linea(CAJA, "Cobros en efectivo", 320000), linea(VENTAS, "Ventas", credito=320000)])
    asiento_contabilizado("2026-10-10", oct_, "Sueldos de la primera quincena", [
        linea(SUELDOS, "Sueldos", 145000), linea(CAJA, "Pago de nómina", credito=145000)])
    asiento_contabilizado("2026-10-15", oct_, "Pago de alquiler de octubre", [
        linea(ARRENDAMIENTOS, "Alquiler del local", 25000), linea(CAJA, "Pago en efectivo", credito=25000)])
    asiento_contabilizado("2026-10-16", oct_, "Compra de artículos de oficina", [
        linea(OFICINA, "Papelería y tóner", 4200), linea(CAJA, "Pago en efectivo", credito=4200)])


def automaticos():
    # V15: un ajuste de inventario por conteo físico que no se pudo
    # contabilizar (el mapeo «Otros Ingresos por Ajuste de Inventario» estaba
    # apagado) y cuya causa ya se corrigió: el video lo encuentra en el
    # Registro de Integración y lo contabiliza.
    balance_inicial()
    mapeo_id = sql("SELECT id FROM account_mappings WHERE company_id=1 AND deleted_at IS NULL "
                   "AND required_mapping_type='inventory_adjustment_gain_other_income'")
    llamar("PATCH", f"/v1/accounting-integration/account-mappings/{mapeo_id}", {"active": False})
    ubicacion = llamar("POST", "/v1/inventory/location", {
        "warehouse": 1, "position": "A-01", "description": "Estante principal"})
    llamar("POST", "/v1/inventory/movement/entry", {
        "product": 1, "batchNumber": "L-CONTEO-10", "quantity": 12, "inventoryMovementType": 3,
        "unitPrice": "85.00", "inventoryLocation": ubicacion["id"], "notes": "Conteo físico de octubre"})
    llamar("PATCH", f"/v1/accounting-integration/account-mappings/{mapeo_id}", {"active": True})


# ── lote C: informes, períodos y cierre ─────────────────────────────────────

def completar_2025():
    """El calendario de 2025 solo traía de enero a abril."""
    for n in range(5, 13):
        fin = sql(f"SELECT LAST_DAY('2025-{n:02d}-01')")
        llamar("POST", "/v1/accounting-periods", {
            "name": f"{MESES[n - 1]} 2025", "type": "monthly", "startDate": f"2025-{n:02d}-01",
            "endDate": fin, "fiscalYear": 2025, "periodNumber": n})


def prestamo_largo_plazo():
    """Sin una cuenta de pasivo no corriente el préstamo caería en Operación."""
    return llamar("POST", "/v1/accounting-chart", {
        "code": "2.02.01.01.01", "name": "Préstamo Banco Popular a largo plazo", "type": "liability",
        "nature": "credit", "level": 5, "parent": cuenta("2.02.01.01"), "allowsMovement": True,
        "reportSection": "LONG_TERM_DEBT", "isMonetary": True})["id"]


# Año de operación de la distribuidora: resultado 2025 = 96,000 y 2026 hasta
# septiembre = 238,000 (Banco nunca queda en negativo).
OPERACION = [
    ("2025-05-02", "Aporte de capital inicial", [("1.01.01.02.01", 1000000, 0), ("3.01.01.01.01", 0, 1000000)]),
    ("2025-05-05", "Préstamo bancario a largo plazo", [("1.01.01.02.01", 500000, 0), ("2.02.01.01.01", 0, 500000)]),
    ("2025-05-10", "Compra de mobiliario de oficina", [("1.02.01.03.01", 240000, 0), ("1.01.04.02", 43200, 0),
                                                      ("1.01.01.02.01", 0, 283200)]),
    ("2025-06-15", "Compra de inventario a crédito", [("1.01.06.01", 400000, 0), ("1.01.04.02", 72000, 0),
                                                     ("2.01.01.01.01", 0, 472000)]),
    ("2025-07-20", "Venta a crédito", [("1.01.02.01.01", 472000, 0), ("4.01.01", 0, 400000),
                                       ("2.01.04.01.01.01", 0, 72000)]),
    ("2025-07-20", "Costo de la venta a crédito", [("5.01.01.01", 220000, 0), ("1.01.06.01", 0, 220000)]),
    ("2025-08-31", "Gastos de agosto", [("6.02.01.01", 120000, 0), ("6.03.02", 60000, 0), ("6.03.03", 15000, 0),
                                        ("1.01.01.02.01", 0, 195000)]),
    ("2025-09-15", "Cobro a cliente", [("1.01.01.02.01", 472000, 0), ("1.01.02.01.01", 0, 472000)]),
    ("2025-10-10", "Pago a proveedor", [("2.01.01.01.01", 472000, 0), ("1.01.01.02.01", 0, 472000)]),
    ("2025-11-30", "Venta al contado", [("1.01.01.02.01", 354000, 0), ("4.01.01", 0, 300000),
                                        ("2.01.04.01.01.01", 0, 54000)]),
    ("2025-11-30", "Costo de la venta al contado", [("5.01.01.01", 150000, 0), ("1.01.06.01", 0, 150000)]),
    ("2025-12-31", "Depreciación del mobiliario", [("6.03.22.02.02", 14000, 0), ("1.02.01.03.01.01", 0, 14000)]),
    ("2025-12-31", "Intereses del préstamo", [("6.04.01", 25000, 0), ("1.01.01.02.01", 0, 25000)]),
    ("2026-04-15", "Compra de inventario al contado", [("1.01.06.01", 200000, 0), ("1.01.04.02", 36000, 0),
                                                      ("1.01.01.02.01", 0, 236000)]),
    ("2026-05-20", "Venta a crédito", [("1.01.02.01.01", 590000, 0), ("4.01.01", 0, 500000),
                                       ("2.01.04.01.01.01", 0, 90000)]),
    ("2026-05-20", "Costo de la venta a crédito", [("5.01.01.01", 180000, 0), ("1.01.06.01", 0, 180000)]),
    ("2026-06-10", "Compra de vehículo de reparto", [("1.02.01.03.02", 800000, 0), ("1.01.01.02.01", 0, 800000)]),
    ("2026-06-30", "Gastos de junio", [("6.02.01.01", 130000, 0), ("6.03.02", 60000, 0), ("6.03.03", 18000, 0),
                                       ("6.05.01", 2000, 0), ("1.01.01.02.01", 0, 210000)]),
    ("2026-07-15", "Cobro parcial a cliente", [("1.01.01.02.01", 400000, 0), ("1.01.02.01.01", 0, 400000)]),
    ("2026-08-05", "Abono al préstamo e intereses", [("2.02.01.01.01", 100000, 0), ("6.04.01", 20000, 0),
                                                    ("1.01.01.02.01", 0, 120000)]),
    ("2026-09-10", "Venta al contado", [("1.01.01.01.02", 236000, 0), ("4.01.01", 0, 200000),
                                        ("2.01.04.01.01.01", 0, 36000)]),
    ("2026-09-10", "Costo de la venta al contado", [("5.01.01.01", 40000, 0), ("1.01.06.01", 0, 40000)]),
    ("2026-09-30", "Aporte adicional de capital", [("1.01.01.02.01", 200000, 0), ("3.01.01.01.01", 0, 200000)]),
    ("2026-09-30", "Depreciación del mobiliario", [("6.03.22.02.02", 12000, 0), ("1.02.01.03.01.01", 0, 12000)]),
]


def informes():
    # V17/V18: año y medio de operación, con el préstamo en una cuenta de
    # largo plazo para que salga en Financiamiento.
    completar_2025()
    prestamo_largo_plazo()
    ids = {}
    for fecha, descripcion, lineas in OPERACION:
        anio, mes = int(fecha[:4]), int(fecha[5:7])
        detalles = []
        for codigo, debito, credito in lineas:
            ids.setdefault(codigo, cuenta(codigo))
            detalles.append(linea(ids[codigo], descripcion, debito, credito))
        asiento_contabilizado(fecha, periodo(f"{MESES[mes - 1]} {anio}"), descripcion, detalles)


def cierre_reversar():
    # V21: el ejercicio 2025 cerrado (CIE-2025-0001). Mayo a noviembre se
    # cierran antes: el cierre anual exige que no quede ningún período previo
    # abierto.
    informes()
    for n in range(5, 12):
        llamar("PUT", f"/v1/accounting-periods/{periodo(f'{MESES[n - 1]} 2025')}/close", {})
    llamar("POST", "/v1/accounting-closing/execute", {
        "accountingPeriodId": periodo("Diciembre 2025"), "resultAccountCode": "3.03.01",
        "retainedEarningsAccountCode": "3.04", "notes": "Cierre del ejercicio 2025",
        "createNextPeriod": False, "confirmWithoutIncomeTaxProvision": True})


def periodos():
    # V19 y V20 parten de la instantánea: meses de 2025 y 2026 cerrados y
    # abiertos, trimestres, el año fiscal y el período de ajustes.
    pass


# ── lote D: banca, activos, centros de costo y presupuestos ─────────────────

POPULAR, BHD = 1, 3        # bancos del catálogo global
BANCO_1 = 7                # 1.01.01.02.01 Banco 1
TITULAR = "Distribuidora Germiva Demo S.R.L."


def cuentas_bancarias():
    """Banco BHD con su propia cuenta contable y Banco Popular sobre «Banco 1»."""
    gl = llamar("POST", "/v1/accounting-chart", {
        "code": "1.01.01.02.02", "name": "Banco BHD", "type": "asset", "nature": "debit", "level": 5,
        "parent": CUENTA_BANCOS, "allowsMovement": True, "reportSection": "CASH_AND_EQUIVALENTS",
        "isMonetary": True})["id"]
    llamar("POST", "/v1/bank-accounts", {
        "accountNumber": "9600123456", "accountType": "checking", "accountHolder": TITULAR, "bank": BHD,
        "currency": DOP, "glAccount": gl, "initialBalance": 100000, "openingDate": "2026-09-01"})
    llamar("POST", "/v1/bank-accounts", {
        "accountNumber": "0001234567", "accountType": "checking", "accountHolder": TITULAR, "bank": POPULAR,
        "currency": DOP, "glAccount": BANCO_1, "initialBalance": 50000, "openingDate": "2026-10-01"})
    return gl


def transferencias():
    # V22: dos cuentas en pesos con saldo, para transferir y anular.
    cuentas_bancarias()


def movimientos_bhd():
    gl = cuentas_bancarias()
    sep = periodo("Septiembre 2026")
    asiento_contabilizado("2026-09-10", sep, "Depósito transferencia cliente", [
        linea(gl, "Depósito en Banco BHD", 25000), linea(cuenta("4.02.01.02.01"), "Otros ingresos", credito=25000)])
    asiento_contabilizado("2026-09-20", sep, "Pago alquiler septiembre", [
        linea(cuenta("6.03.02"), "Alquiler septiembre", 8000), linea(gl, "Salida Banco BHD", credito=8000)])
    return gl


def conciliar():
    # V23: libros del BHD a 117,000 al 30/09 (apertura 100,000 + depósito −
    # alquiler); el extracto trae además comisiones e intereses.
    movimientos_bhd()


def activo(codigo, nombre):
    return llamar("POST", "/v1/fixed-assets", {
        "code": codigo, "name": nombre, "categoryId": 3, "acquisitionCost": 60000, "salvageValue": 0,
        "acquisitionDate": "2026-04-01", "inServiceDate": "2026-04-01", "status": "active",
        "condition": "good"})["id"]


def activos():
    # V24 crea el activo en pantalla; la instantánea no trae ninguno de la empresa.
    pass


def activos_baja():
    # V25: dos escritorios en uso desde abril, uno para dar de baja y otro
    # para vender.
    activo("ACT-OF-002", "Escritorio de recepción")
    activo("ACT-OF-003", "Archivo metálico")


def centros_costo():
    # V26: Ventas al primer nivel y Operaciones bajo Administración, para que
    # la jerarquía tenga dos niveles.
    adm = int(sql("SELECT id FROM cost_centers WHERE company_id=1 AND code='CC-ADM' AND deleted_at IS NULL"))
    llamar("POST", "/v1/cost-centers", {"code": "CC-VEN", "name": "Ventas", "type": "revenue",
                                         "budgetAmount": "150000"})
    llamar("POST", "/v1/cost-centers", {"code": "CC-OPS", "name": "Operaciones", "type": "cost",
                                         "budgetAmount": "300000", "parent": adm})


def presupuestos():
    # V27: septiembre con ingresos, alquiler y comisiones contabilizados, para
    # comparar contra el presupuesto que el video crea.
    gl = movimientos_bhd()
    asiento_contabilizado("2026-09-30", periodo("Septiembre 2026"), "Comisiones bancarias de septiembre", [
        linea(cuenta("6.05.01"), "Comisiones y servicios", 400), linea(gl, "Cargo del banco", credito=400)])


# ── La firma contable y sus clientes (videos 28–33) ─────────────────────────
# Todo ficticio: la firma «Germiva Contadores» y sus clientes con RNC 130555xxx.
# El admin es el contador de la firma; cada estado deja su sesión en la
# empresa donde arranca el video.

FIRMA = {"legalName": "Germiva Contadores & Asociados S.R.L.", "tradeName": "Germiva Contadores",
         "rnc": "130555090", "phones": ["809-555-0190"], "email": "firma@contadores.germiva.com"}
COLMADO = {"legalName": "Colmado Germiva del Ensanche S.R.L.", "tradeName": "Colmado Germiva",
           "rnc": "130555210", "phones": ["809-555-0210"], "email": "colmado@germiva.com"}
PLANTILLA_FIRMA = "GERMIVA_CONTADORES"


def entrar(empresa_id):
    """La sesión del admin pasa a esa empresa: la API la toma al iniciar sesión."""
    global TOKEN
    sql(f"UPDATE users SET current_company_id={empresa_id} WHERE id=1")
    TOKEN = token()


def empresa_id(rnc):
    return int(sql(f"SELECT id FROM companies WHERE rnc='{rnc}' AND deleted_at IS NULL"))


def plantilla_id(codigo):
    return int(sql(f"SELECT id FROM accounting_chart_templates WHERE code='{codigo}' AND deleted_at IS NULL"))


def cuenta_de(empresa, codigo):
    """Cuenta del catálogo que ve la empresa: la suya con ese código o la de la plantilla."""
    return int(sql(f"SELECT id FROM accounting_chart WHERE code='{codigo}' AND deleted_at IS NULL "
                   f"AND (company_id={empresa} OR company_id IS NULL) "
                   "ORDER BY company_id IS NULL, template_id <=> 1 DESC, id LIMIT 1"))


def firma():
    """V28: la firma verificada con su catálogo ya ajustado para sus clientes."""
    firma_ = llamar("POST", "/v1/company", FIRMA)["id"]
    llamar("POST", "/v1/accountants/admin/designate", {"company": firma_, "licenseNumber": "12345"})
    entrar(firma_)
    llamar("PATCH", f"/v1/accounting-chart/{cuenta_de(firma_, '1.01.01.02.01')}/company-settings",
           {"customName": "Banco Popular - Cuenta corriente"})
    llamar("POST", "/v1/accounting-chart", {
        "name": "Banco BHD - Cuenta corriente", "code": "1.01.01.02.02", "type": "asset",
        "nature": "debit", "level": 5, "parent": CUENTA_BANCOS, "allowsMovement": True})
    llamar("POST", "/v1/accounting-chart", {
        "name": "Caja chica", "code": "1.01.01.01.03", "type": "asset", "nature": "debit",
        "level": 5, "parent": cuenta_de(firma_, "1.01.01.01"), "allowsMovement": True})
    return firma_


def firma_plantilla():
    """V29: la plantilla de la firma ya guardada con el alcance «Mi firma contable»."""
    firma_ = firma()
    llamar("POST", "/v1/accounting-chart/templates/from-current-catalog", {
        "code": PLANTILLA_FIRMA, "name": "Catálogo Germiva Contadores",
        "description": "Catálogo base de la firma para comercios y servicios", "scope": "firm"})
    return firma_


def firma_alta():
    """V30: la plantilla de la firma es la por defecto de los clientes nuevos."""
    firma_ = firma_plantilla()
    llamar("PATCH", "/v1/accountants/firm/default-chart-template",
           {"templateId": plantilla_id(PLANTILLA_FIRMA)})
    return firma_


def cliente_invitado(firma_):
    """El Colmado: empresa propia del admin (catálogo compartido) que acepta a la firma."""
    colmado = llamar("POST", "/v1/company", COLMADO)["id"]
    entrar(firma_)
    enlace = llamar("POST", "/v1/accountants/clients/invite",
                    {"rnc": COLMADO["rnc"], "accessLevel": "FULL_ADMIN"})
    entrar(colmado)
    llamar("PATCH", f"/v1/accountants/my-accountant/{enlace['link']['id']}/accept", {"confirmFullAccess": True})
    return colmado


def firma_cambio():
    """V31: un cliente dado de alta con el catálogo del sistema (sin asientos) y el
    Colmado, invitado, que comparte la plantilla del sistema."""
    firma_ = firma_alta()
    llamar("POST", "/v1/accountants/clients/create-company", {
        "rnc": "130555201", "legalName": "Ferretería Germiva del Cibao S.R.L.",
        "tradeName": "Ferretería del Cibao", "ownerEmail": "admin@ferreteria.germiva.com",
        "ownerName": "Rosa Germiva", "accessLevel": "FULL_ADMIN", "chartTemplateId": plantilla_id("GERMIVA_BASE")})
    cliente_invitado(firma_)
    entrar(empresa_id("130555201"))


def firma_asistente():
    """V32: el Colmado ya tiene su balance inicial contabilizado, con un banco que
    él mismo creó con un código que la plantilla de la firma no trae."""
    firma_ = firma_alta()
    colmado = cliente_invitado(firma_)
    banco = llamar("POST", "/v1/accounting-chart", {
        "name": "Banco Popular", "code": "1.01.01.02.05", "type": "asset", "nature": "debit",
        "level": 5, "parent": CUENTA_BANCOS, "allowsMovement": True})["id"]
    llamar("POST", "/v1/journal-entry/opening-balance", {
        "date": "2026-10-01", "description": "Balance inicial",
        "details": [
            {"accountId": banco, "description": "Saldo en Banco Popular", "debitAmount": 120000},
            {"accountId": CAJA, "description": "Efectivo en caja", "debitAmount": 15000},
            {"accountId": CAPITAL, "description": "Capital aportado", "creditAmount": 135000},
        ]})
    entrar(colmado)


ESTADOS = {"panel": panel, "cuentas": cuentas, "mapeo": mapeo, "autoposteo": autoposteo,
           "asientos": asientos, "reversar": reversar, "recurrentes": recurrentes, "mayor": mayor, "automaticos": automaticos, "catalogo": catalogo, "balance-inicial": balance_inicial, "bancos": bancos,
           "cierre-mensual": cierre_mensual, "cierre-anual": cierre_anual,
           "revaluacion": revaluacion, "informes": informes,
           "cierre-reversar": cierre_reversar, "periodos": periodos,
           "transferencias": transferencias, "conciliar": conciliar, "activos": activos,
           "activos-baja": activos_baja, "centros-costo": centros_costo, "presupuestos": presupuestos,
           "firma": firma, "firma-plantilla": firma_plantilla, "firma-alta": firma_alta,
           "firma-cambio": firma_cambio, "firma-asistente": firma_asistente}

if __name__ == "__main__":
    TOKEN = token()
    ESTADOS[sys.argv[1]]()
