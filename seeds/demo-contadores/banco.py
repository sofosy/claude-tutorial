"""Cuenta bancaria de Caribe Fresco y conciliaciones de agosto (completa) y septiembre (completa)."""
import json
from api import api, sql
M = "maria.santana@caribefresco.demo"
def sembrar():
    cta = sql("SELECT id FROM bank_accounts WHERE company_id=15 AND deleted_at IS NULL LIMIT 1")
    if cta: cid = int(cta[0][0])
    else:
        r = api(M, "POST", "/v1/bank-accounts", {"accountName": "Cuenta corriente operativa", "accountNumber": "7104829935", "accountType": "checking",
            "initialBalance": 1250000, "bank": 1, "glAccount": 7, "isDefault": True, "openingDate": "2026-04-30", "accountHolder": "Distribuidora Caribe Fresco SRL"})
        cid = r["id"]; print("cuenta", cid)
    if sql("SELECT COUNT(*) FROM bank_reconciliations WHERE company_id=15")[0][0] != "0": print("conciliaciones ya hechas"); return
    for ref, ini, fin, per, aper, cierre in (("CONC-2026-08", "2026-08-01", "2026-08-31", 198, 1612450.30, 1987320.75),
                                             ("CONC-2026-09", "2026-09-01", "2026-09-30", 199, 1987320.75, 2348915.40)):
        r = api(M, "POST", "/v1/bank-reconciliation", {"referenceNumber": ref, "reconciliationDate": fin, "statementStartDate": ini, "statementEndDate": fin,
            "openingBalance": aper, "closingBalance": cierre, "bankAccount": cid, "accountingPeriod": per}, permitir=(400, 422, 500))
        rid = r.get("id")
        print(ref, rid or json.dumps(r, ensure_ascii=False)[:300])
        if not rid: continue
        for f, d, monto in ((ini[:8] + "08", "Depósito cobros clientes", 420500.0), (ini[:8] + "15", "Transferencia Supermercado La Estrella", 318750.0),
                            (ini[:8] + "22", "Depósito cobros ruta Santiago", 265300.0)):
            api(M, "POST", f"/v1/bank-reconciliation/{rid}/items", {"transactionDate": f, "description": d, "bankAmount": monto, "bookAmount": monto, "transactionType": "deposit"}, permitir=(400, 422))
        print(json.dumps(api(M, "PATCH", f"/v1/bank-reconciliation/{rid}/complete", {}, permitir=(400, 422, 500)), ensure_ascii=False)[:200])
if __name__ == "__main__":
    sembrar()
