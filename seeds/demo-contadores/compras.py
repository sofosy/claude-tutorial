"""Compras recibidas (e-CF E31 del proveedor) por el buzón manual: alimentan Compras, CxP y el 606."""
from api import api
M = "maria.santana@caribefresco.demo"
def r2(x): return round(x + 1e-9, 2)
def comprar(ncf, rnc, nombre, desc, monto, fecha, vence, cat="09", gs=1, itbis=True, tasa="18"):
    itb = r2(monto * 0.18) if itbis else 0.0
    tasa = tasa if itbis else "E"
    det = [{"productName": desc, "quantity": 1, "unitPrice": monto, "subtotal": monto, "netAmount": monto, "taxableAmount": monto if itbis else 0,
            "taxAmount": itb, "total": r2(monto + itb), "taxRateCode": tasa, "goodOrServiceIndicator": gs}]
    tb = [{"taxRateCode": tasa, "taxRatePercentage": 18 if itbis else 0, "taxableAmount": monto if itbis else 0, "taxAmount": itb, "itemCount": 1}]
    body = {"acknowledgeUnbilledReceipts": True, "invoice": {
        "saveAsDraft": False, "recordAsPurchase": True, "ncfTypeCode": "31", "ncf": ncf, "buyerRnc": rnc, "buyerLegalName": nombre, "buyerName": nombre,
        "paymentTypeCode": "2", "issueDate": fecha, "paymentDueDate": vence, "goods606Category": cat, "details": det,
        "totals": {"subtotal": monto, "totalTaxableAmount": monto if itbis else 0, "totalTaxAmount": itb, "total": r2(monto + itb), "taxBreakdown": tb}}}
    return api(M, "POST", "/v1/supplier-document-inbox/manual", body, permitir=(400, 409, 422, 500))
if __name__ == "__main__":
    import json
    r = comprar("E310000900001", "130555130", "Cooperativa Agrícola Constanza Verde", "Vegetales frescos (prueba)", 48500.0, "2026-09-03", "2026-10-03", itbis=False)
    print(json.dumps(r, ensure_ascii=False)[:600])
