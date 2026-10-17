"""Ventas al por mayor (supermercados y hoteles) para que Caribe Fresco tenga margen sano: ~14 por mes, RD$90–220 mil."""
import json, random, datetime as dt, pathlib
from api import api, sql
from movimiento_util import dias
M = "maria.santana@caribefresco.demo"; HOY = dt.date(2026, 10, 10)
EST = pathlib.Path(__file__).with_name("estado.json")
est = json.loads(EST.read_text(encoding="utf-8"))
def guardar(): EST.write_text(json.dumps(est, ensure_ascii=False, indent=1), encoding="utf-8")
random.seed(3030)
prods = []
for pid, code in sql("SELECT id, code FROM products WHERE company_id=15 AND deleted_at IS NULL AND code IN ('CF-ARR','CF-HAB','CF-UVA','CF-MAZ','CF-CEB','CF-PAP','CF-PLA','CF-FRE','CF-NAM','CF-PIM','CF-YUC','CF-AGU','CF-TOM','CF-AJI')"):
    p = api(M, "GET", f"/v1/product/one/{pid}")
    prods.append({"id": int(pid), "price": p["prices"][0]["id"], "inv": p["managesInventory"], "costo": float(p["purchasePrice"] or 0)})
if not est.get("repuesto2"):
    coop = int(sql("SELECT id FROM partners WHERE company_id=15 AND tin='130555130'")[0][0])
    for p in prods:
        if p["inv"]:
            api(M, "POST", f"/v1/product/{p['id']}/inventory/entry", {"product": p["id"], "quantity": 1500, "inventoryLocation": 4, "inventoryMovementType": 1,
                "partner": coop, "unitPrice": str(p["costo"]), "batchNumber": "REP-2026B", "notes": "Reposición mayorista"})
    est["repuesto2"] = True; guardar(); print("reposición mayorista lista", flush=True)
GRANDES = ["130555102", "130555103", "130555107", "130555108", "130555116", "130555117", "130555118"]
clis = [int(r[0]) for r in sql("SELECT id FROM partners WHERE company_id=15 AND tin IN ('" + "','".join(GRANDES) + "')")]
VOL = {(2026, 5): 12, (2026, 6): 13, (2026, 7): 14, (2026, 8): 15, (2026, 9): 16, (2026, 10): 18}
est.setdefault("grandes", [])
for (y, m), n in VOL.items():
    clave = f"{y}-{m:02d}"; hechas = sum(1 for v in est["grandes"] if v["mes"] == clave)
    for f in dias(y, m, n)[hechas:]:
        det = [{"product": p["id"], "quantity": random.choice([12, 15, 18, 20, 25, 30]), "priceId": p["price"]} for p in random.sample(prods, random.choice([3, 4, 4, 5]))]
        r = api(M, "POST", "/v1/invoices", {"issuedDate": f.isoformat(), "ncfType": 1, "partner": random.choice(clis), "paymentType": 2,
                                            "paymentDueDate": (f + dt.timedelta(days=30)).isoformat(), "terms": "30 días", "details": det})
        num, total = r["invoiceNumber"], r["total"]
        api(M, "PATCH", f"/v1/invoices/change-status/{num}", {"invoiceStatusCode": "EMITTED"})
        cobro = f + dt.timedelta(days=random.randint(18, 40))
        pagar = cobro < HOY and (f.month < 9 or random.random() < 0.6)
        if pagar:
            api(M, "POST", "/v1/payment", {"invoiceNumber": num, "amount": str(total), "amountReceived": str(total), "transactionDate": cobro.isoformat(), "paymentMethodCode": "TRANSFER"})
        est["grandes"].append({"mes": clave, "num": num, "total": total, "pagada": pagar}); guardar()
    print("mayoristas", clave, "listas", flush=True)
print("FIN mayoristas", len(est["grandes"]), flush=True)
