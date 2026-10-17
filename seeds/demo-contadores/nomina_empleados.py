"""Plantilla de Caribe Fresco: 16 empleados con salario mensual (nombres y cédulas ficticios, con dígito verificador válido)."""
import random
from api import api, sql
M = "maria.santana@caribefresco.demo"
def cedula(base):
    s = f"{base:010d}"; tot = 0
    for i, ch in enumerate(s):
        d = int(ch) * (1 if i % 2 == 0 else 2); tot += d // 10 + d % 10
    return s + str((10 - tot % 10) % 10)
EMPLEADOS = [  # nombre, cargo, departamento, salario, ingreso
 ("Rafael Santana Ureña", 2, 1, 145000, "2021-03-01"), ("Yolanda Marte Jiménez", 3, 4, 95000, "2021-06-14"),
 ("Carlos Manuel Abreu Peña", 4, 8, 62000, "2022-01-10"), ("Wendy Altagracia Pichardo", 6, 5, 48000, "2022-04-04"),
 ("José Miguel Taveras Gil", 9, 9, 52000, "2022-08-01"), ("Ana Karina De los Santos", 10, 7, 32000, "2023-02-13"),
 ("Luis Ernesto Polanco Díaz", 8, 11, 45000, "2023-05-02"), ("Francisco Javier Mejía Soto", 4, 8, 55000, "2022-11-21"),
 ("Rosa Elena Batista Cruz", 10, 4, 30000, "2024-01-08"), ("Pedro Antonio Cruz Reyes", 10, 8, 28500, "2023-09-18"),
 ("Miguel Ángel Rosario Vidal", 10, 8, 28500, "2024-03-04"), ("Juana María Encarnación", 10, 6, 24000, "2024-06-03"),
 ("Ramón Darío Guzmán Lora", 10, 6, 24000, "2024-07-15"), ("Carmen Luisa Fernández Mota", 7, 4, 36000, "2025-01-13"),
 ("Héctor Julio Vargas Núñez", 10, 8, 26000, "2025-02-17"), ("Altagracia Mercedes Peña", 10, 6, 24000, "2025-04-07")]
def sembrar():
    ya = {r[0] for r in sql("SELECT name FROM partners WHERE company_id=15 AND partnerType='EMPLOYEE' AND deleted_at IS NULL")}
    random.seed(7)
    for i, (n, cargo, dep, sal, ing) in enumerate(EMPLEADOS):
        if n in ya: continue
        r = api(M, "POST", "/v1/employees", {"name": n, "documentType": "CEDULA", "documentNumber": cedula(4029000000 + i * 7919 + random.randint(0, 999)),
            "employeeNumber": f"CF-{i+1:03d}", "position": cargo, "department": dep, "hireDate": ing + "T04:00:00.000Z", "contractStatus": "active",
            "baseSalary": f"{sal:.2f}", "paymentType": "fixed", "payrollFrequency": "monthly", "createUserAccess": False, "workSchedule": 4},
            permitir=(400, 422, 500))
        print(n, "->", (r or {}).get("id") or r)
if __name__ == "__main__":
    sembrar()
