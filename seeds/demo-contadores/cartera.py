"""Cartera de la firma Reyes & Mercedes (12): clientes nuevos creados desde la herramienta del contador (datos ficticios)."""
import json
from api import api, cambiar_empresa, sql
A = "ana.reyes@reyesmercedes.demo"
CLIENTES = [
 ("130555201", "SUPERMERCADO LOS HIDALGOS SRL", "Supermercado Los Hidalgos", "gerencia@loshidalgos.demo", "Ramona Hidalgo", "ACCOUNTING"),
 ("130555202", "RESTAURANTE EL CONUCO GOURMET SRL", "El Conuco Gourmet", "admin@conucogourmet.demo", "Teodoro Batista", "ACCOUNTING_PAYROLL"),
 ("130555203", "FERRETERIA MULTIHOGAR DEL ESTE SRL", "Ferretería Multihogar", "ventas@multihogar.demo", "Esteban Rijo", "ACCOUNTING"),
 ("130555204", "CLINICA VETERINARIA HUELLITAS SRL", "Veterinaria Huellitas", "citas@huellitas.demo", "Paola Castillo", "ACCOUNTING"),
 ("130555205", "CONSTRUCTORA PIEDRA ANGULAR SRL", "Piedra Angular", "obras@piedraangular.demo", "Manuel Ozuna", "ACCOUNTING_PAYROLL"),
 ("130555206", "FARMACIA LA ESPERANZA SRL", "Farmacia La Esperanza", "farmacia@laesperanza.demo", "Ivelisse Matos", "ACCOUNTING"),
 ("130555207", "TALLER MECANICO HERMANOS FELIX SRL", "Taller Hermanos Félix", "taller@hermanosfelix.demo", "Wilson Félix", "ACCOUNTING"),
 ("130555208", "AGENCIA DE VIAJES BRISAS DEL MAR SRL", "Viajes Brisas del Mar", "reservas@brisasdelmar.demo", "Claudia Peralta", "ACCOUNTING"),
 ("130555209", "COLEGIO LUZ DEL SABER SRL", "Colegio Luz del Saber", "direccion@luzdelsaber.demo", "Bernarda Liriano", "ACCOUNTING_PAYROLL"),
 ("130555210", "PANIFICADORA EL TRIGAL SRL", "Panificadora El Trigal", "pedidos@eltrigal.demo", "Fausto Almánzar", "ACCOUNTING"),
]
def sembrar():
    cambiar_empresa(A, 12)
    ya = {r[0] for r in sql("SELECT rnc FROM companies WHERE rnc LIKE '1305552%'")}
    for rnc, legal, com, mail, dueno, nivel in CLIENTES:
        if rnc in ya: continue
        r = api(A, "POST", "/v1/accountants/clients/create-company", {"rnc": rnc, "legalName": legal, "tradeName": com, "ownerEmail": mail,
            "ownerName": dueno, "phone": f"809-555-0{rnc[-3:]}", "accessLevel": nivel}, permitir=(400, 409, 422, 500))
        print(com, json.dumps(r, ensure_ascii=False)[:160])
if __name__ == "__main__":
    sembrar()
