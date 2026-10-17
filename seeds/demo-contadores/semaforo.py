"""Deja la cartera de la firma 12 lista para el video: suscripciones activas, 606/607 de 202609 descargados por la contadora
(menos Caribe Fresco, que es el caso del video) y NCF de consumo bajos en dos clientes (ámbar)."""
import json, urllib.request
from api import api, cambiar_empresa, sql, API, login, _tokens
A = "ana.reyes@reyesmercedes.demo"; PERIODO = "202609"
def txt(rep):
    r = urllib.request.Request(f"{API}/v1/dgii-reports/{rep}/txt?period={PERIODO}", headers={"Authorization": "Bearer " + _tokens[A]})
    with urllib.request.urlopen(r, timeout=120) as resp: return len(resp.read())
def sembrar():
    # suscripciones: clientes pagando (dos en prueba, para que se vea natural)
    sql("UPDATE subscriptions SET status='ACTIVE', plan_id=15, expirationDate='2027-10-31 23:00:00' WHERE company_id BETWEEN 71 AND 78")
    sql("UPDATE subscriptions SET expirationDate='2026-11-30 23:00:00' WHERE company_id IN (79,80)")
    # Colmado Don Chicho (17): abrir septiembre y octubre para que el período salga en verde
    sql("UPDATE accounting_periods SET status='open' WHERE company_id=17 AND startDate >= '2026-09-01' AND startDate < '2026-11-01'")
    # NCF de consumo (B02) bajo el 20 %: ámbar
    for cid, pct in ((17, 0.12), (76, 0.15)):
        sql(f"UPDATE secuentials SET status='active', totalCodesAvailable=FLOOR(totalCodes*{pct}), totalCodesUsed=totalCodes-FLOOR(totalCodes*{pct}) WHERE company_id={cid} AND ncf_type_id=2")
    ya = {r[0] for r in sql(f"SELECT DISTINCT company_id FROM audit_logs WHERE event='EXPORT_607' AND entity_id='{PERIODO}'")}
    for cid in [17] + list(range(71, 81)):
        if str(cid) in ya: continue
        cambiar_empresa(A, cid)
        print(cid, "606", txt("606"), "607", txt("607"), flush=True)
    cambiar_empresa(A, 12)
if __name__ == "__main__":
    sembrar()
