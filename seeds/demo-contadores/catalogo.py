"""Catálogo de la demo comercial (Caribe Fresco, empresa 15): productos, clientes y proveedores ficticios.
Idempotente: no repite lo que ya existe (por código o RNC). Uso: python catalogo.py"""
from api import api, sql
M = "maria.santana@caribefresco.demo"
EXENTO, ITBIS, UND, SACO, FARDO, DOC = 4, 1, 43, 46, 14, 13
PRODUCTOS = [  # código, nombre, unidad, costo, precio, impuesto
 ("CF-PIN","Caja de piña (8 unidades)",UND,520,800,EXENTO), ("CF-YUC","Saco de yuca 50 lb",SACO,900,1350,EXENTO),
 ("CF-TOM","Caja de tomate barceló 25 lb",UND,700,1050,EXENTO), ("CF-CEB","Saco de cebolla roja 50 lb",SACO,1600,2300,EXENTO),
 ("CF-PAP","Saco de papa 50 lb",SACO,1250,1800,EXENTO), ("CF-LEC","Caja de lechosa (10 unidades)",UND,600,900,EXENTO),
 ("CF-LIM","Caja de limón 25 lb",UND,550,850,EXENTO), ("CF-NAR","Caja de naranja dulce",UND,450,700,EXENTO),
 ("CF-BAT","Saco de batata 50 lb",SACO,850,1250,EXENTO), ("CF-AJI","Caja de ají cubanela 25 lb",UND,750,1100,EXENTO),
 ("CF-LCH","Caja de lechuga repollada (24 unidades)",UND,680,1000,EXENTO), ("CF-GUI","Racimo de guineo maduro",UND,250,400,EXENTO),
 ("CF-ZAN","Caja de zanahoria 25 lb",UND,500,780,EXENTO), ("CF-NAM","Saco de ñame 50 lb",SACO,1300,1900,EXENTO),
 ("CF-CHI","Caja de chinola 25 lb",UND,600,920,EXENTO), ("CF-COC","Caja de coco seco (20 unidades)",UND,500,800,EXENTO),
 ("CF-PIM","Caja de pimiento morrón 25 lb",UND,900,1350,EXENTO), ("CF-AUY","Saco de auyama 50 lb",SACO,700,1050,EXENTO),
 ("CF-FRE","Caja de fresas (12 bandejas)",UND,1100,1650,EXENTO), ("CF-UVA","Caja de uvas importadas 18 lb",UND,1800,2600,EXENTO),
 ("CF-MAZ","Caja de manzana roja importada",UND,1600,2350,EXENTO), ("CF-VER","Docena de mazos de cilantro y verdura",DOC,180,300,EXENTO),
 ("CF-BER","Caja de berenjena 25 lb",UND,450,700,EXENTO), ("CF-PEP","Caja de pepino 25 lb",UND,420,650,EXENTO),
 ("CF-HAB","Saco de habichuela roja 50 lb",SACO,2600,3500,EXENTO), ("CF-ARR","Saco de arroz selecto 125 lb",SACO,3900,4950,EXENTO),
]
CLIENTES = [  # RNC ficticio (rango 1305551xx), nombre
 ("130555102","Supermercado La Estrella del Norte SRL"),("130555103","Hotel Brisas del Caribe SRL"),
 ("130555104","Restaurante Sabor Criollo SRL"),("130555105","Colmado La Esquina Feliz SRL"),
 ("130555106","Cafetería El Buen Gusto SRL"),("130555107","Supermercado Mi Familia SRL"),
 ("130555108","Hotel Costa Esmeralda SRL"),("130555109","Comedor Doña Mercedes SRL"),
 ("130555110","Minimarket Los Prados SRL"),("130555111","Pica Pollo El Sabrosón SRL"),
 ("130555112","Restaurante Mar y Tierra SRL"),("130555113","Colegio Nuevo Amanecer SRL"),
 ("130555114","Hospedaje Villa Tropical SRL"),("130555115","Frutería Tropical del Este SRL"),
 ("130555116","Distribuidora El Granero SRL"),("130555117","Supermercado Plaza Central SRL"),
 ("130555118","Catering Eventos del Valle SRL"),("130555119","Heladería Coco Loco SRL"),
 ("130555120","Repostería Dulce Hogar SRL"),("130555121","Colmado Hermanos Rosario SRL"),
]
PROVEEDORES = [("130555130","Cooperativa Agrícola Constanza Verde"),("130555131","Finca Hermanos Tavárez SRL"),
 ("130555132","Importadora Frutas del Mundo SRL"),("130555133","Agroexportadora Valle de Ocoa SRL")]

def sembrar():
  ya = {r[0] for r in sql("SELECT code FROM products WHERE company_id=15 AND deleted_at IS NULL AND code IS NOT NULL")}
  for c, n, u, costo, precio, imp in PRODUCTOS:
      if c in ya: continue
      api(M, "POST", "/v1/product", {"category": "PRODUCT", "name": n, "code": c, "unitMeasureId": u, "taxId": imp, "purchaseTaxId": imp,
          "managesInventory": True, "purchasePrice": costo, "minStock": 10,
          "prices": [{"priceListId": 5, "price": precio, "taxIncluded": False, "customerType": "REGULAR"}]})
      print("producto", c)
  rncs = {r[0] for r in sql("SELECT tin FROM partners WHERE company_id=15 AND deleted_at IS NULL AND tin IS NOT NULL")}
  for rnc, n in CLIENTES:
      if rnc in rncs: continue
      api(M, "POST", "/v1/partner", {"name": n, "tin": rnc, "partnerType": ["CUSTOMER"], "partnerCategory": "BUSINESS", "customerType": "REGULAR", "priceListId": 5}); print("cliente", n)
  for rnc, n in PROVEEDORES:
      if rnc in rncs: continue
      api(M, "POST", "/v1/partner", {"name": n, "tin": rnc, "partnerType": ["SUPPLIER"], "partnerCategory": "BUSINESS"}); print("proveedor", n)

if __name__ == "__main__":
    sembrar()
