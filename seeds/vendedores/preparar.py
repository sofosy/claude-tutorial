"""Arma por el API el estado que cada video de la serie Vendedores encuentra hecho.

Los estados se apoyan unos en otros en el orden en que se ven los videos:

  base       empleados con salario, productos, clientes; fichas de Carmen y Pedro
             (Luis todavía no tiene ficha: el video 01 se la crea)
  fichas     base + la ficha de Luis (V-0003, zona Norte, supervisor Pedro)
  cartera    fichas + ejecutivo de cuenta, zona, ruta y plazo de cada cliente
  ventas     cartera + esquema «Vendedores de ruta» y tres facturas emitidas
  cobradas   ventas + cobros: cada cobro genera su comisión
  liquidada  cobradas + liquidación de octubre aprobada y período de nómina
  nomina     liquidada + la nómina de la quincena calculada

Todo lo inventado lleva «Germiva» o el rango de RNC 130555 (privacidad de la serie).
"""
import datetime as dt
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request

API = "http://localhost:3001/api"
DOP = 32
B01 = 1
HOY = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=4)).date()
CLAVE_VENDEDOR = "Germiva.2026"

EMPLEADOS = [
    # nombre, apellidos, cédula, salario quincenal
    ("Carmen", "Rosario Peña", "40255500011", "22000.00"),
    ("Pedro", "Almonte Cruz", "40255500012", "30000.00"),
    ("Luis", "Gómez Díaz", "40255500013", "20000.00"),
]
PRODUCTOS = [
    # nombre, precio, costo
    ("Pintura acrílica Germiva galón", 1000, 600),
    ("Brocha Germiva 3 pulgadas", 250, 120),
]
CLIENTES = [
    # nombre, RNC, ejecutivo (nombre del empleado), zona, ruta, plazo
    ("Ferretería Germiva del Norte", "130555101", "Luis", "NORTE", "Ruta 1 Santiago", 30),
    ("Colmado Germiva Este", "130555102", "Carmen", "ESTE", "Ruta 3 La Romana", 15),
    ("Constructora Germiva Ciudad", "130555103", "Luis", "CIUDAD", "Ruta 2 Naco", 45),
]


def sql(consulta):
    r = subprocess.run(["docker", "exec", "-i", "germiva-dev-mysql", "mysql",
                        "--default-character-set=utf8mb4", "-uroot", "germiva", "-N", "-B",
                        "-e", consulta], capture_output=True, text=True, check=True)
    return r.stdout.strip()


TOKEN = None


def llamar(metodo, ruta, cuerpo=None, token=None):
    cab = {"Content-Type": "application/json", "Authorization": f"Bearer {token or TOKEN}"}
    datos = json.dumps(cuerpo).encode() if cuerpo is not None else None
    req = urllib.request.Request(API + ruta, data=datos, headers=cab, method=metodo)
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            txt = r.read().decode()
            return json.loads(txt) if txt else {}
    except urllib.error.HTTPError as e:
        raise SystemExit(f"{metodo} {ruta} → {e.code}: {e.read().decode()[:600]}")


def entrar(usuario, clave):
    req = urllib.request.Request(API + "/auth/dev/login", method="POST",
                                 data=json.dumps({"username": usuario, "password": clave}).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())["accessToken"]


def empleado(nombre):
    """Por la cédula: la base sembrada ya trae empleados llamados «Carmen» y «Luis»."""
    cedula = next(e[2] for e in EMPLEADOS if e[0] == nombre)
    return int(sql(f"SELECT id FROM partners WHERE company_id=1 AND tin='{cedula}' AND deleted_at IS NULL"))


def cliente(nombre):
    return int(sql(f"SELECT id FROM partners WHERE company_id=1 AND name='{nombre}' "
                   "AND deleted_at IS NULL ORDER BY id LIMIT 1"))


def producto(nombre):
    return int(sql(f"SELECT id FROM products WHERE company_id=1 AND name='{nombre}' "
                   "AND deleted_at IS NULL ORDER BY id LIMIT 1"))


# ── base ─────────────────────────────────────────────────────────────────────

def crear_empleados():
    puesto = int(sql("SELECT id FROM positions WHERE company_id=1 AND deleted_at IS NULL ORDER BY id LIMIT 1"))
    for nombre, apellidos, cedula, salario in EMPLEADOS:
        e = llamar("POST", "/v1/employees", {
            "name": nombre, "firstLastName": apellidos.split()[0],
            "secondLastName": apellidos.split()[1], "position": puesto,
            "hireDate": "2026-08-01T12:00:00.000Z"})
        sql(f"UPDATE partners SET tin='{cedula}' WHERE id={e['id']}")
        llamar("POST", "/v1/payroll/employee-salaries", {
            "employee": e["id"], "baseSalary": salario, "payrollFrequency": "biweekly",
            "paymentType": "fixed", "effectiveDate": "2026-08-01"})


def ubicacion():
    fila = sql("SELECT id FROM inventory_location WHERE company_id=1 AND deleted_at IS NULL ORDER BY id LIMIT 1")
    if fila:
        return int(fila)
    almacen = int(sql("SELECT id FROM warehouse WHERE company_id=1 AND deleted_at IS NULL ORDER BY id LIMIT 1"))
    return llamar("POST", "/v1/inventory/location", {
        "warehouse": almacen, "position": "A-01", "description": "Almacén principal"})["id"]


def crear_productos():
    lugar = ubicacion()
    for i, (nombre, precio, costo) in enumerate(PRODUCTOS):
        llamar("POST", "/v1/product", {
            "category": "PRODUCT", "name": nombre, "tax": 1, "purchaseTax": 1, "unitMeasure": 43,
            "unitMeasureValue": "1", "managesInventory": True, "usesBatchControl": True,
            "purchasePrice": f"{costo}.00", "productType": 12})
        pid = producto(nombre)
        llamar("POST", "/v1/price", {
            "product": pid, "price": f"{precio}.00", "priority": 1, "customerType": "REGULAR",
            "taxIncluded": False, "description": "Precio de lista"})
        llamar("POST", "/v1/inventory/movement/entry", {
            "product": pid, "batchNumber": f"L-2026-{i + 1:03d}", "quantity": 500,
            "inventoryLocation": lugar, "inventoryMovementType": 17,
            "unitPrice": costo, "layerUnitCost": costo, "notes": "Inventario inicial"})


def crear_clientes():
    for nombre, rnc, *_ in CLIENTES:
        llamar("POST", "/v1/partner", {
            "name": nombre, "tin": rnc, "partnerType": ["CUSTOMER"], "partnerCategory": "BUSINESS",
            "customerType": "REGULAR", "isInformalTaxpayer": True})


def ficha(nombre, **extra):
    return llamar("POST", "/v1/sales-reps", {"partner": empleado(nombre), **extra})


def base():
    # El aviso «Configuración incompleta» sale una sola vez por usuario y
    # empresa: se gasta aquí para que no tape la pantalla al entrar en el video.
    llamar("POST", "/v1/user-preferences/incomplete-config-notice/claim", {})
    crear_empleados()
    crear_productos()
    crear_clientes()
    ficha("Carmen", code="V-0001", salesZone="ESTE", salesRoute="Ruta 3 La Romana")
    ficha("Pedro", code="V-0002", salesZone="CIUDAD", notes="Supervisor de ventas")


# ── estados siguientes ───────────────────────────────────────────────────────

def fichas():
    base()
    # El supervisor es otra FICHA de vendedor (su id), no el empleado.
    supervisor = int(sql(f"SELECT id FROM sales_reps WHERE company_id=1 AND partner_id={empleado('Pedro')}"))
    ficha("Luis", code="V-0003", salesZone="NORTE", salesRoute="Ruta 1 Santiago",
          supervisor=supervisor, maxDiscountPercent=5)
    # La Ferretería la llevaba Carmen: el video 02 se la pasa a Luis y el
    # historial del ejecutivo de cuenta muestra los dos tramos.
    llamar("PATCH", f"/v1/sales-reps/customers/{cliente(CLIENTES[0][0])}/seller",
           {"seller": empleado("Carmen"), "reason": "Cartera inicial de la empresa"})
    sql(f"UPDATE customer_seller_assignments SET from_date='2026-08-01' WHERE customer_id={cliente(CLIENTES[0][0])}")


def usuario_de_luis():
    rol = int(sql("SELECT id FROM roles WHERE code='SALES_REP' AND company_id IS NULL"))
    llamar("PATCH", f"/v1/employees/{empleado('Luis')}", {"user": {
        "username": "luis.gomez", "email": "luis.gomez@distribuidora.germiva.com",
        "password": CLAVE_VENDEDOR, "active": True, "roleIds": [rol]}})


def cartera():
    fichas()
    usuario_de_luis()
    for nombre, _rnc, ejecutivo, zona, ruta, plazo in CLIENTES:
        llamar("PATCH", f"/v1/partner/{cliente(nombre)}", {
            "defaultSeller": empleado(ejecutivo), "salesZone": zona, "salesRoute": ruta,
            "paymentTermDays": plazo})


CAJERA = ("ana.perez", "Germiva.2026")


def caja():
    """cartera + la cajera Ana con su turno abierto en la Caja Principal: la
    venta del POS sale con la vendedora que se elige y con Ana como cajera."""
    cartera()
    rol = int(sql("SELECT id FROM roles WHERE code='CASHIER' AND company_id IS NULL"))
    llamar("POST", "/user", {"username": CAJERA[0], "email": "ana.perez@distribuidora.germiva.com",
                            "password": CAJERA[1], "name": "Ana", "lastName": "Pérez",
                            "active": True, "roles": [rol]})
    ana = int(sql(f"SELECT id FROM users WHERE username='{CAJERA[0]}'"))
    # Sin certificado digital en el entorno local el POS no puede emitir el
    # E32: durante el cobro la empresa factura con comprobantes tradicionales
    # (B02). El paso del video que abre la factura vuelve a encenderlo.
    sql("UPDATE companies SET managesElectronicBilling=0 WHERE id=1")
    llamar("POST", "/v1/cashiers/sessions/open", {"cashier": 1, "user": ana, "initialCash": 5000,
                                                 "notes": "Turno de la mañana"})


def esquema():
    llamar("POST", "/v1/commission-schemes", {
        "name": "Vendedores de ruta", "type": "percentage", "calculationBase": "sale_amount",
        "accrualTrigger": "on_each_payment", "basePercentage": 3, "effectiveDate": "2026-08-01",
        "employees": [empleado("Luis"), empleado("Carmen")],
        "productRates": [{"product": producto(PRODUCTOS[0][0]), "rate": 5}]})


def factura(nombre_cliente, lineas):
    """Factura a crédito B01, emitida. El vendedor sale del ejecutivo del cliente."""
    f = llamar("POST", "/v1/invoices", {
        "ncfType": B01, "incomeType": 1, "currency": DOP, "partner": cliente(nombre_cliente),
        "details": [{"product": producto(n), "quantity": q} for n, q in lineas]})
    llamar("PATCH", f"/v1/invoices/change-status/{f['invoiceNumber']}", {"invoiceStatusCode": "EMITTED"})
    return f["invoiceNumber"]


def ventas():
    cartera()
    esquema()
    numeros = [
        factura(CLIENTES[0][0], [(PRODUCTOS[0][0], 10), (PRODUCTOS[1][0], 8)]),   # Luis
        factura(CLIENTES[1][0], [(PRODUCTOS[1][0], 20)]),                        # Carmen
        factura(CLIENTES[2][0], [(PRODUCTOS[0][0], 6)]),                         # Luis
    ]
    with open("/tmp/vendedores-facturas.json", "w") as fh:
        json.dump(numeros, fh)
    return numeros


def total(numero):
    return float(sql(f"SELECT total FROM invoices WHERE invoice_number='{numero}' AND company_id=1"))


def cobrar(numero, monto, nota):
    llamar("POST", "/v1/payment", {"invoiceNumber": numero, "amount": f"{monto:.2f}",
                                  "amountReceived": f"{monto:.2f}", "paymentMethodCode": "TRANSFER",
                                  "notes": nota})


def esperar_comisiones(cuantas):
    for _ in range(60):
        n = int(sql("SELECT COUNT(*) FROM sales_commissions WHERE company_id=1 AND deleted_at IS NULL"))
        if n >= cuantas:
            return
        time.sleep(0.5)
    raise SystemExit(f"las comisiones no llegaron: {n} de {cuantas}")


def cobradas():
    norte, este, ciudad = ventas()
    cobrar(norte, total(norte), "Transferencia Banco Popular")
    cobrar(este, total(este), "Transferencia BHD")
    cobrar(ciudad, round(total(ciudad) / 2, 2), "Abono del 50 %")
    esperar_comisiones(3)


def liquidada():
    cobradas()
    r = llamar("POST", "/v1/commission-settlements/prepare", {"periodDate": str(HOY)})
    for sid in r["settlementIds"]:
        llamar("POST", f"/v1/commission-settlements/{sid}/submit", {})
        llamar("POST", f"/v1/commission-settlements/{sid}/approve", {"comments": "Revisada con el supervisor"})
    periodo_nomina()


def quincena():
    if HOY.day <= 15:
        return HOY.replace(day=1), HOY.replace(day=15)
    ultimo = (HOY.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
    return HOY.replace(day=16), ultimo


def periodo_nomina():
    ini, fin = quincena()
    return llamar("POST", "/v1/payroll-periods", {
        "code": f"Q{ini:%Y%m%d}", "name": f"Segunda quincena de octubre {ini.year}",
        "frequency": "biweekly", "startDate": str(ini), "endDate": str(fin), "paymentDate": str(fin)})["id"]


def nomina():
    liquidada()
    pid = int(sql("SELECT id FROM payroll_periods WHERE company_id=1 AND deleted_at IS NULL "
                  "ORDER BY id DESC LIMIT 1"))
    llamar("POST", f"/v1/payroll-periods/{pid}/calculate")


ESTADOS = {"base": base, "fichas": fichas, "cartera": cartera, "caja": caja, "ventas": ventas,
           "cobradas": cobradas, "liquidada": liquidada, "nomina": nomina}

if __name__ == "__main__":
    TOKEN = entrar("admin", "admin")
    ESTADOS[sys.argv[1]]()
