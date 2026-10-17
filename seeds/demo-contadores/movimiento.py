"""Seis meses de movimiento para Caribe Fresco (empresa 15): reposición, ventas con cobros y compras recibidas.
Deja un registro en estado.json para no duplicar si se vuelve a correr. Uso: python movimiento.py"""
import json, random, datetime as dt, pathlib
from api import api, sql
from compras import comprar, r2
M = "maria.santana@caribefresco.demo"; HOY = dt.date(2026, 10, 10)
EST = pathlib.Path(__file__).with_name("estado.json")
est = json.loads(EST.read_text(encoding="utf-8")) if EST.exists() else {}
def guardar(): EST.write_text(json.dumps(est, ensure_ascii=False, indent=1), encoding="utf-8")
random.seed(2026)

# ── productos con su precio ──
prods = []
for pid, code in sql("SELECT id, code FROM products WHERE company_id=15 AND deleted_at IS NULL AND code LIKE 'CF-%'"):
    p = api(M, "GET", f"/v1/product/one/{pid}")
    if not p.get("prices"): continue
    prods.append({"id": int(pid), "code": code, "price": p["prices"][0]["id"], "precio": float(p["prices"][0]["price"]),
                  "inv": p["managesInventory"], "itbis": float(p["tax"]["percentage"]), "costo": float(p["purchasePrice"] or 0)})
print(len(prods), "productos con precio", flush=True)

# ── 1. reposición (una vez) ──
if not est.get("repuesto"):
    coop = int(sql("SELECT id FROM partners WHERE company_id=15 AND tin='130555130'")[0][0])
    for p in prods:
        if p["inv"]:
            api(M, "POST", f"/v1/product/{p['id']}/inventory/entry", {"product": p["id"], "quantity": 500, "inventoryLocation": 4,
                "inventoryMovementType": 1, "partner": coop, "unitPrice": str(p["costo"]), "batchNumber": "REP-2026", "notes": "Reposición de temporada"})
    est["repuesto"] = True; guardar(); print("reposición lista", flush=True)

# ── 2. ventas ──
clientes = [int(r[0]) for r in sql("SELECT id FROM partners WHERE company_id=15 AND deleted_at IS NULL AND partnerType='CUSTOMER' AND name<>'Consumidor Final'")]
grandes = clientes[:8]  # unos pocos compran más seguido
VOL = {(2026, 5): 18, (2026, 6): 22, (2026, 7): 26, (2026, 8): 30, (2026, 9): 36, (2026, 10): 16}
def dias(y, m, n):
    ult = (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)).day
    tope = 9 if (y, m) == (2026, 10) else ult
    hab = [dt.date(y, m, d) for d in range(1, tope + 1) if dt.date(y, m, d).weekday() != 6]
    return sorted(random.choice(hab) for _ in range(n))
est.setdefault("ventas", [])
for (y, m), n in VOL.items():
    clave = f"{y}-{m:02d}"
    hechas = sum(1 for v in est["ventas"] if v["mes"] == clave)
    for f in dias(y, m, n)[hechas:]:
        cli = random.choice(grandes) if random.random() < 0.55 else random.choice(clientes)
        lineas = random.sample(prods, random.choice([1, 2, 2, 3, 3, 4]))
        det = [{"product": p["id"], "quantity": random.choice([3, 5, 6, 8, 10, 12, 15, 20]) if p["precio"] < 2000 else random.choice([2, 3, 4, 5, 6]),
                "priceId": p["price"]} for p in lineas]
        credito = random.random() < 0.7
        body = {"issuedDate": f.isoformat(), "ncfType": 1, "partner": cli, "paymentType": 2 if credito else 1, "details": det}
        if credito: body.update(paymentDueDate=(f + dt.timedelta(days=30)).isoformat(), terms="30 días")
        r = api(M, "POST", "/v1/invoices", body)
        num, total = r["invoiceNumber"], r["total"]
        api(M, "PATCH", f"/v1/invoices/change-status/{num}", {"invoiceStatusCode": "EMITTED"})
        # cobro: contado el mismo día; crédito a los 20–45 días si ya pasó (septiembre a medias, octubre pendiente)
        cobro = f if not credito else f + dt.timedelta(days=random.randint(20, 45))
        pagar = (not credito) or (cobro < HOY and (f.month < 9 or random.random() < 0.55) and random.random() > 0.06)
        if pagar:
            api(M, "POST", "/v1/payment", {"invoiceNumber": num, "amount": str(total), "amountReceived": str(total),
                "transactionDate": cobro.isoformat(), "paymentMethodCode": "CASH" if not credito else random.choice(["TRANSFER", "TRANSFER", "CHECK"])})
        est["ventas"].append({"mes": clave, "num": num, "total": total, "pagada": pagar}); guardar()
    print("ventas", clave, "listas", flush=True)

# ── 3. compras recibidas ──
prov = {n: t for t, n in sql("SELECT tin, name FROM partners WHERE company_id=15 AND deleted_at IS NULL AND partnerType='SUPPLIER' AND tin IS NOT NULL")}
CAMPO = [("Cooperativa Agrícola Constanza Verde", "Vegetales frescos de Constanza"), ("Finca Hermanos Tavárez SRL", "Plátano, yuca y víveres"),
         ("Importadora Frutas del Mundo SRL", "Frutas importadas (uvas y manzanas)"), ("Agroexportadora Valle de Ocoa SRL", "Ají, tomate y cebolla"),
         ("AGROINDUSTRIAL MONTE VERDE SRL", "Aguacate y mango")]
SERV = [("EDENORTE DOMINICANA SA", "Energía eléctrica", 14500, 2), ("COMPANIA DOMINICANA DE TELEFONOS SA", "Internet y telefonía", 4590, 2),
        ("SEGURIDAD INTEGRAL DOMINICANA SRL", "Servicio de vigilancia", 14000, 2), ("TRANSPORTE RAPIDO DEL CIBAO SRL", "Fletes de distribución", 18500, 2),
        ("COMBUSTIBLES DEL NORTE SRL", "Combustible de la flotilla", 26500, 1), ("EMPAQUES DEL CARIBE SRL", "Cajas y empaques", 12800, 1),
        ("PAPELERIA LA NACIONAL SRL", "Materiales de oficina", 3200, 1)]
est.setdefault("compras", [])
hechas = {c["ncf"] for c in est["compras"]}
sec = 900100
for (y, m), n in VOL.items():
    fechas = dias(y, m, 8 if m < 9 else 12)
    for i, f in enumerate(fechas):
        nom, desc = CAMPO[i % len(CAMPO)]; sec += 1; ncf = f"E31{sec:010d}"
        if ncf in hechas or nom not in prov: continue
        monto = float(random.choice(range(38000, 142000, 1250)))
        r = comprar(ncf, prov[nom], nom, desc, monto, f.isoformat(), (f + dt.timedelta(days=30)).isoformat(), cat="09", gs=1, itbis=False)
        est["compras"].append({"ncf": ncf, "mes": f"{y}-{m:02d}", "ok": bool(r and r.get("success"))}); guardar()
    for j, (nom, desc, base, gs) in enumerate(SERV):
        if (y, m) == (2026, 10) and j < 4: continue  # octubre ya trae estos servicios
        sec += 1; ncf = f"E31{sec:010d}"
        if ncf in hechas or nom not in prov: continue
        f = dt.date(y, m, min(5 + j * 3, 9 if (y, m) == (2026, 10) else 26))
        monto = r2(base * random.uniform(0.9, 1.12))
        r = comprar(ncf, prov[nom], nom, desc, monto, f.isoformat(), (f + dt.timedelta(days=30)).isoformat(), cat="02", gs=gs)
        est["compras"].append({"ncf": ncf, "mes": f"{y}-{m:02d}", "ok": bool(r and r.get("success"))}); guardar()
    print("compras", y, m, "listas", flush=True)
print("FIN", len(est["ventas"]), "ventas,", len(est["compras"]), "compras", flush=True)
