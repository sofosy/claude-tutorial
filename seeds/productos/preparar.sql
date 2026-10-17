UPDATE companies SET legalName='Tienda Germiva Demo S.R.L.', tradeName='Tienda Germiva', rnc='130555001', email='ventas@tienda.germiva.com', website='https://germiva.com' WHERE id=1;
UPDATE users SET email='admin@germiva.com', current_company_id=1 WHERE id=1;
UPDATE attributes SET options=JSON_ARRAY('S','M','L','XL') WHERE id=2 AND company_id=1;
DELETE FROM products WHERE company_id=1 AND code='INS-001';
CREATE TEMPORARY TABLE t AS SELECT * FROM products WHERE id=52;
UPDATE t SET id=(SELECT m FROM (SELECT MAX(id)+1 m FROM products) x), name='Tela de algodón', code='INS-001', description='Tela de algodón peinado, por metro', description_html=NULL, brand=NULL, purchasePrice=180, salePrice=250, lastPurchasePrice=180, averagePurchasePrice=180, has_variants=0, created_at=NOW(6), updated_at=NOW(6), visible_in_store=0;
INSERT INTO products SELECT * FROM t;
SELECT id,name,code FROM products WHERE company_id=1 AND code='INS-001';
