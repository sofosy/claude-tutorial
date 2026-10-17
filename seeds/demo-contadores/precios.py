"""Precio de venta (lista «Precio regular», id 5) para los productos del catálogo que no lo tengan."""
from api import api, sql
from catalogo import PRODUCTOS, M
for c, n, u, costo, precio, imp in PRODUCTOS + [("CF-AGU","",0,650,1250,0),("CF-MAN","",0,480,750,0),("CF-PLA","",0,1450,2100,0),("CF-AGP","",0,120,180,0)]:
    pid = sql(f"SELECT id FROM products WHERE company_id=15 AND code='{c}' AND deleted_at IS NULL")[0][0]
    p = api(M, "GET", f"/v1/product/one/{pid}")
    if p.get("prices"): continue
    api(M, "POST", "/v1/price", {"product": int(pid), "priceListId": 5, "customerType": "REGULAR", "price": f"{precio:.2f}", "taxIncluded": False, "priority": 1})
    print("precio", c, precio)
