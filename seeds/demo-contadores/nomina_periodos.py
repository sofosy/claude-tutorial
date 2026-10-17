"""Períodos de nómina mensual de Caribe Fresco: julio–septiembre calculados, aprobados y pagados; octubre aprobado (pago el 30)."""
import json
from api import api, sql
M = "maria.santana@caribefresco.demo"
PER = [("2026-M07", "Julio 2026", "2026-07-01", "2026-07-31", True), ("2026-M08", "Agosto 2026", "2026-08-01", "2026-08-31", True),
       ("2026-M09", "Septiembre 2026", "2026-09-01", "2026-09-30", True), ("2026-M10", "Octubre 2026", "2026-10-01", "2026-10-31", False)]
def sembrar():
    hechos = {r[0] for r in sql("SELECT code FROM payroll_periods WHERE company_id=15")}
    for code, nombre, ini, fin, pagar in PER:
        if code in hechos: continue
        pago = fin if pagar else "2026-10-30"
        r = api(M, "POST", "/v1/payroll-periods", {"code": code, "name": nombre, "frequency": "monthly", "startDate": ini, "endDate": fin, "paymentDate": pago})
        pid = r["id"]
        c = api(M, "POST", f"/v1/payroll-periods/{pid}/calculate", None, permitir=(400, 422, 500)); print(nombre, "calc", str(c)[:160])
        a = api(M, "POST", f"/v1/payroll-periods/{pid}/approve", None, permitir=(400, 422, 500)); print(nombre, "aprob", str(a)[:160])
        if pagar:
            p = api(M, "PATCH", f"/v1/payroll-periods/{pid}/mark-as-paid", {"paymentDate": pago, "paymentReference": f"TRF-{code}"}, permitir=(400, 422, 500))
            print(nombre, "pago", str(p)[:160])
if __name__ == "__main__":
    sembrar()
