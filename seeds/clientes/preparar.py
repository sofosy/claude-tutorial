"""Arma por el API el estado que cada video de la serie Clientes encuentra hecho.

  base        productos y clientes de la Distribuidora Germiva: tres ferreterías con zona,
              una persona con cédula, y UNA cuenta del Supermercado Germiva (RNC 130555300).
  sucursales  base + dos cuentas más del mismo RNC (Oriental y Norte) y una factura emitida y
              cobrada en Central, otra emitida a Oriental. Es el punto de partida del video 06.

Todo lo inventado lleva «Germiva» o el rango de RNC 130555 (privacidad de la serie).
"""
import importlib.util
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("vend", os.path.join(AQUI, "..", "vendedores", "preparar.py"))
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

SUPER_RNC = "130555300"
SUPER_RAZON = "Supermercados Germiva S.R.L."
FERRETERIAS = [
    ("Ferretería Germiva del Norte", "130555101", "NORTE"),
    ("Colmado Germiva Este", "130555102", "ESTE"),
    ("Constructora Germiva Ciudad", "130555103", "CIUDAD"),
]


def cuenta(nombre):
    return v.llamar("POST", "/v1/partner", {
        "name": nombre, "tin": SUPER_RNC, "legalName": SUPER_RAZON, "partnerType": ["CUSTOMER"],
        "partnerCategory": "BUSINESS", "customerType": "REGULAR", "documentType": "RNC"})


def anonimizar():
    """La base sembrada trae clientes y proveedores con nombres y documentos del padrón:
    se renombran por otros inventados (rango 130558) antes de crear los de la serie."""
    v.sql("UPDATE partners SET name=CONCAT('Cliente Demo Germiva ', LPAD(id, 3, '0')), "
          "tin=IF(tin IS NULL, NULL, CONCAT('130558', LPAD(id, 3, '0'))), "
          "legal_name=IF(legal_name IS NULL, NULL, CONCAT('Cliente Demo Germiva ', LPAD(id, 3, '0'), ' S.R.L.')) "
          "WHERE company_id=1 AND id>3 AND partnerType NOT LIKE '%EMPLOYEE%'")
    v.sql("UPDATE customer_fiscal_identities SET tax_id=CONCAT('130558', LPAD(id, 3, '0')), "
          "legal_name=CONCAT('Cliente Demo Germiva ', LPAD(id, 3, '0'), ' S.R.L.') WHERE company_id=1")


def base():
    anonimizar()
    v.llamar("POST", "/v1/user-preferences/incomplete-config-notice/claim", {})
    v.crear_productos()
    for nombre, rnc, zona in FERRETERIAS:
        r = v.llamar("POST", "/v1/partner", {
            "name": nombre, "tin": rnc, "legalName": nombre + " S.R.L.", "partnerType": ["CUSTOMER"], "partnerCategory": "BUSINESS", "customerType": "REGULAR",
            "documentType": "RNC", "salesZone": zona})
    v.llamar("POST", "/v1/partner", {
        "name": "María Germiva Peña", "tin": "40255500099", "partnerType": ["CUSTOMER"],
        "partnerCategory": "PERSON", "customerType": "REGULAR", "documentType": "CEDULA"})
    cuenta("Supermercado Germiva Central")


def sucursales():
    base()
    cuenta("Supermercado Germiva Oriental")
    cuenta("Supermercado Germiva Norte")
    central = v.cliente("Supermercado Germiva Central")
    oriental = v.cliente("Supermercado Germiva Oriental")
    for pid in (central, oriental):
        f = v.llamar("POST", "/v1/invoices", {
            "ncfType": v.B01, "incomeType": 1, "currency": v.DOP, "partner": pid,
            "details": [{"product": v.producto(v.PRODUCTOS[0][0]), "quantity": 2}]})
        v.llamar("PATCH", f"/v1/invoices/change-status/{f['invoiceNumber']}", {"invoiceStatusCode": "EMITTED"})
        if pid == central:
            v.cobrar(f["invoiceNumber"], v.total(f["invoiceNumber"]), "Transferencia Banco Popular")


ESTADOS = {"base": base, "sucursales": sucursales}

if __name__ == "__main__":
    v.TOKEN = v.entrar("admin", "admin")
    ESTADOS[sys.argv[1]]()
