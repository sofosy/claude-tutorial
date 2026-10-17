"""Deja el escenario listo para una toma del video «demo-contadores» (correr ANTES de grabar):
- Ana entra a su firma (current_company_id = 12), no a un cliente.
- Caribe Fresco (15) vuelve a tener el 606/607 de septiembre SIN descargar: sale en rojo.
Ojo: la API guarda 5 min en memoria el resumen de la cartera; entre tomas, esperar 5 min."""
from api import sql
sql("UPDATE users SET current_company_id=12 WHERE id=242")
sql("DELETE FROM audit_logs WHERE company_id=15 AND event IN ('EXPORT_606','EXPORT_607') AND entity_id='202609'")
print("escenario listo: Ana en su firma, Caribe Fresco con el 606/607 de septiembre pendiente")
