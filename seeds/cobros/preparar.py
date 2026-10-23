"""Arma por el API el estado que cada video de la serie Cobros encuentra hecho.

  base     clientes de la Distribuidora Germiva con facturas B01 a crédito, emitidas y sin cobrar:
             Ferretería Germiva del Norte  4 facturas: 1,180 · 2,360 · 3,540 · 5,900
             Colmado Germiva Este          1 factura de 1,180 (cobro total)
             Farmacia Germiva Sur 2,360 (abono) · Librería Germiva Centro 1,180 (efectivo) · Taller Germiva Oeste 2,360 (combinado)
             Constructora Germiva Ciudad   1 factura de 11,800 (para la retención del cliente)
             Supermercado Germiva (RNC compartido): Central 2 facturas de 1,180; Oriental 1 de 1,180
  cobrado  base + un cobro de 5,000 de la Ferretería que salda las dos primeras facturas y deja la
             tercera parcial (RCP de varias facturas), punto de partida del video 07.

Todo lo inventado lleva «Germiva» o el rango de RNC 130555 (privacidad de la serie).
"""
import importlib.util
import os
import sys
import uuid

AQUI = os.path.dirname(os.path.abspath(__file__))


def cargar(nombre, *ruta):
    spec = importlib.util.spec_from_file_location(nombre, os.path.join(AQUI, *ruta))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


v = cargar("vend", "..", "vendedores", "preparar.py")
c = cargar("cli", "..", "clientes", "preparar.py")
c.v = v

GALON, BROCHA = v.PRODUCTOS[0][0], v.PRODUCTOS[1][0]
FERRETERIA, COLMADO, CONSTRUCTORA = (n for n, _r, _z in c.FERRETERIAS)

# Un cliente por escenario del video 02 y 03: así el selector de factura (que se busca por cliente)
# siempre encuentra UNA sola factura y los montos que dice la voz no dependen del orden.
OTROS = [
    ("Farmacia Germiva Sur", "130555201"),
    ("Librería Germiva Centro", "130555202"),
    ("Taller Germiva Oeste", "130555203"),
]

FACTURAS = {
    FERRETERIA: [[(GALON, 1)], [(GALON, 2)], [(GALON, 3)], [(BROCHA, 20)]],
    COLMADO: [[(GALON, 1)]],
    CONSTRUCTORA: [[(GALON, 10)]],
    "Farmacia Germiva Sur": [[(GALON, 2)]],
    "Librería Germiva Centro": [[(GALON, 1)]],
    "Taller Germiva Oeste": [[(GALON, 2)]],
    "Supermercado Germiva Central": [[(GALON, 1)], [(GALON, 1)]],
    "Supermercado Germiva Oriental": [[(GALON, 1)]],
}


def emitir(nombre, lineas):
    f = v.llamar("POST", "/v1/invoices", {
        "ncfType": v.B01, "incomeType": 1, "currency": v.DOP, "partner": v.cliente(nombre),
        "details": [{"product": v.producto(n), "quantity": q} for n, q in lineas]})
    v.llamar("PATCH", f"/v1/invoices/change-status/{f['invoiceNumber']}", {"invoiceStatusCode": "EMITTED"})
    return f["invoiceNumber"]


def base():
    c.base()
    c.cuenta("Supermercado Germiva Oriental")
    for nombre, rnc in OTROS:
        v.llamar("POST", "/v1/partner", {
            "name": nombre, "tin": rnc, "legalName": nombre + " S.R.L.", "partnerType": ["CUSTOMER"],
            "partnerCategory": "BUSINESS", "customerType": "REGULAR", "documentType": "RNC"})
    for nombre in (FERRETERIA, COLMADO, CONSTRUCTORA, "Supermercado Germiva Central", "Supermercado Germiva Oriental",
                   *(n for n, _ in OTROS)):
        v.llamar("PATCH", f"/v1/partner/{v.cliente(nombre)}", {"paymentTermDays": 30})
    for nombre, lotes in FACTURAS.items():
        for lineas in lotes:
            emitir(nombre, lineas)


def documentos_abiertos(nombre):
    r = v.llamar("GET", f"/v1/payment/settlement/open-documents/{v.cliente(nombre)}")
    return r if isinstance(r, list) else r.get("data", r.get("documents", []))


def cobrado():
    base()
    docs = sorted(documentos_abiertos(FERRETERIA), key=lambda d: d.get("issueDate") or d.get("dueDate") or "")
    # Facturas 1 y 2 completas y la 3 con 1,460 (QA-COBRO-VARIAS-FACTURAS-DEV).
    reparto = [1180, 2360, 1460]
    allocations = [{"accountReceivable": d["accountReceivable"] if "accountReceivable" in d else d["id"],
                    "expectedOutstanding": f"{float(d['outstandingAmount']):.2f}", "amount": f"{a:.2f}"}
                   for d, a in zip(docs, reparto)]
    v.llamar("POST", "/v1/payment/settlement", {
        "partner": v.cliente(FERRETERIA), "settlementKey": uuid.uuid4().hex, "paymentMethodCode": "TRANSFER",
        "amount": "5000.00", "reference": "TRF-998877", "notes": "Pago según remesa de la Ferretería",
        "allocations": allocations})


ESTADOS = {"base": base, "cobrado": cobrado}

if __name__ == "__main__":
    v.TOKEN = v.entrar("admin", "admin")
    ESTADOS[sys.argv[1]]()
