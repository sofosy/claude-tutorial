"""Pagos a proveedores de Caribe Fresco: todo lo emitido hasta el 9-sep se paga a ~30 días; septiembre después del 9, la mitad."""
import datetime as dt, random, json
from api import api, sql
M = "maria.santana@caribefresco.demo"; HOY = dt.date(2026, 10, 10)
random.seed(99)
filas = sql("SELECT id, DATE(issueDate), outstandingAmount, documentNumber FROM accounts_payable WHERE company_id=15 AND deleted_at IS NULL AND outstandingAmount>0 ORDER BY issueDate") \
    if any(r[0] == 'company_id' for r in sql("SHOW COLUMNS FROM accounts_payable")) else []
print(len(filas), "cuentas por pagar abiertas")
hechos = 0
for i, (apid, emision, saldo, doc) in enumerate(filas):
    f = dt.date.fromisoformat(emision)
    pago = f + dt.timedelta(days=random.randint(25, 33))
    if pago >= HOY: continue
    if f >= dt.date(2026, 9, 10) and random.random() < 0.5: continue
    r = api(M, "POST", f"/v1/accounts-payable/{apid}/apply-payment", {"paymentAmount": float(saldo), "paymentDate": pago.isoformat(),
        "paymentMethod": "bank_transfer", "reference": f"TRF-{pago:%m%d}-{i:03d}"}, permitir=(400, 409, 422, 500))
    if isinstance(r, dict) and r.get("_error"): print("error", apid, r["_cuerpo"][:200]); break
    hechos += 1
print("pagadas", hechos)
print(sql("SELECT ROUND(SUM(outstandingAmount)), SUM(outstandingAmount>0) FROM accounts_payable WHERE company_id=15 AND deleted_at IS NULL"))
