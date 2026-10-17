"""Caja «Caja Mostrador» de Caribe Fresco, turno abierto hoy y ventas de mostrador (B02, consumidor final, efectivo)."""
import json, random
from api import api, sql
M = "maria.santana@caribefresco.demo"
def sembrar():
    c = sql("SELECT id FROM cashiers WHERE company_id=15 AND deleted_at IS NULL LIMIT 1")
    cid = int(c[0][0]) if c else api(M, "POST", "/v1/cashiers", {"code": "CAJA-01", "name": "Caja Mostrador", "location": "Almacén Principal",
                                                                    "acceptCash": True, "acceptCard": True, "acceptTransfer": True})["id"]
    s = api(M, "POST", "/v1/cashiers/sessions/open", {"cashier": cid, "initialCash": 5000, "denominations": [{"cashDenomination": 2, "quantity": 5}]}, permitir=(400, 409, 422))
    sid = s.get("id") or (s.get("session") or {}).get("id")
    if not sid:
        print("sesión:", json.dumps(s, ensure_ascii=False)[:300]); sid = int(sql(f"SELECT id FROM cashier_sessions WHERE cashier_id={cid} ORDER BY id DESC LIMIT 1")[0][0])
    prods = []
    for pid, code in sql("SELECT id, code FROM products WHERE company_id=15 AND code IN ('CF-GUI','CF-AGP','CF-LIM','CF-NAR','CF-VER','CF-COC','CF-PIN','CF-LEC')"):
        p = api(M, "GET", f"/v1/product/one/{pid}"); prods.append((int(pid), p["prices"][0]["id"], float(p["prices"][0]["price"]), float(p["tax"]["percentage"])))
    random.seed(10)
    for _ in range(9):
        lineas = random.sample(prods, random.choice([1, 2, 3])); det = []; tot = 0.0
        for pid, prid, precio, tasa in lineas:
            q = random.choice([1, 2, 3]); det.append({"product": pid, "quantity": q, "priceId": prid}); tot += q * precio * (1 + tasa / 100)
        tot = round(tot, 2); recibido = float(int(tot / 500 + 1) * 500)
        r = api(M, "POST", "/v1/invoices", {"ncfType": 2, "paymentType": 1, "details": det,
            "payment": {"amount": f"{tot:.2f}", "paymentMethodCode": "CASH", "amountReceived": f"{recibido:.2f}", "cashierSession": sid}}, permitir=(400, 422, 500))
        print("pos", r.get("invoiceNumber") or json.dumps(r, ensure_ascii=False)[:300])
if __name__ == "__main__":
    sembrar()
