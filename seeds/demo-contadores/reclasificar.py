"""Compras de mercancía a las fincas (606 cat. 09): del gasto 6.03.21 a Inventario de mercancías 1.01.06.01.
Evita contar dos veces el costo (la compra como gasto y luego el costo de ventas). Los servicios siguen como gasto."""
from api import sql
FINCAS = ("Cooperativa Agrícola Constanza Verde", "Finca Hermanos Tavárez SRL", "Importadora Frutas del Mundo SRL",
          "Agroexportadora Valle de Ocoa SRL", "AGROINDUSTRIAL MONTE VERDE SRL")
nombres = "','".join(FINCAS)
je = f"""SELECT DISTINCT je.id FROM journal_entries je JOIN invoices i ON i.invoice_number=je.documentNumber AND i.company_id=je.company_id
         JOIN partners p ON p.id=i.partner_id WHERE je.company_id=15 AND i.invoice_direction='PURCHASE' AND p.name IN ('{nombres}')"""
ids = [r[0] for r in sql(je)]
print(len(ids), "asientos de compras de mercancía")
if ids:
    lista = ",".join(ids)
    sql(f"UPDATE journal_entry_details SET account_id=32 WHERE journal_entry_id IN ({lista}) AND account_id=167")
    sql(f"UPDATE general_ledger SET accountId=32 WHERE journalEntryId IN ({lista}) AND accountId=167")
print(sql("""SELECT DATE_FORMAT(g.date,'%Y-%m') m, ROUND(SUM(CASE WHEN a.code LIKE '4%' THEN g.creditAmount-g.debitAmount ELSE 0 END)) ingresos,
             ROUND(SUM(CASE WHEN a.code LIKE '5%' OR a.code LIKE '6%' THEN g.debitAmount-g.creditAmount ELSE 0 END)) costos_gastos
             FROM general_ledger g JOIN accounting_chart a ON a.id=g.accountId WHERE g.company_id=15 AND g.deleted_at IS NULL GROUP BY 1 ORDER BY 1"""))
