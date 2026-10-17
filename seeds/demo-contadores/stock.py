"""Existencias iniciales (movimiento 17 «Carga inicial de existencias») en Almacén Principal / ubicación 4."""
import random
from api import api, sql
from catalogo import PRODUCTOS, M
random.seed(15)
for c, n, u, costo, precio, imp in PRODUCTOS:
    pid = int(sql(f"SELECT id FROM products WHERE company_id=15 AND code='{c}'")[0][0])
    if sql(f"SELECT COUNT(*) FROM inventory_movement m JOIN inventory i ON i.id=m.inventory_id WHERE i.product_id={pid}")[0][0] != "0": continue
    qty = random.choice([60, 80, 120, 150, 200, 240])
    api(M, "POST", f"/v1/product/{pid}/inventory/entry", {"product": pid, "quantity": qty, "inventoryLocation": 4, "inventoryMovementType": 17,
        "unitPrice": str(costo), "batchNumber": "INI-2026", "notes": "Carga inicial"})
    print("stock", c, qty)
