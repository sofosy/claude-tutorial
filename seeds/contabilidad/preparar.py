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


ESTADOS = {"panel": panel, "catalogo": catalogo, "balance-inicial": balance_inicial, "bancos": bancos,
           "cierre-mensual": cierre_mensual, "cierre-anual": cierre_anual,
           "revaluacion": revaluacion}

if __name__ == "__main__":
    TOKEN = token()
    ESTADOS[sys.argv[1]]()
