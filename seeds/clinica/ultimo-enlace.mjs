// node seeds/clinica/ultimo-enlace.mjs → imprime el token del último enlace de registro de la clínica (para abrirlo en cámara).
import { uno, empresa } from './_lib.mjs';
console.log(uno(`SELECT token FROM patient_intake_links WHERE company_id=${empresa()} ORDER BY id DESC LIMIT 1`));
