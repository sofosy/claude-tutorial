-- Ajustes previos a preparar.mjs cuando el canon se arma sobre la instantánea del dev-env (no Windows).
UPDATE companies SET legalName='Tienda Germiva Demo S.R.L.', tradeName='Tienda Germiva', rnc='130555001', email='ventas@tienda.germiva.com', website='https://germiva.com' WHERE id=1;
UPDATE users SET email='admin@germiva.com', current_company_id=1 WHERE id=1;
UPDATE attributes SET options=JSON_ARRAY('S','M','L','XL') WHERE id=2 AND company_id=1;
